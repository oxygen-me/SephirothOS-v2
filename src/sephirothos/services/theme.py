"""Application theme selection and application."""

from __future__ import annotations

from enum import StrEnum
from typing import Protocol

from PySide6.QtCore import QObject, Signal

from sephirothos.services.display_scale import DisplayScaleService
from sephirothos.ui.styles import (
    VOID_PALETTE,
    ThemePalette,
    build_application_stylesheet,
)


class ThemeId(StrEnum):
    VOID = "void"
    SATAN = "satan"
    RGB = "rgb"
    PISS = "piss"
    BISEXUAL = "bisexual"


THEME_DISPLAY_NAMES: dict[ThemeId, str] = {
    ThemeId.VOID: "Void",
    ThemeId.SATAN: "Satan",
    ThemeId.RGB: "RGB",
    ThemeId.PISS: "Piss",
    ThemeId.BISEXUAL: "Bisexual",
}

AVAILABLE_PALETTES: dict[ThemeId, ThemePalette] = {
    ThemeId.VOID: VOID_PALETTE,
}


class ThemeTarget(Protocol):
    """Object capable of receiving a Qt stylesheet."""

    def setStyleSheet(self, stylesheet: str) -> None:
        """Apply a Qt stylesheet."""


class ThemeError(ValueError):
    """Base exception for theme selection failures."""


class UnknownThemeError(ThemeError):
    """Raised when a theme identifier is not recognized."""


class UnavailableThemeError(ThemeError):
    """Raised when a known theme does not yet have a palette."""


class ThemeService(QObject):
    """Own and apply the active SephirothOS theme."""

    theme_changed = Signal(str)

    def __init__(
        self,
        target: ThemeTarget,
        display_scale: DisplayScaleService,
        initial_theme: str | ThemeId = ThemeId.VOID,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)

        self._target = target
        self._display_scale = display_scale
        self._theme_id = self._validated_available_theme(initial_theme)

        self._display_scale.scale_changed.connect(self._handle_scale_change)

    @property
    def theme_id(self) -> ThemeId:
        return self._theme_id

    @property
    def display_name(self) -> str:
        return THEME_DISPLAY_NAMES[self._theme_id]

    @property
    def known_themes(self) -> tuple[ThemeId, ...]:
        return tuple(ThemeId)

    @property
    def available_themes(self) -> tuple[ThemeId, ...]:
        return tuple(AVAILABLE_PALETTES)

    def is_available(self, theme_id: str | ThemeId) -> bool:
        try:
            parsed = ThemeId(theme_id)
        except ValueError:
            return False

        return parsed in AVAILABLE_PALETTES

    def apply_current(self) -> None:
        palette = AVAILABLE_PALETTES[self._theme_id]
        stylesheet = build_application_stylesheet(
            palette,
            self._display_scale,
        )
        self._target.setStyleSheet(stylesheet)

    def set_theme(self, theme_id: str | ThemeId) -> bool:
        validated = self._validated_available_theme(theme_id)

        if validated == self._theme_id:
            return False

        self._theme_id = validated
        self.apply_current()
        self.theme_changed.emit(self._theme_id.value)
        return True

    def _handle_scale_change(self, _factor: float) -> None:
        self.apply_current()

    @staticmethod
    def _validated_available_theme(
        theme_id: str | ThemeId,
    ) -> ThemeId:
        try:
            parsed = ThemeId(theme_id)
        except ValueError as error:
            raise UnknownThemeError(f"Unknown theme: {theme_id!r}.") from error

        if parsed not in AVAILABLE_PALETTES:
            raise UnavailableThemeError(
                f"Theme {THEME_DISPLAY_NAMES[parsed]!r} does not have a palette yet."
            )

        return parsed
