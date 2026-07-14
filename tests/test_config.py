import json

import pytest

from sephirothos.config import (
    CURRENT_SCHEMA_VERSION,
    AppConfig,
    AppearanceConfig,
    ConfigStore,
    ConfigurationError,
)


def test_missing_configuration_creates_defaults(
    tmp_path,
) -> None:
    path = tmp_path / "config.json"
    store = ConfigStore(path)

    config = store.load()

    assert config == AppConfig()
    assert path.exists()


def test_configuration_round_trip(
    tmp_path,
) -> None:
    path = tmp_path / "config.json"
    store = ConfigStore(path)

    expected = AppConfig(
        username="Craig-John",
        onboarding_complete=True,
        appearance=AppearanceConfig(
            theme_id="void",
            accent_id="blue",
            display_scale=1.25,
            font_family="Segoe UI",
        ),
    )

    store.save(expected)

    assert store.load() == expected


def test_schema_one_configuration_is_migrated(
    tmp_path,
) -> None:
    path = tmp_path / "config.json"
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "username": "Brad",
                "theme_id": "void",
                "display_scale": 1.5,
                "onboarding_complete": True,
            }
        ),
        encoding="utf-8",
    )

    store = ConfigStore(path)
    config = store.load()

    assert config.schema_version == CURRENT_SCHEMA_VERSION
    assert config.username == "Brad"
    assert config.appearance.theme_id == "void"
    assert config.appearance.display_scale == 1.5
    assert config.appearance.accent_id == "purple"

    migrated_data = json.loads(path.read_text(encoding="utf-8"))

    assert migrated_data["schema_version"] == 2
    assert migrated_data["appearance"]["theme_id"] == "void"
    assert migrated_data["appearance"]["display_scale"] == 1.5
    assert "theme_id" not in migrated_data
    assert "display_scale" not in migrated_data


def test_invalid_json_raises_configuration_error(
    tmp_path,
) -> None:
    path = tmp_path / "config.json"
    path.write_text(
        "{invalid",
        encoding="utf-8",
    )

    store = ConfigStore(path)

    with pytest.raises(ConfigurationError):
        store.load()


def test_configuration_root_must_be_object(
    tmp_path,
) -> None:
    path = tmp_path / "config.json"
    path.write_text(
        "[]",
        encoding="utf-8",
    )

    store = ConfigStore(path)

    with pytest.raises(ConfigurationError):
        store.load()


def test_appearance_must_be_object() -> None:
    with pytest.raises(ConfigurationError):
        AppConfig.from_mapping(
            {
                "schema_version": 2,
                "appearance": [],
            }
        )


def test_boolean_is_not_accepted_as_display_scale() -> None:
    with pytest.raises(ConfigurationError):
        AppConfig.from_mapping(
            {
                "schema_version": 2,
                "appearance": {
                    "display_scale": True,
                },
            }
        )


def test_saved_configuration_is_readable_json(
    tmp_path,
) -> None:
    path = tmp_path / "config.json"
    store = ConfigStore(path)

    store.save(
        AppConfig(username="Brad"),
    )

    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["schema_version"] == 2
    assert data["username"] == "Brad"
    assert data["appearance"]["theme_id"] == "void"
    assert data["appearance"]["accent_id"] == "purple"
