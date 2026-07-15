"""SephirothOS application composition and lifecycle."""

from __future__ import annotations

import logging
import math
from dataclasses import replace

from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication

from sephirothos.config import (
    AppConfig,
    AppearanceConfig,
    ConfigStore,
    ConfigurationError,
)
from sephirothos.events import EventBus
from sephirothos.logging_config import configure_logging
from sephirothos.metadata import (
    APPLICATION_NAME,
    ORGANIZATION_NAME,
    VERSION,
)
from sephirothos.services.background_music import BackgroundMusicPlayer
from sephirothos.services.display_scale import DisplayScaleService
from sephirothos.services.theme import ThemeService
from sephirothos.ui.metrics import UiMetrics
from sephirothos.ui.shell import AppShell

logger = logging.getLogger(__name__)


class SephirothApplication:
    """Construct and own the SephirothOS runtime."""

    def __init__(
        self,
        arguments: list[str],
        config_store: ConfigStore | None = None,
    ) -> None:
        self.log_path = configure_logging()
        logger.info("Starting SephirothOS %s", VERSION)

        self.qt_application = QApplication(arguments)
        self._configure_metadata()

        self.config_store = config_store or ConfigStore()
        self.config = self.config_store.load()

        logger.info(
            "Loaded configuration with theme=%s accent=%s scale=%.2f font=%s",
            self.config.appearance.theme_id,
            self.config.appearance.accent_id,
            self.config.appearance.display_scale,
            self.config.appearance.font_family,
        )

        self._configure_font()

        self.event_bus = EventBus()
        self.display_scale = self._create_display_scale(self.config)
        self.metrics = UiMetrics.from_scale(self.display_scale)

        self.theme = ThemeService(
            target=self.qt_application,
            metrics=self.metrics,
            initial_theme=self.config.appearance.theme_id,
            initial_accent=self.config.appearance.accent_id,
        )

        self.shell = AppShell(
            config=self.config,
            event_bus=self.event_bus,
            metrics=self.metrics,
        )

        self.background_music = BackgroundMusicPlayer(
            parent=self.qt_application,
        )
        self.qt_application.aboutToQuit.connect(
            self.background_music.stop,
        )

        self._connect_events()
        self.theme.apply_current()

        logger.info("Application runtime initialized")

    def run(self) -> int:
        """Show the shell and enter the Qt event loop."""

        logger.info("Showing fullscreen application shell")
        self.shell.showFullScreen()

        self.background_music.play()

        exit_code = self.qt_application.exec()

        logger.info("Application exited with code %d", exit_code)
        return exit_code

    def _configure_metadata(self) -> None:
        QCoreApplication.setApplicationName(APPLICATION_NAME)
        QCoreApplication.setApplicationVersion(VERSION)
        QCoreApplication.setOrganizationName(ORGANIZATION_NAME)

    def _connect_events(self) -> None:
        self.event_bus.quit_requested.connect(
            self.qt_application.quit,
        )
        self.event_bus.appearance_apply_requested.connect(
            self._apply_appearance,
        )

    @staticmethod
    def _create_display_scale(
        config: AppConfig,
    ) -> DisplayScaleService:
        return DisplayScaleService(
            config.appearance.display_scale,
        )

    def _configure_font(self) -> None:
        """Configure the default Qt application font."""

        font_family = self.config.appearance.font_family

        self.qt_application.setFont(
            QFont(font_family),
        )

        logger.info(
            "Configured application font family=%s",
            font_family,
        )

    def _apply_appearance(
        self,
        appearance: AppearanceConfig,
    ) -> None:
        """Persist and apply an appearance draft."""

        previous_appearance = self.config.appearance
        applied = replace(appearance)

        try:
            self.config.appearance = applied
            self.config_store.save(self.config)

        except ConfigurationError:
            self.config.appearance = previous_appearance

            logger.exception("Could not save appearance configuration")
            self.event_bus.appearance_apply_failed.emit("Could not save appearance settings.")
            return

        restart_required = not math.isclose(
            self.display_scale.factor,
            applied.display_scale,
        )

        self.qt_application.setFont(
            QFont(applied.font_family),
        )

        theme_changed = self.theme.set_theme(
            applied.theme_id,
        )
        accent_changed = self.theme.set_accent(
            applied.accent_id,
        )

        if not theme_changed and not accent_changed:
            # Reapply the stylesheet after changing the application font.
            self.theme.apply_current()

        logger.info(
            "Applied appearance theme=%s accent=%s scale=%.2f font=%s restart_required=%s",
            applied.theme_id,
            applied.accent_id,
            applied.display_scale,
            applied.font_family,
            restart_required,
        )

        self.event_bus.appearance_applied.emit(
            replace(applied),
            restart_required,
        )
