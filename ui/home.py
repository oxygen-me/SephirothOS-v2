# --- imports
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFrame, QStackedWidget, \
    QButtonGroup, QGroupBox, QSizePolicy
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap

from eventbus import mainBus

from utils.fun.headliners import home_subtitles
import random

home_subtitle = random.choice(home_subtitles)

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
        self.seclayout.addLayout(self.leftlayout)
        self.seclayout.addLayout(self.rightlayout)

        self.leftlayout.addLayout(self.tllayout)
        self.leftlayout.addLayout(self.bllayout)

        # --- make widgets
        # --------------------------

        # --- top left
        self.syswidget = QWidget()
        self.syswidget.setStyleSheet(styles.c_widget(tlib.CURRENT))

        self.syswidgetlayout = QVBoxLayout()
        self.syswidgetlayout.setContentsMargins(20, 20, 20, 20)
        self.syswidgetlayout.setSpacing(20)
        self.syswidget.setLayout(self.syswidgetlayout)

        self.systitle = QLabel("System Status")
        self.systitle.setStyleSheet(styles.c_title(tlib.CURRENT))
        self.syswidgetlayout.addWidget(self.systitle)

        self.syswidgetlayout.addStretch()

        self.tipwidget = QWidget()
        self.tipwidget.setStyleSheet(styles.c_widget(tlib.CURRENT))

        self.tipwidgetlayout = QVBoxLayout()
        self.tipwidgetlayout.setContentsMargins(20, 20, 20, 20)
        self.tipwidgetlayout.setSpacing(20)
        self.tipwidget.setLayout(self.tipwidgetlayout)

        self.tiptitle = QLabel("Daily Tip")
        self.tiptitle.setStyleSheet(styles.c_title(tlib.CURRENT))
        self.tipwidgetlayout.addWidget(self.tiptitle)

        self.tipwidgetlayout.addStretch()

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

        self.perfwidgetlayout.addStretch()

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
        self.unreadlayout.setSpacing(5)

        # --- unread label
        self.unreadlabel = QLabel("Unread")
        self.unreadlabel.setStyleSheet(styles.s_title(tlib.CURRENT))
        self.unreadlayout.addWidget(self.unreadlabel)

        self.mainlayout.addLayout(self.unreadlayout)

        # --- earlier layout
        self.earlierlayout = QVBoxLayout()
        self.earlierlayout.setContentsMargins(0, 0, 0, 0)
        self.earlierlayout.setSpacing(5)

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

        # --- add titlebox to main
        self.mainlayout.addLayout(self.titlebox)



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