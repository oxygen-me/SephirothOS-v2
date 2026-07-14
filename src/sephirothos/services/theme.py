"""Application theme and accent selection."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol

from PySide6.QtCore import QObject, Signal

from sephirothos.ui.metrics import UiMetrics
from sephirothos.ui.styles import (
    PURPLE_ACCENT_PALETTE,
    VOID_PALETTE,
    AccentPalette,
    ThemePalette,
    apply_accent_palette,
    build_application_stylesheet,
)


class ThemeId(StrEnum):
    VOID = "void"
    SATAN = "satan"
    RGB = "rgb"
    PISS = "piss"
    BISEXUAL = "bisexual"


class AccentId(StrEnum):
    PURPLE = "purple"
    BLUE = "blue"
    LIGHT_BLUE = "light-blue"
    TEAL = "teal"
    GREEN = "green"
    YELLOW = "yellow"
    ORANGE = "orange"
    RED = "red"


THEME_DISPLAY_NAMES: dict[ThemeId, str] = {
    ThemeId.VOID: "Void",
    ThemeId.SATAN: "Satan",
    ThemeId.RGB: "RGB",
    ThemeId.PISS: "Piss",
    ThemeId.BISEXUAL: "Bisexual",
}

ACCENT_DISPLAY_NAMES: dict[AccentId, str] = {
    AccentId.PURPLE: "Purple",
    AccentId.BLUE: "Blue",
    AccentId.LIGHT_BLUE: "Light Blue",
    AccentId.TEAL: "Teal",
    AccentId.GREEN: "Green",
    AccentId.YELLOW: "Yellow",
    AccentId.ORANGE: "Orange",
    AccentId.RED: "Red",
}


@dataclass(frozen=True, slots=True)
class ThemeDefinition:
    """Theme palette and its appearance capabilities."""

    palette: ThemePalette
    supports_custom_accent: bool = True


AVAILABLE_THEMES: dict[ThemeId, ThemeDefinition] = {
    ThemeId.VOID: ThemeDefinition(
        palette=VOID_PALETTE,
        supports_custom_accent=True,
    ),
}

AVAILABLE_ACCENTS: dict[AccentId, AccentPalette] = {
    AccentId.PURPLE: PURPLE_ACCENT_PALETTE,
}


class ThemeTarget(Protocol):
    """Object capable of receiving a Qt stylesheet."""

    def setStyleSheet(self, stylesheet: str) -> None:
        """Apply a Qt stylesheet."""


class ThemeError(ValueError):
    """Base exception for theme or accent selection failures."""


class UnknownThemeError(ThemeError):
    """Raised when a theme identifier is not recognized."""


class UnavailableThemeError(ThemeError):
    """Raised when a known theme does not yet have a palette."""


class UnknownAccentError(ThemeError):
    """Raised when an accent identifier is not recognized."""


class UnavailableAccentError(ThemeError):
    """Raised when a known accent does not yet have a palette."""


class ThemeService(QObject):
    """Own and apply the active SephirothOS theme and accent."""

    theme_changed = Signal(str)
    accent_changed = Signal(str)

    def __init__(
        self,
        target: ThemeTarget,
        metrics: UiMetrics,
        initial_theme: str | ThemeId = ThemeId.VOID,
        initial_accent: str | AccentId = AccentId.PURPLE,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)

        self._target = target
        self._metrics = metrics
        self._theme_id = self._validated_available_theme(
            initial_theme,
        )
        self._accent_id = self._validated_available_accent(
            initial_accent,
        )

    @property
    def theme_id(self) -> ThemeId:
        return self._theme_id

    @property
    def accent_id(self) -> AccentId:
        return self._accent_id

    @property
    def display_name(self) -> str:
        return THEME_DISPLAY_NAMES[self._theme_id]

    @property
    def accent_display_name(self) -> str:
        return ACCENT_DISPLAY_NAMES[self._accent_id]

    @property
    def known_themes(self) -> tuple[ThemeId, ...]:
        return tuple(ThemeId)

    @property
    def available_themes(self) -> tuple[ThemeId, ...]:
        return tuple(AVAILABLE_THEMES)

    @property
    def known_accents(self) -> tuple[AccentId, ...]:
        return tuple(AccentId)

    @property
    def available_accents(self) -> tuple[AccentId, ...]:
        return tuple(AVAILABLE_ACCENTS)

    @property
    def palette(self) -> ThemePalette:
        """Return the fully resolved active palette."""

        return resolve_palette(
            self._theme_id,
            self._accent_id,
        )

    def is_available(
        self,
        theme_id: str | ThemeId,
    ) -> bool:
        try:
            parsed = ThemeId(theme_id)
        except ValueError:
            return False

        return parsed in AVAILABLE_THEMES

    def is_accent_available(
        self,
        accent_id: str | AccentId,
    ) -> bool:
        try:
            parsed = AccentId(accent_id)
        except ValueError:
            return False

        return parsed in AVAILABLE_ACCENTS

    def apply_current(self) -> None:
        stylesheet = build_application_stylesheet(
            self.palette,
            self._metrics,
        )
        self._target.setStyleSheet(stylesheet)

    def set_theme(
        self,
        theme_id: str | ThemeId,
    ) -> bool:
        validated = self._validated_available_theme(
            theme_id,
        )

        if validated == self._theme_id:
            return False

        self._theme_id = validated
        self.apply_current()
        self.theme_changed.emit(self._theme_id.value)
        return True

    def set_accent(
        self,
        accent_id: str | AccentId,
    ) -> bool:
        validated = self._validated_available_accent(
            accent_id,
        )

        if validated == self._accent_id:
            return False

        self._accent_id = validated
        self.apply_current()
        self.accent_changed.emit(self._accent_id.value)
        return True

    @staticmethod
    def _validated_available_theme(
        theme_id: str | ThemeId,
    ) -> ThemeId:
        try:
            parsed = ThemeId(theme_id)
        except ValueError as error:
            raise UnknownThemeError(f"Unknown theme: {theme_id!r}.") from error

        if parsed not in AVAILABLE_THEMES:
            raise UnavailableThemeError(
                f"Theme {THEME_DISPLAY_NAMES[parsed]!r} does not have a palette yet."
            )

        return parsed

    @staticmethod
    def _validated_available_accent(
        accent_id: str | AccentId,
    ) -> AccentId:
        try:
            parsed = AccentId(accent_id)
        except ValueError as error:
            raise UnknownAccentError(f"Unknown accent: {accent_id!r}.") from error

        if parsed not in AVAILABLE_ACCENTS:
            raise UnavailableAccentError(
                f"Accent {ACCENT_DISPLAY_NAMES[parsed]!r} does not have a palette yet."
            )

        return parsed


def resolve_palette(
    theme_id: str | ThemeId,
    accent_id: str | AccentId,
) -> ThemePalette:
    """Resolve a complete palette for an available theme and accent."""

    parsed_theme = ThemeId(theme_id)
    parsed_accent = AccentId(accent_id)

    definition = AVAILABLE_THEMES[parsed_theme]

    if not definition.supports_custom_accent:
        return definition.palette

    return apply_accent_palette(
        definition.palette,
        AVAILABLE_ACCENTS[parsed_accent],
    )
