"""Root SephirothOS application widget."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from sephirothos.config import AppConfig
from sephirothos.events import EventBus
from sephirothos.metadata import APPLICATION_NAME
from sephirothos.ui.metrics import UiMetrics
from sephirothos.ui.roles import SurfaceRole


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

        self.setObjectName("appShell")
        self.setWindowTitle(APPLICATION_NAME)

        self.setProperty("surfaceRole", SurfaceRole.BACKGROUND.value)

        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)

        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        placeholder = QLabel("SephirothOS alpha-1")
        placeholder.setObjectName("alphaPlaceholder")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(placeholder)
