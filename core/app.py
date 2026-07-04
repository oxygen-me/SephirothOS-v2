# --- imports
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt

from utils.fun.headliners import window_names

import random

window_title = random.choice(window_names)

# --- create app class
class AppShell(QWidget):
    def __init__(self, cfgdata=None):
        super().__init__()

        # --- immediately store config
        self.config = cfgdata
        cfg = self.config

        # --- set title
        self.setWindowTitle(window_title)

        # --- set fullscreen by default
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.showFullScreen()

        # --- set theme
        self.setStyleSheet("background-color: #15161a;")

        # --- set main layout
        self.mainlayout = QVBoxLayout()
        self.mainlayout.setContentsMargins(20, 20, 20, 20)
        self.mainlayout.setSpacing(0)
        self.setLayout(self.mainlayout)

        # --- content area creation
        self.contentarea = QWidget()
        self.contentarea.setStyleSheet("background-color: #1f2024;")
        self.mainlayout.addWidget(self.contentarea)

        # --- content layout setup
        self.contentlayout = QVBoxLayout()
        self.contentlayout.setContentsMargins(0, 0, 0, 0)
        self.contentlayout.setSpacing(0)
        self.contentarea.setLayout(self.contentlayout)