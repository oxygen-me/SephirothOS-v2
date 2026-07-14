"""General settings page."""

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from sephirothos.ui.metrics import UiMetrics
from sephirothos.ui.roles import SurfaceRole, TextRole


class GeneralPage(QWidget):
    """Display general application settings."""

    def __init__(
        self,
        metrics: UiMetrics,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.setProperty(
            "surfaceRole",
            SurfaceRole.TRANSPARENT.value,
        )

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(
            metrics.space_20,
            metrics.space_20,
            metrics.space_20,
            metrics.space_20,
        )
        self.main_layout.setSpacing(metrics.space_20)

        self.title_label = QLabel("General")
        self.title_label.setProperty(
            "textRole",
            TextRole.PAGE_TITLE.value,
        )

        self.main_layout.addWidget(self.title_label)
        self.main_layout.addStretch()
