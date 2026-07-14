"""Application configuration model and persistence."""

from __future__ import annotations

import json
import os
import tempfile
from collections.abc import Mapping
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from sephirothos.paths import config_path

LEGACY_SCHEMA_VERSION = 1
CURRENT_SCHEMA_VERSION = 2

DEFAULT_THEME_ID = "void"
DEFAULT_ACCENT_ID = "purple"
DEFAULT_DISPLAY_SCALE = 1.0
DEFAULT_FONT_FAMILY = "Segoe UI"
DEFAULT_BACKGROUND_MODE = "solid"
DEFAULT_WALLPAPER_FIT = "fill"


class ConfigurationError(RuntimeError):
    """Raised when application configuration is invalid or cannot be saved."""


def _required_string(
    data: Mapping[str, Any],
    key: str,
    default: str,
) -> str:
    value = data.get(key, default)

    if not isinstance(value, str) or not value.strip():
        raise ConfigurationError(f"{key} must be a non-empty string.")

    return value.strip()


@dataclass(slots=True)
class AppearanceConfig:
    """User-configurable application appearance."""

    theme_id: str = DEFAULT_THEME_ID
    accent_id: str = DEFAULT_ACCENT_ID
    display_scale: float = DEFAULT_DISPLAY_SCALE
    font_family: str = DEFAULT_FONT_FAMILY

    @classmethod
    def from_mapping(
        cls,
        data: Mapping[str, Any],
    ) -> AppearanceConfig:
        """Validate and construct appearance configuration."""

        theme_id = _required_string(
            data,
            "theme_id",
            DEFAULT_THEME_ID,
        )
        accent_id = _required_string(
            data,
            "accent_id",
            DEFAULT_ACCENT_ID,
        )
        font_family = _required_string(
            data,
            "font_family",
            DEFAULT_FONT_FAMILY,
        )

        display_scale = data.get(
            "display_scale",
            DEFAULT_DISPLAY_SCALE,
        )

        if isinstance(display_scale, bool) or not isinstance(display_scale, int | float):
            raise ConfigurationError("display_scale must be numeric.")

        return cls(
            theme_id=theme_id,
            accent_id=accent_id,
            display_scale=float(display_scale),
            font_family=font_family,
        )

    def to_mapping(self) -> Mapping[str, Any]:
        """Return a JSON-serializable representation."""

        return asdict(self)


@dataclass(slots=True)
class AppConfig:
    """User-configurable SephirothOS state."""

    schema_version: int = CURRENT_SCHEMA_VERSION
    username: str = "User"
    onboarding_complete: bool = False
    appearance: AppearanceConfig = field(
        default_factory=AppearanceConfig,
    )

    @classmethod
    def from_mapping(
        cls,
        data: Mapping[str, Any],
    ) -> AppConfig:
        """Validate and construct configuration from decoded JSON data."""

        schema_version = data.get(
            "schema_version",
            LEGACY_SCHEMA_VERSION,
        )

        if not isinstance(schema_version, int) or isinstance(schema_version, bool):
            raise ConfigurationError("schema_version must be an integer.")

        if schema_version not in (
            LEGACY_SCHEMA_VERSION,
            CURRENT_SCHEMA_VERSION,
        ):
            raise ConfigurationError(f"Unsupported configuration schema: {schema_version}")

        username = _required_string(
            data,
            "username",
            "User",
        )

        onboarding_complete = data.get(
            "onboarding_complete",
            False,
        )

        if not isinstance(onboarding_complete, bool):
            raise ConfigurationError("onboarding_complete must be boolean.")

        if schema_version == LEGACY_SCHEMA_VERSION:
            appearance_data: Mapping[str, Any] = {
                "theme_id": data.get(
                    "theme_id",
                    DEFAULT_THEME_ID,
                ),
                "display_scale": data.get(
                    "display_scale",
                    DEFAULT_DISPLAY_SCALE,
                ),
            }
        else:
            raw_appearance = data.get("appearance", {})

            if not isinstance(raw_appearance, Mapping):
                raise ConfigurationError("appearance must be an object.")

            appearance_data = raw_appearance

        return cls(
            schema_version=CURRENT_SCHEMA_VERSION,
            username=username,
            onboarding_complete=onboarding_complete,
            appearance=AppearanceConfig.from_mapping(
                appearance_data,
            ),
        )

    def to_mapping(self) -> Mapping[str, Any]:
        """Return configuration in a JSON-serializable representation."""

        return asdict(self)


class ConfigStore:
    """Load and atomically save application configuration."""

    def __init__(
        self,
        path: Path | None = None,
    ) -> None:
        self.path = config_path() if path is None else path

    def load(self) -> AppConfig:
        """Load configuration, creating defaults when no file exists."""

        if not self.path.exists():
            config = AppConfig()
            self.save(config)
            return config

        try:
            with self.path.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise ConfigurationError("The configuration root must be a JSON object.")

            source_schema = data.get(
                "schema_version",
                LEGACY_SCHEMA_VERSION,
            )
            config = AppConfig.from_mapping(data)

            if source_schema != CURRENT_SCHEMA_VERSION:
                self.save(config)

            return config

        except (
            ConfigurationError,
            json.JSONDecodeError,
            OSError,
            TypeError,
        ) as error:
            raise ConfigurationError(f"Could not load configuration from {self.path}") from error

    def save(
        self,
        config: AppConfig,
    ) -> None:
        """Save configuration using an atomic file replacement."""

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

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
                temporary_path = Path(
                    temporary_file.name,
                )

            os.replace(
                temporary_path,
                self.path,
            )

        except OSError as error:
            if temporary_path is not None:
                temporary_path.unlink(
                    missing_ok=True,
                )

            raise ConfigurationError(f"Could not save configuration to {self.path}") from error
