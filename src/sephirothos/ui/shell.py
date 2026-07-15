"""Root SephirothOS application widget."""

from __future__ import annotations

from dataclasses import dataclass
from functools import partial
from random import choice

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from sephirothos.config import AppConfig
from sephirothos.content.window_titles import WINDOW_TITLES
from sephirothos.events import EventBus
from sephirothos.ui.metrics import UiMetrics
from sephirothos.ui.roles import ButtonVariant, DividerRole, SurfaceRole, TextRole
from sephirothos.ui.tabs.apps.bar import AppsBar
from sephirothos.ui.tabs.apps.tab import AppsTab
from sephirothos.ui.tabs.cli.bar import CliBar
from sephirothos.ui.tabs.cli.tab import CliTab
from sephirothos.ui.tabs.home.bar import HomeBar
from sephirothos.ui.tabs.home.tab import HomeTab
from sephirothos.ui.tabs.navigation import (
    DEFAULT_TAB,
    TAB_LABELS,
    TAB_ORDER,
    TabId,
)
from sephirothos.ui.tabs.settings.bar import SettingsBar
from sephirothos.ui.tabs.settings.tab import SettingsTab


@dataclass(frozen=True, slots=True)
class TabPair:
    """Widgets associated with one primary tab."""

    bar: QWidget
    tab: QWidget


