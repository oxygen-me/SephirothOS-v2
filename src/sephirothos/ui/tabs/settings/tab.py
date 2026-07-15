"""Settings tab."""

from PySide6.QtWidgets import (
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from sephirothos.config import AppearanceConfig
from sephirothos.ui.metrics import UiMetrics
from sephirothos.ui.roles import SurfaceRole
from sephirothos.ui.tabs.settings.navigation import (
    DEFAULT_SETTINGS_PAGE,
    SETTINGS_PAGE_ORDER,
    SettingsPageId,
)
from sephirothos.ui.tabs.settings.pages.appearance import (
    AppearancePage,
)
from sephirothos.ui.tabs.settings.pages.general import (
    GeneralPage,
)


class SettingsTab(QWidget):
    """Own the Settings tab's pages and page selection."""

    def __init__(
        self,
        metrics: UiMetrics,
        appearance: AppearanceConfig,
    ) -> None:
        super().__init__()

        self.metrics = metrics
        self.appearance = appearance

        self.setProperty(
            "surfaceRole",
            SurfaceRole.TRANSPARENT.value,
        )

        self._build_ui()
        self.set_active_page(DEFAULT_SETTINGS_PAGE)

    def _build_ui(self) -> None:
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.page_stack = QStackedWidget()
        self.page_stack.setProperty(
            "surfaceRole",
            SurfaceRole.TRANSPARENT.value,
        )

        self.appearance_page = AppearancePage(
            metrics=self.metrics,
            appearance=self.appearance,
        )

        self.pages: dict[SettingsPageId, QWidget] = {
            SettingsPageId.GENERAL: GeneralPage(
                metrics=self.metrics,
            ),
            SettingsPageId.APPEARANCE: self.appearance_page,
        }

        for page_id in SETTINGS_PAGE_ORDER:
            self.page_stack.addWidget(
                self.pages[page_id],
            )

        self.main_layout.addWidget(self.page_stack)

    def set_active_page(
        self,
        page_id: SettingsPageId,
    ) -> None:
        self.page_stack.setCurrentWidget(self.pages[page_id])
