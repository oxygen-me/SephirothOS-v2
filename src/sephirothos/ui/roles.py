"""Semantic UI styling roles."""

from enum import StrEnum


class SurfaceRole(StrEnum):
    BACKGROUND = "background"
    CHROME = "chrome"
    PANEL = "panel"
    CARD = "card"
    TRANSPARENT = "transparent"
    OUTLINED = "outlined"
    ACCENT_OUTLINED = "accent-outlined"


class ButtonVariant(StrEnum):
    NAVIGATION = "navigation"
    SECONDARY = "secondary"
    SELECTABLE = "selectable"
    CARD_ACTION = "card-action"
    PRIMARY = "primary"
    ACCENT_OUTLINE = "accent-outline"
    THEME_OPTION = "theme-option"
    LINK = "link"


class TextRole(StrEnum):
    PAGE_TITLE = "page-title"
    PAGE_SUBTITLE = "page-subtitle"
    CARD_TITLE = "card-title"
    CAPTION = "caption"
    BODY = "body"
    BODY_MUTED = "body-muted"
    USERNAME = "username"
    SECTION_TITLE = "section-title"
    SECTION_CAPTION = "section-caption"
    WELCOME_TITLE = "welcome-title"
    WELCOME_TITLE_ACCENT = "welcome-title-accent"
    WELCOME_SUBTITLE = "welcome-subtitle"
    WELCOME_BODY = "welcome-body"
    WELCOME_PAGE_TITLE = "welcome-page-title"
    WELCOME_PAGE_SUBTITLE = "welcome-page-subtitle"
    ACCENT_SUBTITLE = "accent-subtitle"
    ACCENT_BODY = "accent-body"


class Tone(StrEnum):
    ACCENT = "accent"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


class ProgressRole(StrEnum):
    DEFAULT = "default"


class ProgressVariant(StrEnum):
    CPU = "cpu"
    MEMORY = "memory"
    DISK = "disk"
    PISS = "piss"


class DividerRole(StrEnum):
    DEFAULT = "default"
    STRONG = "strong"


class IndicatorRole(StrEnum):
    DEFAULT_CIRCLE = "default-circle"
    ACCENT_CIRCLE = "accent-circle"


class ScrollRole(StrEnum):
    DEFAULT = "default"


class InputRole(StrEnum):
    SEARCH = "search"
    EDITOR = "editor"
    COMBO = "combo"
    SCALE = "scale"


class TableRole(StrEnum):
    DEFAULT = "default"


class CheckRole(StrEnum):
    DEFAULT = "default"
