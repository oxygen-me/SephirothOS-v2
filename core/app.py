# --- imports
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
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
        self.setStyleSheet("background-color: #15161a; border-radius: 0px;")

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
        self.contentlayout.setContentsMargins(20, 20, 20, 20)
        self.contentlayout.setSpacing(0)
        self.contentarea.setLayout(self.contentlayout)

        # --- topbar
        self.topbar = QWidget()
        self.topbar.setStyleSheet("background-color: #15161a;")

        # --- topbar layout
        self.topbarlayout = QHBoxLayout()
        self.topbarlayout.setContentsMargins(10, 10, 10, 10)
        self.topbarlayout.setSpacing(0)

        # --- title label
        self.toptitle = QLabel("SephirothOS")
        self.toptitle.setStyleSheet("background-color: transparent; color: white; font-family: Segoe UI; font-size: 24px; font-weight: 650;")

        # --- buttons
        self.homebtn = QPushButton("Home")
        self.homebtn.setStyleSheet("""
                QPushButton { background-color: #15161a; color: white; font-family: Segoe UI; font-size: 16px; }
                QPushButton:hover {}
                QPushButton:pressed {}
                """)

        self.appsbtn = QPushButton("Apps")
        self.appsbtn.setStyleSheet("""
                QPushButton { background-color: #15161a; color: white; font-family: Segoe UI; font-size: 16px; }
                QPushButton:hover {}
                QPushButton:pressed {}
                """)

        self.settingsbtn = QPushButton("Settings")
        self.settingsbtn.setStyleSheet("""
                QPushButton { background-color: #15161a; color: white; font-family: Segoe UI; font-size: 16px; }
                QPushButton:hover {}
                QPushButton:pressed {}
                """)

        self.clibtn = QPushButton("CLI")
        self.clibtn.setStyleSheet("""
                QPushButton { background-color: #15161a; color: white; font-family: Segoe UI; font-size: 16px; }
                QPushButton:hover {}
                QPushButton:pressed {}
                """)

        # --- assemble
        self.topbar.setLayout(self.topbarlayout)
        self.topbarlayout.addWidget(self.toptitle)
        self.topbarlayout.addSpacing(60)

        self.topbarlayout.addWidget(self.homebtn)
        self.topbarlayout.addSpacing(30)
        self.topbarlayout.addWidget(self.appsbtn)
        self.topbarlayout.addSpacing(30)
        self.topbarlayout.addWidget(self.settingsbtn)
        self.topbarlayout.addSpacing(30)
        self.topbarlayout.addWidget(self.clibtn)

        self.topbarlayout.addStretch()

        self.contentlayout.addWidget(self.topbar)
        self.contentlayout.addStretch()