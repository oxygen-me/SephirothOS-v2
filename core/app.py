# --- general imports
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QSizePolicy, \
    QStackedWidget
from PySide6.QtCore import Qt
from utils.fun.headliners import window_names
import random

# --- get window title
window_title = random.choice(window_names)

# --- extra vars
default_btn_qss = """
                QPushButton { background-color: #15161a; color: white; font-family: Segoe UI; font-size: 16px; padding-top: 10px; padding-bottom: 10px; }
                QPushButton:hover { background-color: #1a1b20; }
                QPushButton:pressed { background-color: #0e0f12 }
                """

selected_btn_qss = "background-color: #0e0f12; color: white; font-family: Segoe UI; font-size: 16px; padding-top: 10px; padding-bottom: 10px;"

# --- page imports
from ui.home import HomePage
from ui.applications import AppsPage
from ui.settings import SettingsPage
from ui.cli import CLIPage

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
        self.contentlayout.setSpacing(20)
        self.contentarea.setLayout(self.contentlayout)

        # --- topbar
        self.topbar = QWidget()
        self.topbar.setStyleSheet("background-color: #15161a;")

        # --- topbar layout
        self.topbarlayout = QHBoxLayout()
        self.topbarlayout.setContentsMargins(0, 0, 0, 0)
        self.topbarlayout.setSpacing(0)

        # --- buttons
        self.homebtn = QPushButton("Home")
        self.homebtn.setStyleSheet(selected_btn_qss)
        self.homebtn.clicked.connect(self.switch_to_home)

        self.appsbtn = QPushButton("Apps")
        self.appsbtn.setStyleSheet(default_btn_qss)
        self.appsbtn.clicked.connect(self.switch_to_apps)

        self.settingsbtn = QPushButton("Settings")
        self.settingsbtn.setStyleSheet(default_btn_qss)
        self.settingsbtn.clicked.connect(self.switch_to_settings)

        self.clibtn = QPushButton("CLI")
        self.clibtn.setStyleSheet(default_btn_qss)
        self.clibtn.clicked.connect(self.switch_to_cli)

        # --- arealayout
        self.arealayout = QHBoxLayout()
        self.arealayout.setContentsMargins(0, 0, 0, 0)
        self.arealayout.setSpacing(20)

        # --- sidebar
        self.sidebar = QWidget()
        self.sidebar.setStyleSheet("background-color: #15161a;")

        # --- sidebar layout
        self.sidebarlayout = QVBoxLayout()
        self.sidebarlayout.setContentsMargins(10, 10, 10, 10)
        self.sidebarlayout.setSpacing(0)
        self.sidebar.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        # --- weather
        self.weatherlabel = QLabel("Super Cool Weather")
        self.weatherlabel.setStyleSheet("background-color: transparent; color: #15161a; font-family: Segoe UI; font-size: 24px; font-weight: 400;")

        # --- mainarea
        self.mainarea = QWidget()
        self.mainarea.setStyleSheet("background-color: #15161a;")
        self.mainarea.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # --- stackarea
        self.stackarea = QVBoxLayout()
        self.stackarea.setContentsMargins(0, 0, 0, 0)
        self.stackarea.setSpacing(0)

        # --- assemble
        self.topbar.setLayout(self.topbarlayout)
        self.topbarlayout.addWidget(self.homebtn)
        self.topbarlayout.addWidget(self.appsbtn)
        self.topbarlayout.addWidget(self.settingsbtn)
        self.topbarlayout.addWidget(self.clibtn)

        self.sidebar.setLayout(self.sidebarlayout)
        self.sidebarlayout.addWidget(self.weatherlabel)
        self.sidebarlayout.addStretch()

        self.contentlayout.addWidget(self.topbar)

        self.contentlayout.addLayout(self.arealayout)
        self.arealayout.addWidget(self.sidebar)
        self.arealayout.addWidget(self.mainarea)

        self.mainarea.setLayout(self.stackarea)

        # --- stack
        self.stack = QStackedWidget()

        self.stack.addWidget(HomePage(self.stack))
        self.stack.addWidget(AppsPage(self.stack))
        self.stack.addWidget(SettingsPage(self.stack))
        self.stack.addWidget(CLIPage(self.stack))

        self.stack.setCurrentIndex(0)

        self.stackarea.addWidget(self.stack)

    # --- create button methods
    def switch_to_home(self):
        self.stack.setCurrentIndex(0)

        self.homebtn.setStyleSheet(selected_btn_qss)
        self.appsbtn.setStyleSheet(default_btn_qss)
        self.settingsbtn.setStyleSheet(default_btn_qss)
        self.clibtn.setStyleSheet(default_btn_qss)

    def switch_to_apps(self):
        self.stack.setCurrentIndex(1)

        self.homebtn.setStyleSheet(default_btn_qss)
        self.appsbtn.setStyleSheet(selected_btn_qss)
        self.settingsbtn.setStyleSheet(default_btn_qss)
        self.clibtn.setStyleSheet(default_btn_qss)

    def switch_to_settings(self):
        self.stack.setCurrentIndex(2)

        self.homebtn.setStyleSheet(default_btn_qss)
        self.appsbtn.setStyleSheet(default_btn_qss)
        self.settingsbtn.setStyleSheet(selected_btn_qss)
        self.clibtn.setStyleSheet(default_btn_qss)

    def switch_to_cli(self):
        self.stack.setCurrentIndex(3)

        self.homebtn.setStyleSheet(default_btn_qss)
        self.appsbtn.setStyleSheet(default_btn_qss)
        self.settingsbtn.setStyleSheet(default_btn_qss)
        self.clibtn.setStyleSheet(selected_btn_qss)