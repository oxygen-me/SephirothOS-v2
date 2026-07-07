# --- imports
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFrame, QStackedWidget, \
    QButtonGroup, QGroupBox, QSizePolicy, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QProgressBar
from PySide6.QtCore import Qt, QSize, QThread
from PySide6.QtGui import QIcon, QPixmap

from eventbus import mainBus
from api.backend.hometab.dashboard import DashboardBackend
from utils.fun.headliners import home_subtitles
from utils.fun.tipquote import qotds, tips
import random

home_subtitle = random.choice(home_subtitles)
qotd = random.choice(qotds)
totd = random.choice(tips)
tiptodisplay = totd

from utils.themes import styles, tlib

# --- create HomeTab class
class HomeTab(QWidget):
    def __init__(self, stack):
        super().__init__()

        # --- store stack
        self.stack = stack

        # --- configure bg to be transparent
        self.setStyleSheet(styles.t_widget(tlib.CURRENT))

        # --- create layout
        self.mainlayout = QVBoxLayout()
        self.mainlayout.setContentsMargins(0, 0, 0, 0)
        self.mainlayout.setSpacing(0)
        self.setLayout(self.mainlayout)

        # --- create stack
        self.homestack = QStackedWidget()

        self.homestack.addWidget(DashboardPage(self.homestack))
        self.homestack.addWidget(NotificationsPage(self.homestack))
        self.homestack.addWidget(TasksPage(self.homestack))
        self.homestack.addWidget(ActivityPage(self.homestack))

        self.homestack.setCurrentIndex(0)

        self.mainlayout.addWidget(self.homestack, 1)



