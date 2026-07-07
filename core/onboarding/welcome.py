# --- imports
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout, QPushButton, QLineEdit, \
    QComboBox
from PySide6.QtCore import Qt

from eventbus import mainBus

from pathlib import Path

import assets.resource_rc as resources_rc

import json
import os

config_path = Path(str(os.getenv('APPDATA'))) / 'SephirothOS' / 'config.json'
license_path = Path(str(os.getenv('APPDATA'))) / 'SephirothOS' / 'license.json'


# --- globaL vars
username1 = ""

# --- create onboarding class
class WelcomeWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("A Greeting Letter From Sephiroth")

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

        # --- stack
        self.stack = QStackedWidget()
        self.contentlayout.addWidget(self.stack)

        self.stack.addWidget(WelcomePage(self.stack))
        self.stack.addWidget(LanguagePage(self.stack))
        self.stack.addWidget(ThemePage(self.stack))
        self.stack.addWidget(AccountPage(self.stack))
        self.stack.addWidget(SettingsPage(self.stack))
        self.stack.addWidget(FinishPage(self.stack))

        self.stack.setCurrentIndex(0)