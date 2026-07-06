# --- general imports
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, \
    QStackedWidget, QFrame, QButtonGroup, QScrollArea
from PySide6.QtCore import Qt
from utils.fun.headliners import window_names
import random

from utils.themes import styles, tlib

# --- get window title
window_title = random.choice(window_names)

# --- page imports
from ui.home import HomeTab
from ui.applications import AppsTab
from ui.settings import SettingsTab
from ui.cli import CLITab

# --- sidebar imports
from ui.home import HomeBar
from ui.applications import AppsBar
from ui.settings import SettingsBar
from ui.cli import CLIBar

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
        self.setStyleSheet(styles.b_widget(tlib.CURRENT))

        # --- set main layout
        self.mainlayout = QVBoxLayout()
        self.mainlayout.setContentsMargins(0, 0, 0, 0)
        self.mainlayout.setSpacing(0)
        self.setLayout(self.mainlayout)

        # --- topbar
        self.topbar = QWidget()
        self.topbar.setStyleSheet(styles.d_widget(tlib.CURRENT))

        # --- topbar layout
        self.topbarlayout = QHBoxLayout()
        self.topbarlayout.setContentsMargins(20, 20, 20, 20)
        self.topbarlayout.setSpacing(20)

        # --- buttons
        self.homebtn = QPushButton("Home")
        self.homebtn.setStyleSheet(styles.d_btn(tlib.CURRENT))

        self.appsbtn = QPushButton("Apps")
        self.appsbtn.setStyleSheet(styles.d_btn(tlib.CURRENT))

        self.settingsbtn = QPushButton("Settings")
        self.settingsbtn.setStyleSheet(styles.d_btn(tlib.CURRENT))

        self.clibtn = QPushButton("CLI")
        self.clibtn.setStyleSheet(styles.d_btn(tlib.CURRENT))

        # --- arealayout
        self.arealayout = QHBoxLayout()
        self.arealayout.setContentsMargins(20, 20, 20, 20)
        self.arealayout.setSpacing(20)

        # --- sidebar
        self.sidebar = QWidget()
        self.sidebar.setStyleSheet(styles.d_widget(tlib.CURRENT))

        # --- sidebar layout
        self.sidebarlayout = QVBoxLayout()
        self.sidebarlayout.setContentsMargins(20, 20, 20, 20)
        self.sidebarlayout.setSpacing(0)
        self.sidebar.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        # --- username
        self.username = QLabel(cfg["username"])
        self.username.setStyleSheet(styles.u_title(tlib.CURRENT))

        # --- user subtitle
        self.usersubtitle = QLabel("Veni, veni, venias, ne me mori facias.")
        self.usersubtitle.setStyleSheet(styles.c_subtitle(tlib.CURRENT))

        # --- status
        self.status = QLabel("Online")
        self.status.setStyleSheet(styles.c_subtitle(tlib.CURRENT))

        # --- div object
        self.divobject = QFrame()
        self.divobject.setFrameShape(QFrame.Shape.HLine)
        self.divobject.setFrameShadow(QFrame.Shadow.Sunken)
        self.divobject.setStyleSheet(styles.d_div(tlib.CURRENT))
        self.divobject.setFixedHeight(1)

        # --- mainarea
        self.mainarea = QWidget()
        self.mainarea.setStyleSheet(styles.d_widget(tlib.CURRENT))
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

        self.mainlayout.addWidget(self.topbar, 0)
        self.mainlayout.addLayout(self.arealayout, 1)

        self.arealayout.addWidget(self.sidebar, 0)
        self.arealayout.addWidget(self.mainarea, 1)

        self.mainarea.setLayout(self.stackarea)

        # --- stack
        self.stack = QStackedWidget()

        self.home_tab = HomeTab(self.stack)
        self.apps_tab = AppsTab(self.stack)
        self.settings_tab = SettingsTab(self.stack)
        self.cli_tab = CLITab(self.stack)

        self.stack.addWidget(make_scroll_page(self.home_tab))
        self.stack.addWidget(make_scroll_page(self.apps_tab))
        self.stack.addWidget(make_scroll_page(self.settings_tab))
        self.stack.addWidget(make_scroll_page(self.cli_tab))

        self.stack.setCurrentIndex(0)

        self.stackarea.addWidget(self.stack)

        # --- side stack
        self.sidestack = QStackedWidget()

        self.home_bar = HomeBar(self.home_tab.homestack)
        self.apps_bar = AppsBar(self.apps_tab.appstack)
        self.settings_bar = SettingsBar(self.settings_tab.settingstack)
        self.cli_bar = CLIBar(self.cli_tab.clistack)

        self.sidestack.addWidget(make_scroll_page(self.home_bar))
        self.sidestack.addWidget(make_scroll_page(self.apps_bar))
        self.sidestack.addWidget(make_scroll_page(self.settings_bar))
        self.sidestack.addWidget(make_scroll_page(self.cli_bar))

        self.sidestack.setCurrentIndex(0)

        self.sidebarlayout.addSpacing(20)

        self.sidebarlayout.addWidget(self.sidestack, 1)

        # --- set expanding sizepolicy
        self.sidestack.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        # --- set size policies for compatibility
        self.sidebar.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.mainarea.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.stack.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.topbar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.sidebar.setMinimumHeight(0)
        self.sidestack.setMinimumHeight(0)

        self.stack.setMinimumHeight(0)

        self.group = QButtonGroup(self)

        toindex = 0

        for btn in (
                self.homebtn,
                self.appsbtn,
                self.settingsbtn,
                self.clibtn,
        ):
            btn.setCheckable(True)
            self.group.addButton(btn, toindex)
            toindex += 1

        self.group.setExclusive(True)

        self.homebtn.setChecked(True)

        self.group.idClicked.connect(self.change_tab)

    # --- create button methods
    def change_tab(self, index):
        self.stack.setCurrentIndex(index)
        self.sidestack.setCurrentIndex(index)

def make_scroll_page(widget):
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setFrameShape(QFrame.Shape.NoFrame)
    scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    scroll.setWidget(widget)
    return scroll