class DashboardPage(QWidget):
    def __init__(self, homestack):
        super().__init__()

        # --- store stack
        self.stack = homestack

        # --- create backend thread
        self.dashboard_thread = QThread(self)
        self.dashboard_backend = DashboardBackend()

        self.dashboard_backend.moveToThread(self.dashboard_thread)

        self.dashboard_thread.started.connect(self.dashboard_backend.start)
        self.dashboard_backend.updated.connect(self.update_dashboard)

        self.dashboard_thread.start()

        # --- configure bg to be transparent
        self.setStyleSheet(styles.t_widget(tlib.CURRENT))

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
        self.title.setStyleSheet(styles.p_title(tlib.CURRENT))

        # --- create subtitle object
        self.subtitle = QLabel(home_subtitle)
        self.subtitle.setStyleSheet(styles.p_subtitle(tlib.CURRENT))

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
        self.clock.setStyleSheet(styles.p_title(tlib.CURRENT))
        self.clock.setAlignment(Qt.AlignmentFlag.AlignRight)

        # --- create date object
        self.date = QLabel()
        self.date.setStyleSheet(styles.p_subtitle(tlib.CURRENT))
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
        self.seclayout.addLayout(self.leftlayout, 5)
        self.seclayout.addLayout(self.rightlayout, 2)

        self.leftlayout.addLayout(self.tllayout)
        self.leftlayout.addLayout(self.bllayout)

        # --- make widgets
        # --------------------------

        # --- top system widget
        self.syswidget = QWidget()
        self.syswidget.setStyleSheet(styles.c_widget(tlib.CURRENT))

        self.syswidgetlayout = QVBoxLayout()
        self.syswidgetlayout.setContentsMargins(20, 20, 20, 20)
        self.syswidgetlayout.setSpacing(20)
        self.syswidget.setLayout(self.syswidgetlayout)

        self.systitle = QLabel("System Status")
        self.systitle.setStyleSheet(styles.c_title(tlib.CURRENT))
        self.syswidgetlayout.addWidget(self.systitle)

        self.syswidgetlayout.addSpacing(20)

        self.status1 = QLabel("")
        self.status1.setStyleSheet(styles.c_body(tlib.CURRENT))
        self.syswidgetlayout.addWidget(self.status1)
        self.status2 = QLabel("")
        self.status2.setStyleSheet(styles.c_body(tlib.CURRENT))
        self.syswidgetlayout.addWidget(self.status2)
        self.status3 = QLabel("")
        self.status3.setStyleSheet(styles.c_body(tlib.CURRENT))
        self.syswidgetlayout.addWidget(self.status3)

        self.syswidgetlayout.addStretch()

        self.sysdiv = QFrame()
        self.sysdiv.setFrameShape(QFrame.Shape.HLine)
        self.sysdiv.setFrameShadow(QFrame.Shadow.Sunken)
        self.sysdiv.setStyleSheet(styles.c_div(tlib.CURRENT))
        self.sysdiv.setFixedHeight(1)

        self.syswidgetlayout.addWidget(self.sysdiv)

        self.sysbottomrow = QHBoxLayout()
        self.sysbottomrow.setContentsMargins(0, 0, 0, 0)
        self.sysbottomrow.setSpacing(0)
        self.syswidgetlayout.addLayout(self.sysbottomrow)

        self.syssubtitle = QLabel("Last checked: just now")
        self.syssubtitle.setStyleSheet(styles.c_subtitle(tlib.CURRENT))
        self.sysbottomrow.addWidget(self.syssubtitle)

        self.nothingbtn = QPushButton("Check Again")
        self.nothingbtn.setStyleSheet(styles.c_btn(tlib.CURRENT))
        self.sysbottomrow.addWidget(self.nothingbtn, alignment=Qt.AlignmentFlag.AlignRight)

        # --- tip widget
        self.tipwidget = QWidget()
        self.tipwidget.setStyleSheet(styles.c_widget(tlib.CURRENT))

        self.tipwidgetlayout = QVBoxLayout()
        self.tipwidgetlayout.setContentsMargins(20, 20, 20, 20)
        self.tipwidgetlayout.setSpacing(20)
        self.tipwidget.setLayout(self.tipwidgetlayout)

        self.tiptitle = QLabel("Daily Tip")
        self.tiptitle.setStyleSheet(styles.c_title(tlib.CURRENT))
        self.tipwidgetlayout.addWidget(self.tiptitle)

        self.tipwidgetlayout.addStretch(1)

        self.tiplabel = QLabel(tiptodisplay)
        self.tiplabel.setWordWrap(True)
        self.tiplabel.setStyleSheet(styles.c_title(tlib.CURRENT))
        self.tipwidgetlayout.addWidget(self.tiplabel)

        self.tipwidgetlayout.addStretch(2)

        self.tipdiv = QFrame()
        self.tipdiv.setFrameShape(QFrame.Shape.HLine)
        self.tipdiv.setFrameShadow(QFrame.Shadow.Sunken)
        self.tipdiv.setStyleSheet(styles.c_div(tlib.CURRENT))
        self.tipdiv.setFixedHeight(1)

        self.tipwidgetlayout.addWidget(self.tipdiv)

        self.tipbottomrow = QHBoxLayout()
        self.tipbottomrow.setContentsMargins(0, 0, 0, 0)
        self.tipbottomrow.setSpacing(0)
        self.tipwidgetlayout.addLayout(self.tipbottomrow)

        self.tipsubtitle = QLabel(f"Tip #{str(tips.index(tiptodisplay) + 1)}")
        self.tipsubtitle.setStyleSheet(styles.c_subtitle(tlib.CURRENT))
        self.tipbottomrow.addWidget(self.tipsubtitle)

        self.nexttipbtn = QPushButton("Next Tip")
        self.nexttipbtn.setStyleSheet(styles.c_btn(tlib.CURRENT))
        self.nexttipbtn.clicked.connect(self.nextTip)
        self.tipbottomrow.addWidget(self.nexttipbtn, alignment=Qt.AlignmentFlag.AlignRight)

        self.quotewidget = QWidget()
        self.quotewidget.setStyleSheet(styles.c_widget(tlib.CURRENT))

        self.quotewidgetlayout = QVBoxLayout()
        self.quotewidgetlayout.setContentsMargins(20, 20, 20, 20)
        self.quotewidgetlayout.setSpacing(20)
        self.quotewidget.setLayout(self.quotewidgetlayout)

        self.quotetitle = QLabel("Quote of the Day")
        self.quotetitle.setStyleSheet(styles.c_title(tlib.CURRENT))
        self.quotewidgetlayout.addWidget(self.quotetitle)

        self.quotewidgetlayout.addStretch()

        self.quotelabel = QLabel('"' + qotd + '"')
        self.quotelabel.setWordWrap(True)
        self.quotelabel.setStyleSheet(styles.c_title(tlib.CURRENT))
        self.quotewidgetlayout.addWidget(self.quotelabel)

        self.quotefrom = QLabel("– Sephiroth")
        self.quotefrom.setStyleSheet(styles.c_body(tlib.CURRENT))
        self.quotewidgetlayout.addWidget(self.quotefrom)

        self.quotewidgetlayout.addStretch()

        self.quotediv = QFrame()
        self.quotediv.setFrameShape(QFrame.Shape.HLine)
        self.quotediv.setFrameShadow(QFrame.Shadow.Sunken)
        self.quotediv.setStyleSheet(styles.c_div(tlib.CURRENT))
        self.quotediv.setFixedHeight(1)
        self.quotewidgetlayout.addWidget(self.quotediv)

        self.inspirebtn = QPushButton("Inspire Me")
        self.inspirebtn.setStyleSheet(styles.c_btn(tlib.CURRENT))
        self.quotewidgetlayout.addWidget(self.inspirebtn, alignment=Qt.AlignmentFlag.AlignRight)

        # --- bottom left
        self.announcementwidget = QWidget()
        self.announcementwidget.setStyleSheet(styles.c_widget(tlib.CURRENT))

        self.announcementwidgetlayout = QVBoxLayout()
        self.announcementwidgetlayout.setContentsMargins(20, 20, 20, 20)
        self.announcementwidgetlayout.setSpacing(20)
        self.announcementwidget.setLayout(self.announcementwidgetlayout)

        self.announcementtitle = QLabel("Announcements")
        self.announcementtitle.setStyleSheet(styles.c_title(tlib.CURRENT))
        self.announcementwidgetlayout.addWidget(self.announcementtitle)

        self.announcementwidgetlayout.addStretch()

        self.appswidget = QWidget()
        self.appswidget.setStyleSheet(styles.c_widget(tlib.CURRENT))

        self.appswidgetlayout = QVBoxLayout()
        self.appswidgetlayout.setContentsMargins(20, 20, 20, 20)
        self.appswidgetlayout.setSpacing(20)
        self.appswidget.setLayout(self.appswidgetlayout)

        self.appstitle = QLabel("Top Apps")
        self.appstitle.setStyleSheet(styles.c_title(tlib.CURRENT))
        self.appswidgetlayout.addWidget(self.appstitle)

        self.appswidgetlayout.addStretch()

        # --- right
        self.perfwidget = QWidget()
        self.perfwidget.setStyleSheet(styles.c_widget(tlib.CURRENT))

        self.perfwidgetlayout = QVBoxLayout()
        self.perfwidgetlayout.setContentsMargins(20, 20, 20, 20)
        self.perfwidgetlayout.setSpacing(20)
        self.perfwidget.setLayout(self.perfwidgetlayout)

        self.perftitle = QLabel("Performance")
        self.perftitle.setStyleSheet(styles.c_title(tlib.CURRENT))
        self.perfwidgetlayout.addWidget(self.perftitle)

        self.perfdiv1 = QFrame()
        self.perfdiv1.setFrameShape(QFrame.Shape.HLine)
        self.perfdiv1.setFrameShadow(QFrame.Shadow.Sunken)
        self.perfdiv1.setStyleSheet(styles.c_div(tlib.CURRENT))
        self.perfdiv1.setFixedHeight(1)
        self.perfwidgetlayout.addWidget(self.perfdiv1)

        self.perfgraphslayout = QVBoxLayout()
        self.perfgraphslayout.setContentsMargins(0, 0, 0, 0)
        self.perfgraphslayout.setSpacing(0)
        self.perfwidgetlayout.addLayout(self.perfgraphslayout, 1)

        self.cpu_usage_title = QLabel("CPU Usage")
        self.ram_usage_title = QLabel("RAM")
        self.disk_usage_title = QLabel("Disk")
        self.extra_usage_title = QLabel("Piss")

        for i in [
            self.cpu_usage_title,
            self.ram_usage_title,
            self.disk_usage_title,
            self.extra_usage_title,
        ]:
            i.setStyleSheet(styles.c_title(tlib.CURRENT))

        self.cpu_usage_subtitle = QLabel("Thinking very hard. Hahaha. Hard...")
        self.cpu_usage_subtitle.setStyleSheet(styles.c_subtitle(tlib.CURRENT))
        self.ram_usage_subtitle = QLabel("Apparently enough to run this.")
        self.ram_usage_subtitle.setStyleSheet(styles.c_subtitle(tlib.CURRENT))
        self.disk_usage_subtitle = QLabel("I am selling your data as we speak.")
        self.disk_usage_subtitle.setStyleSheet(styles.c_subtitle(tlib.CURRENT))
        self.extra_usage_subtitle = QLabel("Bottom text")
        self.extra_usage_subtitle.setStyleSheet(styles.c_subtitle(tlib.CURRENT))

        if i in [
            self.cpu_usage_subtitle,
            self.ram_usage_subtitle,
            self.disk_usage_subtitle,
            self.extra_usage_subtitle,
        ]:
            i.setStyleSheet(styles.c_subtitle(tlib.CURRENT))

        self.cpu_usage_perc = QLabel("")
        self.ram_usage_perc = QLabel("")
        self.disk_usage_perc = QLabel("")
        self.extra_usage_perc = QLabel("")

        for i in [
            self.cpu_usage_perc,
            self.ram_usage_perc,
            self.disk_usage_perc,
            self.extra_usage_perc,
        ]:
            i.setStyleSheet(styles.c_title(tlib.CURRENT))

        self.cpubar = QProgressBar()
        self.cpubar.setRange(0, 100)
        self.cpubar.setStyleSheet(styles.x_pbar(tlib.CURRENT, "#38BDF8"))
        self.cpubar.setTextVisible(False)
        self.cpubar.setFixedHeight(6)

        self.rambar = QProgressBar()
        self.rambar.setRange(0, 100)
        self.rambar.setStyleSheet(styles.x_pbar(tlib.CURRENT, "#844bdd"))
        self.rambar.setTextVisible(False)
        self.rambar.setFixedHeight(6)

        self.diskbar = QProgressBar()
        self.diskbar.setRange(0, 100)
        self.diskbar.setStyleSheet(styles.x_pbar(tlib.CURRENT, "#63e45f"))
        self.diskbar.setTextVisible(False)
        self.diskbar.setFixedHeight(6)

        self.extrabar = QProgressBar()
        self.extrabar.setRange(0, 100)
        self.extrabar.setStyleSheet(styles.x_pbar(tlib.CURRENT, "#ffff00"))
        self.extrabar.setTextVisible(False)
        self.extrabar.setFixedHeight(6)

        self.cpu_layout = QVBoxLayout()
        self.cpu_layout.setContentsMargins(0, 0, 0, 0)
        self.cpu_layout.setSpacing(0)

        self.ram_layout = QVBoxLayout()
        self.ram_layout.setContentsMargins(0, 0, 0, 0)
        self.ram_layout.setSpacing(0)

        self.disk_layout = QVBoxLayout()
        self.disk_layout.setContentsMargins(0, 0, 0, 0)
        self.disk_layout.setSpacing(0)

        self.extra_layout = QVBoxLayout()
        self.extra_layout.setContentsMargins(0, 0, 0, 0)
        self.extra_layout.setSpacing(0)

        self.mincpulayout = QVBoxLayout()
        self.mincpulayout.setContentsMargins(0, 0, 0, 0)
        self.mincpulayout.setSpacing(0)
        self.mincpulayout.addWidget(self.cpu_usage_title)
        self.mincpulayout.addWidget(self.cpu_usage_subtitle)

        self.minramlayout = QVBoxLayout()
        self.minramlayout.setContentsMargins(0, 0, 0, 0)
        self.minramlayout.setSpacing(0)
        self.minramlayout.addWidget(self.ram_usage_title)
        self.minramlayout.addWidget(self.ram_usage_subtitle)

        self.mindisklayout = QVBoxLayout()
        self.mindisklayout.setContentsMargins(0, 0, 0, 0)
        self.mindisklayout.setSpacing(0)
        self.mindisklayout.addWidget(self.disk_usage_title)
        self.mindisklayout.addWidget(self.disk_usage_subtitle)

        self.minextralayout = QVBoxLayout()
        self.minextralayout.setContentsMargins(0, 0, 0, 0)
        self.minextralayout.setSpacing(0)
        self.minextralayout.addWidget(self.extra_usage_title)
        self.minextralayout.addWidget(self.extra_usage_subtitle)

        self.cpu_row = QHBoxLayout()
        self.cpu_row.setContentsMargins(0, 0, 0, 0)
        self.cpu_row.setSpacing(0)
        self.cpu_row.addLayout(self.mincpulayout)
        self.cpu_row.addWidget(self.cpu_usage_perc, alignment=Qt.AlignmentFlag.AlignRight)

        self.ram_row = QHBoxLayout()
        self.ram_row.setContentsMargins(0, 0, 0, 0)
        self.ram_row.setSpacing(0)
        self.ram_row.addLayout(self.minramlayout)
        self.ram_row.addWidget(self.ram_usage_perc, alignment=Qt.AlignmentFlag.AlignRight)

        self.disk_row = QHBoxLayout()
        self.disk_row.setContentsMargins(0, 0, 0, 0)
        self.disk_row.setSpacing(0)
        self.disk_row.addLayout(self.mindisklayout)
        self.disk_row.addWidget(self.disk_usage_perc, alignment=Qt.AlignmentFlag.AlignRight)

        self.extra_row = QHBoxLayout()
        self.extra_row.setContentsMargins(0, 0, 0, 0)
        self.extra_row.setSpacing(0)
        self.extra_row.addLayout(self.minextralayout)
        self.extra_row.addWidget(self.extra_usage_perc, alignment=Qt.AlignmentFlag.AlignRight)

        self.cpu_layout.addLayout(self.cpu_row)
        self.cpu_layout.addSpacing(10)
        self.cpu_layout.addWidget(self.cpubar)

        self.cpu_layout.addStretch()


        self.ram_layout.addLayout(self.ram_row)
        self.ram_layout.addSpacing(10)
        self.ram_layout.addWidget(self.rambar)

        self.ram_layout.addStretch()


        self.disk_layout.addLayout(self.disk_row)
        self.disk_layout.addSpacing(10)
        self.disk_layout.addWidget(self.diskbar)

        self.disk_layout.addStretch()


        self.extra_layout.addLayout(self.extra_row)
        self.extra_layout.addSpacing(10)
        self.extra_layout.addWidget(self.extrabar)

        self.extra_layout.addStretch()

        self.perfgraphslayout.addLayout(self.cpu_layout)
        self.perfgraphslayout.addLayout(self.ram_layout)
        self.perfgraphslayout.addLayout(self.disk_layout)
        self.perfgraphslayout.addLayout(self.extra_layout)

        self.storagewidget = QWidget()
        self.storagewidget.setStyleSheet(styles.c_widget(tlib.CURRENT))

        self.storagewidgetlayout = QVBoxLayout()
        self.storagewidgetlayout.setContentsMargins(20, 20, 20, 20)
        self.storagewidgetlayout.setSpacing(20)
        self.storagewidget.setLayout(self.storagewidgetlayout)

        self.storagetitle = QLabel("Storage")
        self.storagetitle.setStyleSheet(styles.c_title(tlib.CURRENT))
        self.storagewidgetlayout.addWidget(self.storagetitle)

        self.storagewidgetlayout.addStretch()

        self.drivename = QLabel(r"C:\ (Your Mom's House)")
        self.drivename.setStyleSheet(styles.c_body(tlib.CURRENT))
        self.storagewidgetlayout.addWidget(self.drivename)

        self.storagebar = QProgressBar()
        self.storagebar.setStyleSheet(styles.x_pbar(tlib.CURRENT, "#ffffff"))
        self.storagebar.setFixedHeight(6)
        self.storagebar.setRange(1, 100)
        self.storagewidgetlayout.addWidget(self.storagebar)

        self.inforow = QHBoxLayout()
        self.inforow.setContentsMargins(0, 0, 0, 0)
        self.inforow.setSpacing(0)
        self.storagewidgetlayout.addLayout(self.inforow)

        self.foa = QLabel("")
        self.foa.setStyleSheet(styles.c_body(tlib.CURRENT))
        self.inforow.addWidget(self.foa)

        self.storage_perc = QLabel("")
        self.storage_perc.setStyleSheet(styles.c_title(tlib.CURRENT))
        self.inforow.addWidget(self.storage_perc, alignment=Qt.AlignmentFlag.AlignRight)

        self.storagewidgetlayout.addStretch()

        # --- add widgets to layouts
        self.tllayout.addWidget(self.syswidget)
        self.tllayout.addWidget(self.tipwidget)
        self.tllayout.addWidget(self.quotewidget)

        self.bllayout.addWidget(self.announcementwidget)
        self.bllayout.addWidget(self.appswidget)

        self.rightlayout.addWidget(self.perfwidget, 3)
        self.rightlayout.addWidget(self.storagewidget, 1)

    # --- clock update function
    def onClockUpdated(self, now):
        self.clock.setText(now.strftime("%I:%M %p"))
        self.date.setText(now.strftime("%A, %B %d, %Y"))

    def nextTip(self):
        global tiptodisplay
        if tips.index(tiptodisplay) == len(tips) - 1:
            tiptodisplay = tips[0]
        else:
            tiptodisplay = tips[tips.index(tiptodisplay) + 1]

        self.tiplabel.setText(tiptodisplay)
        self.tipsubtitle.setText(f"Tip #{str(tips.index(tiptodisplay) + 1)}")

    # --- update the dashboard using backend like a fish from fishland
    def update_dashboard(self, snapshot):
        self.status1.setText(snapshot.status[0])
        self.status2.setText(snapshot.status[1])
        self.status3.setText(snapshot.status[2])

        self.cpubar.setValue(snapshot.performance.cpu)
        self.cpu_usage_perc.setText(str(snapshot.performance.cpu) + "%")

        self.rambar.setValue(snapshot.performance.ram)
        self.ram_usage_perc.setText(str(snapshot.performance.ram) + "%")

        self.diskbar.setValue(int(snapshot.performance.disk_active))
        self.disk_usage_perc.setText(f"{snapshot.performance.disk_active:.1f}%")

        self.extrabar.setValue(random.randint(1, 100))
        self.extra_usage_perc.setText(str(random.randint(1, 100)) + "%")

        self.foa.setText(f"{snapshot.storage.free_text} free of {snapshot.storage.total_text}")
        self.storagebar.setValue(snapshot.storage.percent)
        self.storage_perc.setText(str(snapshot.storage.percent) + "%")


