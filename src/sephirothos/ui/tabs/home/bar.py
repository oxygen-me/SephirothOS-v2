"""Home sidebar."""

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from sephirothos.ui.metrics import UiMetrics
from sephirothos.ui.roles import SurfaceRole, TextRole


class HomeBar(QWidget):
    def __init__(self, metrics: UiMetrics) -> None:
        super().__init__()

        self.setProperty(
            "surfaceRole",
            SurfaceRole.PANEL.value,
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(metrics.space_10)

        title = QLabel("Home")
        title.setProperty(
            "textRole",
            TextRole.SECTION_TITLE.value,
        )

        layout.addWidget(title)
        layout.addStretch()
