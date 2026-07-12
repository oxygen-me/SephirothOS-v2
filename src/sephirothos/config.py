"""Application configuration model and persistence."""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping

from sephirothos.paths import config_path

CURRENT_SCHEMA_VERSION = 1


class ConfigurationError(RuntimeError):
    """Raised when application configuration is invalid or cannot be saved."""


@dataclass(slots=True)
class AppConfig:
    """User-configurable SephirothOS state."""

    schema_version: int = CURRENT_SCHEMA_VERSION
    username: str = "User"
    theme_id: str = "dark"
    display_scale: float = 1.0
    onboarding_complete: bool = False

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> AppConfig:
        """Validate and construct configuration from decoded JSON data."""

        schema_version = data.get("schema_version", CURRENT_SCHEMA_VERSION)
        username = data.get("username", "User")
        theme_id = data.get("theme_id", "dark")
        display_scale = data.get("display_scale", 1.0)
        onboarding_complete = data.get("onboarding_complete", False)

        if not isinstance(schema_version, int) or isinstance(schema_version, bool):
            raise ConfigurationError("schema_version must be an integer.")

        if schema_version != CURRENT_SCHEMA_VERSION:
            raise ConfigurationError(
                f"Unsupported configuration schema: {schema_version}"
            )

        if not isinstance(username, str) or not username.strip():
            raise ConfigurationError("username must be a non-empty string.")

        if not isinstance(theme_id, str) or not theme_id.strip():
            raise ConfigurationError("theme_id must be a non-empty string.")

        if isinstance(display_scale, bool) or not isinstance(
            display_scale, int | float
        ):
            raise ConfigurationError("display_scale must be numeric.")

        if not isinstance(onboarding_complete, bool):
            raise ConfigurationError("onboarding_complete must be boolean.")

        return cls(
            schema_version=schema_version,
            username=username,
            theme_id=theme_id,
            display_scale=float(display_scale),
            onboarding_complete=onboarding_complete,
        )

    def to_mapping(self) -> Mapping[str, Any]:
        """Return configuration in a JSON-serializable representation."""

        return asdict(self)


class ConfigStore:
    """Load and atomically save application configuration."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = config_path() if path is None else path

    def load(self) -> AppConfig:
        """Load configuration, creating defaults when no file exists."""

        if not self.path.exists():
            config = AppConfig()
            self.save(config)
            return config

        try:
            with self.path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise ConfigurationError(
                    "The configuration root must be a JSON object."
                )

            return AppConfig.from_mapping(data)

        except (
            ConfigurationError,
            json.JSONDecodeError,
            OSError,
            TypeError,
        ) as error:
            raise ConfigurationError(
                f"Could not load configuration from {self.path}"
            ) from error

    def save(self, config: AppConfig) -> None:
        """Save configuration using an atomic file replacement."""
        self.path.parent.mkdir(parents=True, exist_ok=True)

        temporary_path: Path | None = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.path.parent,
                prefix=f"{self.path.stem}-",
                suffix=".tmp",
                delete=False,
            ) as temporary_file:
                json.dump(
                    config.to_mapping(),
                    temporary_file,
                    indent=4,
                    ensure_ascii=False,
                )
                temporary_file.write("\n")
                temporary_file.flush()
                os.fsync(temporary_file.fileno())
                temporary_path = Path(temporary_file.name)

            os.replace(temporary_path, self.path)

        except OSError as error:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)

            raise ConfigurationError(
                f"Could not save configuration to {self.path}"
            ) from error