class NotificationsPage(QWidget):
    def __init__(self, homestack):
        super().__init__()

        # --- store stack
        self.stack = homestack

        # --- configure bg to be transparent
        self.setStyleSheet(styles.t_widget(tlib.CURRENT))

        # --- create mainlayout
        self.mainlayout = QVBoxLayout()
        self.mainlayout.setContentsMargins(20, 20, 20, 20)
        self.mainlayout.setSpacing(20)
        self.setLayout(self.mainlayout)

        # --- create title box
        self.titlebox = QVBoxLayout()
        self.titlebox.setContentsMargins(0, 0, 0, 0)
        self.titlebox.setSpacing(10)

        # --- create title object
        self.title = QLabel("Sephiroth's Mailbox")
        self.title.setStyleSheet(styles.p_title(tlib.CURRENT))
        self.titlebox.addWidget(self.title)

        # --- create subtitle object
        self.subtitle = QLabel("*rings doorbell with aura*")
        self.subtitle.setStyleSheet(styles.p_subtitle(tlib.CURRENT))
        self.titlebox.addWidget(self.subtitle)

        # --- add titlebox to main
        self.mainlayout.addLayout(self.titlebox)

        # --- create btnlayout
        self.btnlayout = QHBoxLayout()
        self.btnlayout.setContentsMargins(0, 0, 0, 0)
        self.btnlayout.setSpacing(20)
        self.mainlayout.addLayout(self.btnlayout, 1)

        # --- buttons
        self.allbtn = QPushButton("All")
        self.allbtn.setStyleSheet(styles.n_btn(tlib.CURRENT))
        self.btnlayout.addWidget(self.allbtn)

        self.unrbtn = QPushButton("Unread")
        self.unrbtn.setStyleSheet(styles.n_btn(tlib.CURRENT))
        self.btnlayout.addWidget(self.unrbtn)

        self.sysbtn = QPushButton("System")
        self.sysbtn.setStyleSheet(styles.n_btn(tlib.CURRENT))
        self.btnlayout.addWidget(self.sysbtn)

        self.updbtn = QPushButton("Updates")
        self.updbtn.setStyleSheet(styles.n_btn(tlib.CURRENT))
        self.btnlayout.addWidget(self.updbtn)

        self.secbtn = QPushButton("")

        self.pixmap1 = QPixmap(":/CadenceAteThem.png")
        self.cat = QIcon(self.pixmap1)

        self.secbtn.setIcon(self.cat)
        self.secbtn.setIconSize(QSize(64, 64))
        self.secbtn.setFlat(True)
        self.btnlayout.addWidget(self.secbtn)

        self.pissbtn = QPushButton("Piss")
        self.pissbtn.setStyleSheet(styles.n_btn(tlib.CURRENT))
        self.btnlayout.addWidget(self.pissbtn)

        self.btnlayout.addStretch()

        self.readbtn = QPushButton("Mark all as read")
        self.readbtn.setStyleSheet(styles.n_btn(tlib.CURRENT))
        self.btnlayout.addWidget(self.readbtn)

        self.mainlayout.addLayout(self.btnlayout)

        # --- unread layout
        self.unreadlayout = QVBoxLayout()
        self.unreadlayout.setContentsMargins(0, 0, 0, 0)
        self.unreadlayout.setSpacing(0)

        # --- unread label
        self.unreadlabel = QLabel("Unread")
        self.unreadlabel.setStyleSheet(styles.s_title(tlib.CURRENT))
        self.unreadlayout.addWidget(self.unreadlabel)

        self.mainlayout.addLayout(self.unreadlayout)

        # --- earlier layout
        self.earlierlayout = QVBoxLayout()
        self.earlierlayout.setContentsMargins(0, 0, 0, 0)
        self.earlierlayout.setSpacing(0)

        # --- earlier label
        self.earlierlabel = QLabel("Earlier")
        self.earlierlabel.setStyleSheet(styles.s_title(tlib.CURRENT))
        self.earlierlayout.addWidget(self.earlierlabel)

        self.mainlayout.addLayout(self.earlierlayout)

        self.mainlayout.addSpacing(20)

        self.mainlayout.addStretch()

        # --- end label
        self.endlabel = QLabel("She sephi on my roth 'til I Sephiroth")
        self.endlabel.setStyleSheet(styles.c_subtitle(tlib.CURRENT))
        self.mainlayout.addWidget(self.endlabel, alignment=Qt.AlignmentFlag.AlignHCenter)




