# --- imports
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt

# --- create app class
class AppShell(QWidget):
    def __init__(self, config=None):
        super().__init__()

        # --- set fullscreen by default
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.showFullScreen()

        # --- set main layout
        self.mainlayout = QVBoxLayout()
        self.mainlayout.setContentsMargins(0, 0, 0, 0)
        self.mainlayout.setSpacing(0)
        self.setLayout(self.mainlayout)