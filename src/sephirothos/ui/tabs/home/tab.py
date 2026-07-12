"""Home tab."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from sephirothos.ui.metrics import UiMetrics
from sephirothos.ui.roles import SurfaceRole, TextRole


class HomeTab(QWidget):
    def __init__(self, metrics: UiMetrics) -> None:
        super().__init__()

        self.setProperty(
            "surfaceRole",
            SurfaceRole.TRANSPARENT.value,
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            metrics.space_20,
            metrics.space_20,
            metrics.space_20,
            metrics.space_20,
        )
        layout.setSpacing(metrics.space_20)

        title = QLabel("Home")
        title.setProperty(
            "textRole",
            TextRole.PAGE_TITLE.value,
        )
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title)