class TasksPage(QWidget):
    def __init__(self, homestack):
        super().__init__()

        # --- store stack
        self.stack = homestack

        # --- configure bg to be transparent
        self.setStyleSheet(styles.t_widget(tlib.CURRENT))

        # --- create mainlayout
        self.mainlayout = QVBoxLayout()
        self.mainlayout.setContentsMargins(20, 20, 20, 20)
        self.mainlayout.setSpacing(20)
        self.setLayout(self.mainlayout)

        # --- create title box
        self.titlebox = QVBoxLayout()
        self.titlebox.setContentsMargins(0, 0, 0, 0)
        self.titlebox.setSpacing(10)

        # --- create title object
        self.title = QLabel("Sephiroth's 9-to-5")
        self.title.setStyleSheet(styles.p_title(tlib.CURRENT))
        self.titlebox.addWidget(self.title)

        # --- create subtitle object
        self.subtitle = QLabel("Still looking for my left shoe...")
        self.subtitle.setStyleSheet(styles.p_subtitle(tlib.CURRENT))
        self.titlebox.addWidget(self.subtitle)

        # --- add titlebox to main
        self.mainlayout.addLayout(self.titlebox)

        # --- create btnlayout
        self.btnlayout = QHBoxLayout()
        self.btnlayout.setContentsMargins(0, 0, 0, 0)
        self.btnlayout.setSpacing(20)
        self.mainlayout.addLayout(self.btnlayout, 1)

        # --- buttons
        self.allbtn = QPushButton("All")
        self.allbtn.setStyleSheet(styles.n_btn(tlib.CURRENT))
        self.btnlayout.addWidget(self.allbtn)

        self.todaybtn = QPushButton("Today")
        self.todaybtn.setStyleSheet(styles.n_btn(tlib.CURRENT))
        self.btnlayout.addWidget(self.todaybtn)

        self.upcbtn = QPushButton("Upcoming")
        self.upcbtn.setStyleSheet(styles.n_btn(tlib.CURRENT))
        self.btnlayout.addWidget(self.upcbtn)

        self.combtn = QPushButton("Completed")
        self.combtn.setStyleSheet(styles.n_btn(tlib.CURRENT))
        self.btnlayout.addWidget(self.combtn)

        self.ovebtn = QPushButton("Overdue")
        self.ovebtn.setStyleSheet(styles.n_btn(tlib.CURRENT))
        self.btnlayout.addWidget(self.ovebtn)

        self.btnlayout.addStretch()

        self.newbtn = QPushButton("+ New Task")
        self.newbtn.setStyleSheet(styles.n_btn(tlib.CURRENT))
        self.btnlayout.addWidget(self.newbtn)

        self.mainlayout.addLayout(self.btnlayout)

        self.groupbox = QGroupBox()
        self.groupbox.setStyleSheet(styles.g_box(tlib.CURRENT))
        self.groupbox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        self.mainlayout.addWidget(self.groupbox)

        self.mainlayout.addStretch()

        self.bottom_row = QHBoxLayout()
        self.bottom_row.setContentsMargins(0, 0, 0, 0)
        self.bottom_row.setSpacing(10)

        self.showing = QLabel("Showing 0 out of 0 tasks")
        self.showing.setStyleSheet(styles.c_subtitle(tlib.CURRENT))
        self.bottom_row.addWidget(self.showing)

        self.bottom_row.addStretch()

        self.mainlayout.addLayout(self.bottom_row)



