"""Settings tab page identities."""

from enum import StrEnum


class SettingsPageId(StrEnum):
    GENERAL = "general"
    APPEARANCE = "appearance"


SETTINGS_PAGE_LABELS: dict[SettingsPageId, str] = {
    SettingsPageId.GENERAL: "General",
    SettingsPageId.APPEARANCE: "Appearance",
}

SETTINGS_PAGE_ORDER: tuple[SettingsPageId, ...] = (
    SettingsPageId.GENERAL,
    SettingsPageId.APPEARANCE,
)

DEFAULT_SETTINGS_PAGE = SettingsPageId.GENERAL
