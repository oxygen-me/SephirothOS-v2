"""SephirothOS application composition and lifecycle."""

from __future__ import annotations

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication

from sephirothos.config import AppConfig, ConfigStore
from sephirothos.events import EventBus
from sephirothos.metadata import (
    APPLICATION_NAME,
    ORGANIZATION_NAME,
    VERSION,
)
from sephirothos.services.display_scale import DisplayScaleService
from sephirothos.services.theme import ThemeService
from sephirothos.ui.metrics import UiMetrics
from sephirothos.ui.shell import AppShell


class SephirothApplication:
    """Construct and own the SephirothOS runtime."""

    def __init__(
        self,
        arguments: list[str],
        config_store: ConfigStore | None = None,
    ) -> None:
        self.qt_application = QApplication(arguments)
        self._configure_metadata()

        self.config_store = config_store or ConfigStore()
        self.config = self.config_store.load()

        self.event_bus = EventBus()
        self.display_scale = self._create_display_scale(self.config)
        self.metrics = UiMetrics.from_scale(self.display_scale)

        self.theme = ThemeService(
            target=self.qt_application,
            metrics=self.metrics,
            initial_theme=self.config.theme_id,
        )

        self.shell = AppShell(
            config=self.config,
            event_bus=self.event_bus,
            metrics=self.metrics,
        )

        self._connect_events()
        self.theme.apply_current()

    def run(self) -> int:
        """Show the shell and enter the Qt event loop."""

        self.shell.showFullScreen()
        return self.qt_application.exec_()

    def _configure_metadata(self) -> None:
        QCoreApplication.setApplicationName(APPLICATION_NAME)
        QCoreApplication.setApplicationVersion(VERSION)
        QCoreApplication.setOrganizationName(ORGANIZATION_NAME)

    def _connect_events(self) -> None:
        self.event_bus.quit_requested.connect(
            self.qt_application.quit,
        )

    @staticmethod
    def _create_display_scale(config: AppConfig) -> DisplayScaleService:
        return DisplayScaleService(config.display_scale)
