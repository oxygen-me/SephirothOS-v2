from pathlib import Path

import pytest

from sephirothos.paths import (
    PathConfigurationError,
    app_data_directory,
    cache_directory,
    config_path,
    log_directory,
)


def test_application_paths_are_derived_from_appdata() -> None:
    environment = {"APPDATA": r"C:\Users\Test\AppData\Roaming"}

    root = Path(environment["APPDATA"]) / "SephirothOS"

    assert app_data_directory(environment) == root
    assert config_path(environment) == root / "config.json"
    assert log_directory(environment) == root / "logs"
    assert cache_directory(environment) == root / "cache"


def test_missing_appdata_raises_clear_error() -> None:
    with pytest.raises(PathConfigurationError):
        app_data_directory({})