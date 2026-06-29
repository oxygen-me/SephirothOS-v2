# --- imports
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt

# --- create app class
class AppShell(QWidget):
    def __init__(self, lcn=None, config=None):
        super().__init__()

        # --- immediately store reference
        self.config = config
        cfg = self.config

        # --- set fullscreen by default
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.showFullScreen()