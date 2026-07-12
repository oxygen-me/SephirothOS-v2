import json

import pytest
from sephirothos.config import (
    AppConfig,
    ConfigurationError,
    ConfigStore,
)


def test_missing_configuration_creates_defaults(tmp_path) -> None:
    path = tmp_path / "config.json"
    store = ConfigStore(path)

    config = store.load()

    assert config == AppConfig()
    assert path.exists()


def test_configuration_round_trip(tmp_path) -> None:
    path = tmp_path / "config.json"
    store = ConfigStore(path)

    expected = AppConfig(
        username="Craig-John",
        theme_id="void",
        display_scale=1.25,
        onboarding_complete=True,
    )

    store.save(expected)

    assert store.load() == expected


def test_invalid_json_raises_configuration_error(tmp_path) -> None:
    path = tmp_path / "config.json"
    path.write_text("{invalid", encoding="utf-8")

    store = ConfigStore(path)

    with pytest.raises(ConfigurationError):
        store.load()


def test_configuration_root_must_be_object(tmp_path) -> None:
    path = tmp_path / "config.json"
    path.write_text("[]", encoding="utf-8")

    store = ConfigStore(path)

    with pytest.raises(ConfigurationError):
        store.load()


def test_boolean_is_not_accepted_as_display_scale(tmp_path) -> None:
    with pytest.raises(ConfigurationError):
        AppConfig.from_mapping({"display_scale": True})


def test_saved_configuration_is_readable_json(tmp_path) -> None:
    path = tmp_path / "config.json"
    store = ConfigStore(path)

    store.save(AppConfig(username="Brad"))

    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["schema_version"] == 1
    assert data["username"] == "Brad"
