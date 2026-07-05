# --- general imports
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, \
    QStackedWidget, QFrame
from PySide6.QtCore import Qt
from utils.fun.headliners import window_names
import random

# --- get window title
window_title = random.choice(window_names)

# --- extra vars
default_btn_qss = """
                QPushButton { background-color: transparent; color: white; font-family: Segoe UI; font-size: 16px; padding-top: 10px; padding-bottom: 10px; }
                QPushButton:hover { background-color: #1a1b20; }
                QPushButton:pressed { background-color: #1a1b1d }
                """

selected_btn_qss = "background-color: #1a1b1d; color: white; font-family: Segoe UI; font-size: 16px; padding-top: 10px; padding-bottom: 10px;"

# --- page imports
from ui.home import HomePage
from ui.applications import AppsPage
from ui.settings import SettingsPage
from ui.cli import CLIPage

# --- sidebar imports
from ui.home import HomeBar
# from ui.applications import AppsBar
from ui.settings import SettingsBar
# from ui.cli import CLIBar

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
        self.setStyleSheet("background-color: #1d1f22; border-radius: 0px;")

        # --- set main layout
        self.mainlayout = QVBoxLayout()
        self.mainlayout.setContentsMargins(0, 0, 0, 0)
        self.mainlayout.setSpacing(0)
        self.setLayout(self.mainlayout)

        # --- topbar
        self.topbar = QWidget()
        self.topbar.setStyleSheet("background-color: #111215;")

        # --- topbar layout
        self.topbarlayout = QHBoxLayout()
        self.topbarlayout.setContentsMargins(20, 20, 20, 20)
        self.topbarlayout.setSpacing(20)

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
        self.arealayout.setContentsMargins(20, 20, 20, 20)
        self.arealayout.setSpacing(20)

        # --- sidebar
        self.sidebar = QWidget()
        self.sidebar.setStyleSheet("background-color: #111215;")

        # --- sidebar layout
        self.sidebarlayout = QVBoxLayout()
        self.sidebarlayout.setContentsMargins(20, 20, 20, 20)
        self.sidebarlayout.setSpacing(0)
        self.sidebar.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        # --- username
        self.username = QLabel(cfg["username"])
        self.username.setStyleSheet("background-color: transparent; color: white; font-family: Segoe UI; font-size: 18px; font-weight: 600;")

        # --- user subtitle
        self.usersubtitle = QLabel("Veni, veni, venias, ne me mori facias.")
        self.usersubtitle.setStyleSheet("background-color: transparent; color: #808080; font-family: Segoe UI; font-size: 14px; font-weight: 500;")

        # --- status
        self.status = QLabel("Online")
        self.status.setStyleSheet("background-color: transparent; color: #808080; font-family: Segoe UI; font-size: 14px; font-weight: 500;")

        # --- div object
        self.divobject = QFrame()
        self.divobject.setFrameShape(QFrame.Shape.HLine)
        self.divobject.setFrameShadow(QFrame.Shadow.Sunken)
        self.divobject.setStyleSheet("background-color: #1b1c1e")
        self.divobject.setFixedHeight(2)

        # --- mainarea
        self.mainarea = QWidget()
        self.mainarea.setStyleSheet("background-color: #111215;")
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
        self.sidebarlayout.addWidget(self.username)
        self.sidebarlayout.addSpacing(10)
        self.sidebarlayout.addWidget(self.usersubtitle)
        self.sidebarlayout.addWidget(self.status)
        self.sidebarlayout.addSpacing(20)
        self.sidebarlayout.addWidget(self.divobject)

        self.mainlayout.addWidget(self.topbar)

        self.mainlayout.addLayout(self.arealayout)
        self.arealayout.addWidget(self.sidebar)
        self.arealayout.addWidget(self.mainarea, 1)

        self.mainarea.setLayout(self.stackarea)

        # --- stack
        self.stack = QStackedWidget()

        self.stack.addWidget(HomePage(self.stack))
        self.stack.addWidget(AppsPage(self.stack))
        self.stack.addWidget(SettingsPage(self.stack))
        self.stack.addWidget(CLIPage(self.stack))

        self.stack.setCurrentIndex(0)

        self.stackarea.addWidget(self.stack)

        # --- side stack
        self.sidestack = QStackedWidget()

        self.sidestack.addWidget(HomeBar(self.sidestack))
        # self.sidestack.addWidget(AppsBar(self.sidestack))
        self.sidestack.addWidget(SettingsBar(self.sidestack))
        # self.sidestack.addWidget(CLIBar(self.sidestack))

        self.sidestack.setCurrentIndex(0)

        self.sidebarlayout.addSpacing(20)
        self.sidebarlayout.addWidget(self.sidestack)

        self.sidebarlayout.addStretch()

    # --- create button methods
    def switch_to_home(self):
        self.stack.setCurrentIndex(0)
        self.sidestack.setCurrentIndex(0)

        self.homebtn.setStyleSheet(selected_btn_qss)
        self.appsbtn.setStyleSheet(default_btn_qss)
        self.settingsbtn.setStyleSheet(default_btn_qss)
        self.clibtn.setStyleSheet(default_btn_qss)

    def switch_to_apps(self):
        self.stack.setCurrentIndex(1)
        self.sidestack.setCurrentIndex(1)

        self.homebtn.setStyleSheet(default_btn_qss)
        self.appsbtn.setStyleSheet(selected_btn_qss)
        self.settingsbtn.setStyleSheet(default_btn_qss)
        self.clibtn.setStyleSheet(default_btn_qss)

    def switch_to_settings(self):
        self.stack.setCurrentIndex(2)
        self.sidestack.setCurrentIndex(2)

        self.homebtn.setStyleSheet(default_btn_qss)
        self.appsbtn.setStyleSheet(default_btn_qss)
        self.settingsbtn.setStyleSheet(selected_btn_qss)
        self.clibtn.setStyleSheet(default_btn_qss)

    def switch_to_cli(self):
        self.stack.setCurrentIndex(3)
        self.sidestack.setCurrentIndex(3)

        self.homebtn.setStyleSheet(default_btn_qss)
        self.appsbtn.setStyleSheet(default_btn_qss)
        self.settingsbtn.setStyleSheet(default_btn_qss)
        self.clibtn.setStyleSheet(selected_btn_qss)