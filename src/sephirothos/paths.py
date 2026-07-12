"""Filesystem locations used by SephirothOS."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Mapping

from sephirothos.metadata import APPLICATION_NAME


class PathConfigurationError(RuntimeError):
    """Raised when required Windows paths cannot be determined."""


def app_data_directory(
    environment: Mapping[str, str] | None = None,
) -> Path:
    """Return the user-specific SephirothOS application data directory."""

    env = os.environ if environment is None else environment
    appdata = env.get("APPDATA")

    if not appdata:
        raise PathConfigurationError("The APPDATA environment variable is unavailable.")

    return Path(appdata) / APPLICATION_NAME


def config_path(environment: Mapping[str, str] | None = None) -> Path:
    """Return the path to the user configuration file."""

    return app_data_directory(environment) / "config.json"


def log_directory(environment: Mapping[str, str] | None = None) -> Path:
    """Return the directory used for application logs."""

    return app_data_directory(environment) / "logs"


def cache_directory(environment: Mapping[str, str] | None = None) -> Path:
    """Return the directory used for disposable application cache data."""

    return app_data_directory(environment) / "cache"
