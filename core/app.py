# --- imports
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt

# --- create app class
class AppShell(QWidget):
    def __init__(self, lcn=None, config=None):
        super().__init__()

        # --- immediately store reference
        self.lcn = lcn
        lcn = self.lcn

        # --- set fullscreen by default
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.showFullScreen()

        # --- set main layout
        self.mainlayout = QVBoxLayout()
        self.mainlayout.setContentsMargins(0, 0, 0, 0)
        self.mainlayout.setSpacing(0)
        self.setLayout(self.mainlayout)