"""Settings sidebar contents."""

from functools import partial

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from sephirothos.ui.metrics import UiMetrics
from sephirothos.ui.roles import (
    ButtonVariant,
    SurfaceRole,
    TextRole,
)
from sephirothos.ui.tabs.settings.navigation import (
    DEFAULT_SETTINGS_PAGE,
    SETTINGS_PAGE_LABELS,
    SETTINGS_PAGE_ORDER,
    SettingsPageId,
)


class SettingsBar(QWidget):
    """Navigation contents displayed inside the shell sidebar."""

    page_requested = Signal(object)

    def __init__(self, metrics: UiMetrics) -> None:
        super().__init__()

        self.metrics = metrics

        self.setProperty(
            "surfaceRole",
            SurfaceRole.TRANSPARENT.value,
        )

        self._build_ui()
        self.set_active_page(DEFAULT_SETTINGS_PAGE)

    def _build_ui(self) -> None:
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(
            self.metrics.space_10,
        )

        self.section_label = QLabel("Settings")
        self.section_label.setProperty(
            "textRole",
            TextRole.SECTION_TITLE.value,
        )

        self.page_button_group = QButtonGroup(self)
        self.page_button_group.setExclusive(True)

        self.page_buttons: dict[
            SettingsPageId,
            QPushButton,
        ] = {}

        self.main_layout.addWidget(self.section_label)

        for page_id in SETTINGS_PAGE_ORDER:
            button = QPushButton(
                SETTINGS_PAGE_LABELS[page_id],
            )
            button.setCheckable(True)
            button.setProperty(
                "buttonVariant",
                ButtonVariant.NAVIGATION.value,
            )
            button.clicked.connect(
                partial(
                    self._handle_page_button,
                    page_id,
                )
            )

            self.page_button_group.addButton(button)
            self.page_buttons[page_id] = button
            self.main_layout.addWidget(button)

        self.main_layout.addStretch()

    def _handle_page_button(
        self,
        page_id: SettingsPageId,
        _checked: bool = False,
    ) -> None:
        self.page_requested.emit(page_id)

    def set_active_page(
        self,
        page_id: SettingsPageId,
    ) -> None:
        self.page_buttons[page_id].setChecked(True)
