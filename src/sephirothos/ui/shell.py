"""Root SephirothOS application widget."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from sephirothos.config import AppConfig
from sephirothos.events import EventBus
from sephirothos.metadata import APPLICATION_NAME


class AppShell(QWidget):
    """Root widget containing the SephirothOS interface."""

    def __init__(
        self,
        config: AppConfig,
        event_bus: EventBus,
    ) -> None:
        super().__init__()

        self.config = config
        self.event_bus = event_bus

        self.setObjectName("appShell")
        self.setWindowTitle(APPLICATION_NAME)
        self.resize(1100, 700)

        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)

        placeholder = QLabel("SephirothOS alpha-1")
        placeholder.setObjectName("alphaPlaceholder")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(placeholder)
