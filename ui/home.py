# --- imports
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtCore import Qt

from eventbus import mainBus

from utils.fun.headliners import home_subtitles
import random

home_subtitle = random.choice(home_subtitles)

# --- create HomePage class
class HomePage(QWidget):
    def __init__(self, stack):
        super().__init__()

        # --- store stack
        self.stack = stack

        # --- configure bg to be transparent
        self.setStyleSheet("background-color: transparent;")

        # --- create mainlayout
        self.mainlayout = QVBoxLayout()
        self.mainlayout.setContentsMargins(20, 20, 20, 20)
        self.mainlayout.setSpacing(20)
        self.setLayout(self.mainlayout)

        # --- create toprow
        self.toprow = QHBoxLayout()
        self.toprow.setContentsMargins(0, 0, 0, 0)
        self.toprow.setSpacing(0)
        self.mainlayout.addLayout(self.toprow)

        # --- create title box
        self.titlebox = QVBoxLayout()
        self.titlebox.setContentsMargins(0, 0, 0, 0)
        self.titlebox.setSpacing(10)

        # --- create title object
        self.title = QLabel("Welcome to Sephiroth's House")
        self.title.setStyleSheet("background-color: transparent; color: white; font-family: Segoe UI; font-size: 36px; font-weight: 500;")

        # --- create subtitle object
        self.subtitle = QLabel(home_subtitle)
        self.subtitle.setStyleSheet("background-color: transparent; color: #808080; font-family: Segoe UI; font-size: 18px; font-weight: 500;")

        # --- assemble titlebox
        self.titlebox.addWidget(self.title)
        self.titlebox.addWidget(self.subtitle)
        self.titlebox.addStretch()

        self.toprow.addLayout(self.titlebox)

        # --- add toprow stretch
        self.toprow.addStretch()

        # --- create clock box
        self.clockbox = QVBoxLayout()
        self.clockbox.setContentsMargins(0, 0, 0, 0)
        self.clockbox.setSpacing(10)

        # --- create clock object
        self.clock = QLabel()
        self.clock.setStyleSheet("background-color: transparent; color: white; font-family: Segoe UI; font-size: 36px; font-weight: 500;")
        self.clock.setAlignment(Qt.AlignmentFlag.AlignRight)

        # --- create date object
        self.date = QLabel()
        self.date.setStyleSheet("background-color: transparent; color: #808080; font-family: Segoe UI; font-size: 18px; font-weight: 500;")
        self.date.setAlignment(Qt.AlignmentFlag.AlignRight)

        # --- allow updates
        mainBus.clockUpdated.connect(self.onClockUpdated)

        # --- assemble clockbox
        self.clockbox.addWidget(self.clock)
        self.clockbox.addWidget(self.date)
        self.clockbox.addStretch()

        self.toprow.addLayout(self.clockbox)

        # --- create sublayout
        self.seclayout = QHBoxLayout()
        self.seclayout.setContentsMargins(0, 0, 0, 0)
        self.seclayout.setSpacing(20)
        self.mainlayout.addLayout(self.seclayout, 1)

        # --- create left layout
        self.leftlayout = QVBoxLayout()
        self.leftlayout.setContentsMargins(0, 0, 0, 0)
        self.leftlayout.setSpacing(20)

        # --- create topleftlayout
        self.tllayout = QHBoxLayout()
        self.tllayout.setContentsMargins(0, 0, 0, 0)
        self.tllayout.setSpacing(20)

        # --- create bottomleftlayout
        self.bllayout = QHBoxLayout()
        self.bllayout.setContentsMargins(0, 0, 0, 0)
        self.bllayout.setSpacing(20)

        # --- create right layout
        self.rightlayout = QVBoxLayout()
        self.rightlayout.setContentsMargins(0, 0, 0, 0)
        self.rightlayout.setSpacing(20)

        # --- assemble layouts
        self.seclayout.addLayout(self.leftlayout)
        self.seclayout.addLayout(self.rightlayout)

        self.leftlayout.addLayout(self.tllayout)
        self.leftlayout.addLayout(self.bllayout)

        # --- make widgets
        # --------------------------

        # --- top left
        self.syswidget = QWidget()
        self.syswidget.setStyleSheet("background-color: #1d1f22; border-radius: 0px;")

        self.syswidgetlayout = QVBoxLayout()
        self.syswidgetlayout.setContentsMargins(20, 20, 20, 20)
        self.syswidgetlayout.setSpacing(20)
        self.syswidget.setLayout(self.syswidgetlayout)

        self.systitle = QLabel("System Status")
        self.systitle.setStyleSheet("background-color: transparent; color: white; font-family: Segoe UI; font-size: 18px; font-weight: 500;")
        self.syswidgetlayout.addWidget(self.systitle)

        self.syswidgetlayout.addStretch()



        self.tipwidget = QWidget()
        self.tipwidget.setStyleSheet("background-color: #1d1f22; border-radius: 0px;")

        self.tipwidgetlayout = QVBoxLayout()
        self.tipwidgetlayout.setContentsMargins(20, 20, 20, 20)
        self.tipwidgetlayout.setSpacing(20)
        self.tipwidget.setLayout(self.tipwidgetlayout)

        self.tiptitle = QLabel("Daily Tip")
        self.tiptitle.setStyleSheet("background-color: transparent; color: white; font-family: Segoe UI; font-size: 18px; font-weight: 500;")
        self.tipwidgetlayout.addWidget(self.tiptitle)

        self.tipwidgetlayout.addStretch()



        self.quotewidget = QWidget()
        self.quotewidget.setStyleSheet("background-color: #1d1f22; border-radius: 0px;")

        self.quotewidgetlayout = QVBoxLayout()
        self.quotewidgetlayout.setContentsMargins(20, 20, 20, 20)
        self.quotewidgetlayout.setSpacing(20)
        self.quotewidget.setLayout(self.quotewidgetlayout)

        self.quotetitle = QLabel("Quote of the Day")
        self.quotetitle.setStyleSheet("background-color: transparent; color: white; font-family: Segoe UI; font-size: 18px; font-weight: 500;")
        self.quotewidgetlayout.addWidget(self.quotetitle)

        self.quotewidgetlayout.addStretch()



        # --- bottom left
        self.announcementwidget = QWidget()
        self.announcementwidget.setStyleSheet("background-color: #1d1f22; border-radius: 0px;")

        self.announcementwidgetlayout = QVBoxLayout()
        self.announcementwidgetlayout.setContentsMargins(20, 20, 20, 20)
        self.announcementwidgetlayout.setSpacing(20)
        self.announcementwidget.setLayout(self.announcementwidgetlayout)

        self.announcementtitle = QLabel("Announcements")
        self.announcementtitle.setStyleSheet("background-color: transparent; color: white; font-family: Segoe UI; font-size: 18px; font-weight: 500;")
        self.announcementwidgetlayout.addWidget(self.announcementtitle)

        self.announcementwidgetlayout.addStretch()



        self.appswidget = QWidget()
        self.appswidget.setStyleSheet("background-color: #1d1f22; border-radius: 0px;")

        self.appswidgetlayout = QVBoxLayout()
        self.appswidgetlayout.setContentsMargins(20, 20, 20, 20)
        self.appswidgetlayout.setSpacing(20)
        self.appswidget.setLayout(self.appswidgetlayout)

        self.appstitle = QLabel("Top Apps")
        self.appstitle.setStyleSheet("background-color: transparent; color: white; font-family: Segoe UI; font-size: 18px; font-weight: 500;")
        self.appswidgetlayout.addWidget(self.appstitle)

        self.appswidgetlayout.addStretch()



        # --- right
        self.perfwidget = QWidget()
        self.perfwidget.setStyleSheet("background-color: #1d1f22; border-radius: 0px;")

        self.perfwidgetlayout = QVBoxLayout()
        self.perfwidgetlayout.setContentsMargins(20, 20, 20, 20)
        self.perfwidgetlayout.setSpacing(20)
        self.perfwidget.setLayout(self.perfwidgetlayout)

        self.perftitle = QLabel("Performance")
        self.perftitle.setStyleSheet("background-color: transparent; color: white; font-family: Segoe UI; font-size: 18px; font-weight: 500;")
        self.perfwidgetlayout.addWidget(self.perftitle)

        self.perfwidgetlayout.addStretch()



        self.storagewidget = QWidget()
        self.storagewidget.setStyleSheet("background-color: #1d1f22; border-radius: 0px;")

        self.storagewidgetlayout = QVBoxLayout()
        self.storagewidgetlayout.setContentsMargins(20, 20, 20, 20)
        self.storagewidgetlayout.setSpacing(20)
        self.storagewidget.setLayout(self.storagewidgetlayout)

        self.storagetitle = QLabel("Storage")
        self.storagetitle.setStyleSheet("background-color: transparent; color: white; font-family: Segoe UI; font-size: 18px; font-weight: 500;")
        self.storagewidgetlayout.addWidget(self.storagetitle)

        self.storagewidgetlayout.addStretch()



        # --- add widgets to layouts
        self.tllayout.addWidget(self.syswidget)
        self.tllayout.addWidget(self.tipwidget)
        self.tllayout.addWidget(self.quotewidget)

        self.bllayout.addWidget(self.announcementwidget)
        self.bllayout.addWidget(self.appswidget)

        self.rightlayout.addWidget(self.perfwidget)
        self.rightlayout.addWidget(self.storagewidget)

    # --- clock update function
    def onClockUpdated(self, now):
        self.clock.setText(now.strftime("%I:%M %p"))
        self.date.setText(now.strftime("%A, %B %d, %Y"))