class AppShell(QWidget):
    """Root widget containing the SephirothOS interface."""

    def __init__(
        self,
        config: AppConfig,
        event_bus: EventBus,
        metrics: UiMetrics,
    ) -> None:
        super().__init__()

        self.config = config
        self.event_bus = event_bus
        self.metrics = metrics

        self.tab_pairs: dict[TabId, TabPair] = {}
        self.tab_buttons: dict[TabId, QPushButton] = {}
        self.current_tab: TabId | None = None

        self.setWindowTitle(choice(WINDOW_TITLES))
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)
        self.setProperty(
            "surfaceRole",
            SurfaceRole.BACKGROUND.value,
        )

        self._build_shell()
        self._register_tabs()
        self._build_top_navigation()
        self.set_active_tab(DEFAULT_TAB)

    def _build_shell(self) -> None:
        """Construct the persistent shell regions."""

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self._build_top_bar()
        self._build_workspace()

        self.main_layout.addWidget(self.top_bar)
        self.main_layout.addWidget(self.workspace, 1)

    def _build_top_bar(self) -> None:
        """Construct the persistent primary navigation bar."""

        self.top_bar = QWidget()
        self.top_bar.setObjectName("topBar")
        self.top_bar.setProperty(
            "surfaceRole",
            SurfaceRole.CHROME.value,
        )
        self.top_bar.setFixedHeight(
            self.metrics.top_bar_height,
        )

        self.top_bar_layout = QHBoxLayout(self.top_bar)
        self.top_bar_layout.setContentsMargins(
            self.metrics.space_10,
            self.metrics.space_10,
            self.metrics.space_10,
            self.metrics.space_10,
        )
        self.top_bar_layout.setSpacing(self.metrics.space_20)

        self.tab_button_group = QButtonGroup(self)
        self.tab_button_group.setExclusive(True)

    def _build_workspace(self) -> None:
        """Construct the sidebar and tab-content workspace."""

        self.workspace = QWidget()
        self.workspace.setObjectName("workspace")
        self.workspace.setProperty(
            "surfaceRole",
            SurfaceRole.BACKGROUND.value,
        )

        self.workspace_layout = QHBoxLayout(self.workspace)
        self.workspace_layout.setContentsMargins(
            self.metrics.space_20,
            self.metrics.space_20,
            self.metrics.space_20,
            self.metrics.space_20,
        )
        self.workspace_layout.setSpacing(self.metrics.space_20)

        self._build_sidebar()
        self._build_content_area()

        self.workspace_layout.addWidget(self.sidebar)
        self.workspace_layout.addWidget(
            self.content_stack,
            1,
        )

    def _build_sidebar(self) -> None:
        """Construct the persistent sidebar and changing bar area."""

        self.sidebar = QWidget()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setProperty(
            "surfaceRole",
            SurfaceRole.PANEL.value,
        )
        self.sidebar.setFixedWidth(self.metrics.sidebar_width)

        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(
            self.metrics.space_20,
            self.metrics.space_20,
            self.metrics.space_20,
            self.metrics.space_20,
        )
        self.sidebar_layout.setSpacing(0)

        self._build_sidebar_header()

        self.bar_stack = QStackedWidget()
        self.bar_stack.setObjectName("barStack")
        self.bar_stack.setProperty(
            "surfaceRole",
            SurfaceRole.TRANSPARENT.value,
        )

        self.sidebar_layout.addSpacing(
            self.metrics.space_20,
        )
        self.sidebar_layout.addWidget(
            self.bar_stack,
            1,
        )

    def _build_sidebar_header(self) -> None:
        """Construct the static sidebar header."""

        self.username_label = QLabel(
            self.config.username,
        )
        self.username_label.setProperty(
            "textRole",
            TextRole.USERNAME.value,
        )

        self.subtitle_label = QLabel("Veni, veni, venias, ne me mori facias.")
        self.subtitle_label.setProperty(
            "textRole",
            TextRole.CAPTION.value,
        )
        self.subtitle_label.setWordWrap(True)

        self.header_divider = QFrame()
        self.header_divider.setObjectName("sidebarHeaderDivider")
        self.header_divider.setFrameShape(
            QFrame.Shape.NoFrame,
        )
        self.header_divider.setProperty(
            "dividerRole",
            DividerRole.DEFAULT.value,
        )
        self.header_divider.setFixedHeight(
            self.metrics.border_thin,
        )

        self.sidebar_layout.addWidget(
            self.username_label,
        )
        self.sidebar_layout.addSpacing(
            self.metrics.space_10,
        )
        self.sidebar_layout.addWidget(
            self.subtitle_label,
        )
        self.sidebar_layout.addSpacing(
            self.metrics.space_20,
        )
        self.sidebar_layout.addWidget(
            self.header_divider,
        )

    def _build_content_area(self) -> None:
        """Construct the changing primary tab area."""

        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName(
            "contentStack",
        )
        self.content_stack.setProperty(
            "surfaceRole",
            SurfaceRole.PANEL.value,
        )

    def _register_tabs(self) -> None:
        """Create and register every primary tab/bar pair."""

        home_bar = HomeBar(self.metrics)
        home_tab = HomeTab(self.metrics)

        settings_bar = SettingsBar(self.metrics)
        settings_tab = SettingsTab(
            self.metrics,
            self.config.appearance,
        )

        settings_tab.appearance_page.apply_requested.connect(
            self.event_bus.appearance_apply_requested.emit,
        )
        self.event_bus.appearance_applied.connect(
            settings_tab.appearance_page.mark_applied,
        )
        self.event_bus.appearance_apply_failed.connect(
            settings_tab.appearance_page.mark_apply_failed,
        )

        home_bar.page_requested.connect(
            home_tab.set_active_page,
        )
        settings_bar.page_requested.connect(
            settings_tab.set_active_page,
        )

        self.tab_pairs = {
            TabId.HOME: TabPair(
                bar=home_bar,
                tab=home_tab,
            ),
            TabId.APPS: TabPair(
                bar=AppsBar(self.metrics),
                tab=AppsTab(self.metrics),
            ),
            TabId.SETTINGS: TabPair(
                bar=settings_bar,
                tab=settings_tab,
            ),
            TabId.CLI: TabPair(
                bar=CliBar(self.metrics),
                tab=CliTab(self.metrics),
            ),
        }

        for tab_id in TAB_ORDER:
            pair = self.tab_pairs[tab_id]

            self.bar_stack.addWidget(pair.bar)
            self.content_stack.addWidget(pair.tab)

    def _build_top_navigation(self) -> None:
        """Create the top-level tab buttons."""

        for tab_id in TAB_ORDER:
            button = QPushButton(TAB_LABELS[tab_id])
            button.setObjectName(f"{tab_id.value}TabButton")
            button.setCheckable(True)
            button.setProperty(
                "buttonVariant",
                ButtonVariant.NAVIGATION.value,
            )

            button.clicked.connect(
                partial(
                    self._handle_tab_button,
                    tab_id,
                )
            )

            self.tab_button_group.addButton(button)
            self.tab_buttons[tab_id] = button

            # Equal stretch gives each primary tab an equal
            # portion of the top bar.
            self.top_bar_layout.addWidget(
                button,
                1,
            )

    def _handle_tab_button(
        self,
        tab_id: TabId,
        _checked: bool = False,
    ) -> None:
        """Handle a top-level navigation-button click."""

        self.set_active_tab(tab_id)

    def set_active_tab(
        self,
        tab_id: TabId,
    ) -> None:
        """Display the bar and content registered to a tab."""

        pair = self.tab_pairs[tab_id]

        self.bar_stack.setCurrentWidget(pair.bar)
        self.content_stack.setCurrentWidget(pair.tab)
        self.tab_buttons[tab_id].setChecked(True)

        self.current_tab = tab_id
