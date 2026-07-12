"""Priamry SephirothOS tab identities."""

from enum import StrEnum


class TabId(StrEnum):
    HOME = "home"
    APPS = "apps"
    SETTINGS = "settings"
    CLI = "cli"


TAB_LABELS: dict[TabId, str] = {
    TabId.HOME: "Home",
    TabId.APPS: "Apps",
    TabId.SETTINGS: "Settings",
    TabId.CLI: "CLI",
}

TAB_ORDER: tuple[TabId, ...] = (
    TabId.HOME,
    TabId.APPS,
    TabId.SETTINGS,
    TabId.CLI,
)

DEFAULT_TAB = TabId.HOME