class ActivityPage(QWidget):
    def __init__(self, homestack):
        super().__init__()

        # --- store stack
        self.stack = homestack

        # --- configure bg to be transparent
        self.setStyleSheet(styles.t_widget(tlib.CURRENT))

        # --- create mainlayout
        self.mainlayout = QVBoxLayout()
        self.mainlayout.setContentsMargins(20, 20, 20, 20)
        self.mainlayout.setSpacing(20)
        self.setLayout(self.mainlayout)

        # --- create toprow
        self.toprow = QHBoxLayout()
        self.toprow.setContentsMargins(0, 0, 0, 0)
        self.toprow.setSpacing(20)
        self.mainlayout.addLayout(self.toprow)

        # --- create title box
        self.titlebox = QVBoxLayout()
        self.titlebox.setContentsMargins(0, 0, 0, 0)
        self.titlebox.setSpacing(10)

        # --- create title object
        self.title = QLabel("Sephiroth's Contractor")
        self.title.setStyleSheet(styles.p_title(tlib.CURRENT))
        self.titlebox.addWidget(self.title)

        # --- create subtitle object
        self.subtitle = QLabel("I have very bad plumbing.")
        self.subtitle.setStyleSheet(styles.p_subtitle(tlib.CURRENT))
        self.titlebox.addWidget(self.subtitle)

        # --- add titlebox to toprow
        self.toprow.addLayout(self.titlebox)

        self.toprow.addStretch()

        # --- process search bar
        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Search processes...")
        self.searchbar.setStyleSheet(styles.d_sbar(tlib.CURRENT))
        self.toprow.addWidget(self.searchbar)

        # --- buttons
        self.newtaskbtn = QPushButton("Run new task")
        self.newtaskbtn.setStyleSheet(styles.n_btn(tlib.CURRENT))
        self.toprow.addWidget(self.newtaskbtn)

        self.endtaskbtn = QPushButton("End task")
        self.endtaskbtn.setStyleSheet(styles.n_btn(tlib.CURRENT))
        self.toprow.addWidget(self.endtaskbtn)

        self.extrasbtn = QPushButton(".svg")
        self.extrasbtn.setStyleSheet(styles.n_btn(tlib.CURRENT))
        self.toprow.addWidget(self.extrasbtn)

        # --- create btnlayout
        self.btnlayout = QHBoxLayout()
        self.btnlayout.setContentsMargins(0, 0, 0, 0)
        self.btnlayout.setSpacing(20)
        self.mainlayout.addLayout(self.btnlayout)

        # --- buttons
        self.procbtn = QPushButton("Processes")
        self.procbtn.setStyleSheet(styles.n_btn(tlib.CURRENT))
        self.btnlayout.addWidget(self.procbtn)

        self.perfbtn = QPushButton("Performance")
        self.perfbtn.setStyleSheet(styles.n_btn(tlib.CURRENT))
        self.btnlayout.addWidget(self.perfbtn)

        self.startbtn = QPushButton("Startup Apps")
        self.startbtn.setStyleSheet(styles.n_btn(tlib.CURRENT))
        self.btnlayout.addWidget(self.startbtn)

        self.userbtn = QPushButton("Users")
        self.userbtn.setStyleSheet(styles.n_btn(tlib.CURRENT))
        self.btnlayout.addWidget(self.userbtn)

        self.detailbtn = QPushButton("Details")
        self.detailbtn.setStyleSheet(styles.n_btn(tlib.CURRENT))
        self.btnlayout.addWidget(self.detailbtn)

        self.servbtn = QPushButton("Services")
        self.servbtn.setStyleSheet(styles.n_btn(tlib.CURRENT))
        self.btnlayout.addWidget(self.servbtn)

        self.btnlayout.addStretch()

        # --- graph row
        self.graphrow = QHBoxLayout()
        self.graphrow.setContentsMargins(0, 0, 0, 0)
        self.graphrow.setSpacing(20)
        self.mainlayout.addLayout(self.graphrow)

        # --- graph cards
        self.cpucard = QWidget()
        self.cpucard.setStyleSheet(styles.c_widget(tlib.CURRENT))

        self.cpulayout = QVBoxLayout()
        self.cpulayout.setContentsMargins(20, 20, 20, 20)
        self.cpulayout.setSpacing(0)
        self.cpucard.setLayout(self.cpulayout)

        self.cpulabel = QLabel("CPU")
        self.cpulabel.setStyleSheet(styles.c_title(tlib.CURRENT))
        self.cpulayout.addWidget(self.cpulabel)

        self.graphrow.addWidget(self.cpucard)


        self.memcard = QWidget()
        self.memcard.setStyleSheet(styles.c_widget(tlib.CURRENT))

        self.memlayout = QVBoxLayout()
        self.memlayout.setContentsMargins(20, 20, 20, 20)
        self.memlayout.setSpacing(0)
        self.memcard.setLayout(self.memlayout)

        self.memlabel = QLabel("Memory")
        self.memlabel.setStyleSheet(styles.c_title(tlib.CURRENT))
        self.memlayout.addWidget(self.memlabel)

        self.graphrow.addWidget(self.memcard)


        self.diskcard = QWidget()
        self.diskcard.setStyleSheet(styles.c_widget(tlib.CURRENT))

        self.disklayout = QVBoxLayout()
        self.disklayout.setContentsMargins(20, 20, 20, 20)
        self.disklayout.setSpacing(0)
        self.diskcard.setLayout(self.disklayout)

        self.disklabel = QLabel("Disk")
        self.disklabel.setStyleSheet(styles.c_title(tlib.CURRENT))
        self.disklayout.addWidget(self.disklabel)

        self.graphrow.addWidget(self.diskcard)


        self.netcard = QWidget()
        self.netcard.setStyleSheet(styles.c_widget(tlib.CURRENT))

        self.netlayout = QVBoxLayout()
        self.netlayout.setContentsMargins(20, 20, 20, 20)
        self.netlayout.setSpacing(0)
        self.netcard.setLayout(self.netlayout)

        self.netlabel = QLabel("Network")
        self.netlabel.setStyleSheet(styles.c_title(tlib.CURRENT))
        self.netlayout.addWidget(self.netlabel)

        self.graphrow.addWidget(self.netcard)


        self.gpucard = QWidget()
        self.gpucard.setStyleSheet(styles.c_widget(tlib.CURRENT))

        self.gpulayout = QVBoxLayout()
        self.gpulayout.setContentsMargins(20, 20, 20, 20)
        self.gpulayout.setSpacing(0)
        self.gpucard.setLayout(self.gpulayout)

        self.gpulabel = QLabel("GPU")
        self.gpulabel.setStyleSheet(styles.c_title(tlib.CURRENT))
        self.gpulayout.addWidget(self.gpulabel)

        self.graphrow.addWidget(self.gpucard)

        # --- table card
        self.table_card = QWidget()
        self.table_card.setStyleSheet(styles.c_widget(tlib.CURRENT))
        self.table_layout = QVBoxLayout()
        self.table_layout.setContentsMargins(20, 20, 20, 20)
        self.table_layout.setSpacing(20)
        self.table_card.setLayout(self.table_layout)

        # --- process table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Name", "Status", "CPU", "Memory", "Disk", "Network", "GPU", "Power usage"
        ])
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)

        self.table_layout.addWidget(self.table)
        self.mainlayout.addWidget(self.table_card)

        self.mainlayout.addStretch()

    def add_process(self, name, status, cpu, memory, disk, network, gpu, power):
        row = self.table.rowCount()
        self.table.insertRow(row)

        values = [name, status, cpu, memory, disk, network, gpu, power]

        for col, value in enumerate(values):
            item = QTableWidgetItem(value)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, col, item)



class HomeBar(QWidget):
    def __init__(self, stack):
        super().__init__()

        self.stack = stack

        # --- configure bg to be transparent
        self.setStyleSheet(styles.t_widget(tlib.CURRENT))

        # --- create mainlayout
        self.mainlayout = QVBoxLayout()
        self.mainlayout.setContentsMargins(0, 0, 0, 0)
        self.mainlayout.setSpacing(0)
        self.setLayout(self.mainlayout)

        # --- overview title
        self.overviewtitle = QLabel("Overview")
        self.overviewtitle.setStyleSheet(styles.s_title(tlib.CURRENT))
        self.mainlayout.addWidget(self.overviewtitle)

        self.mainlayout.addSpacing(10)

        # --- buttons
        self.dashboardbtn = QPushButton("Dashboard")
        self.dashboardbtn.setStyleSheet(styles.d_btn(tlib.CURRENT))
        self.mainlayout.addWidget(self.dashboardbtn)

        self.notifbtn = QPushButton("Notifications")
        self.notifbtn.setStyleSheet(styles.d_btn(tlib.CURRENT))
        self.mainlayout.addWidget(self.notifbtn)

        self.taskbtn = QPushButton("Tasks")
        self.taskbtn.setStyleSheet(styles.d_btn(tlib.CURRENT))
        self.mainlayout.addWidget(self.taskbtn)

        self.activebtn = QPushButton("Activity Monitor")
        self.activebtn.setStyleSheet(styles.d_btn(tlib.CURRENT))
        self.mainlayout.addWidget(self.activebtn)

        self.mainlayout.addSpacing(10)

        # --- div1
        self.div1 = QFrame()
        self.div1.setFrameShape(QFrame.Shape.HLine)
        self.div1.setFrameShadow(QFrame.Shadow.Sunken)
        self.div1.setStyleSheet(styles.d_div(tlib.CURRENT))
        self.div1.setFixedHeight(1)
        self.mainlayout.addWidget(self.div1)

        self.mainlayout.addSpacing(20)

        # --- quick access title
        self.accesstitle = QLabel("Quick Access")
        self.accesstitle.setStyleSheet(styles.s_title(tlib.CURRENT))
        self.mainlayout.addWidget(self.accesstitle)

        self.mainlayout.addSpacing(10)

        # --- more buttons
        self.filebtn = QPushButton("File Explorer")
        self.filebtn.setStyleSheet(styles.d_btn(tlib.CURRENT))
        self.mainlayout.addWidget(self.filebtn)

        self.terminalbtn = QPushButton("Terminal")
        self.terminalbtn.setStyleSheet(styles.d_btn(tlib.CURRENT))
        self.mainlayout.addWidget(self.terminalbtn)

        self.mkpbtn = QPushButton("Marketplace")
        self.mkpbtn.setStyleSheet(styles.d_btn(tlib.CURRENT))
        self.mainlayout.addWidget(self.mkpbtn)

        self.settingsbtn = QPushButton("Settings")
        self.settingsbtn.setStyleSheet(styles.d_btn(tlib.CURRENT))
        self.mainlayout.addWidget(self.settingsbtn)

        self.mainlayout.addSpacing(10)

        # --- div2
        self.div2 = QFrame()
        self.div2.setFrameShape(QFrame.Shape.HLine)
        self.div2.setFrameShadow(QFrame.Shadow.Sunken)
        self.div2.setStyleSheet(styles.d_div(tlib.CURRENT))
        self.div2.setFixedHeight(1)
        self.mainlayout.addWidget(self.div2)

        self.mainlayout.addSpacing(20)

        # --- recent files title
        self.recenttitle = QLabel("Recent Files")
        self.recenttitle.setStyleSheet(styles.s_title(tlib.CURRENT))
        self.mainlayout.addWidget(self.recenttitle)

        self.mainlayout.addSpacing(10)
        self.mainlayout.addStretch()

        self.group = QButtonGroup(self)

        toindex = 0

        for btn in (
            self.dashboardbtn,
            self.notifbtn,
            self.taskbtn,
            self.activebtn,
            self.filebtn,
            self.terminalbtn,
            self.mkpbtn,
            self.settingsbtn,
        ):
            btn.setCheckable(True)
            self.group.addButton(btn, toindex)
            toindex += 1

        self.group.setExclusive(True)

        self.dashboardbtn.setChecked(True)

        self.group.idClicked.connect(self.change_page)

    def change_page(self, index):
        self.stack.setCurrentIndex(index)