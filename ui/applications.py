# --- imports
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, QGroupBox, QStackedWidget, QButtonGroup, QHBoxLayout, QGroupBox
from PySide6.QtCore import Qt

from utils.themes import styles, tlib

# --- create AppsTab class
class AppsTab(QWidget):
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
        self.appstack = QStackedWidget()

        self.appstack.addWidget(AllAppsPage(self.appstack))

        self.appstack.setCurrentIndex(0)

        self.mainlayout.addWidget(self.appstack, 1)

class AllAppsPage(QWidget):
    def __init__(self, appstack):
        super().__init__()

        # --- store stack
        self.stack = appstack

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
        self.title = QLabel("Sephiroth's Wing Clipping Startup")
        self.title.setStyleSheet(styles.p_title(tlib.CURRENT))

        # --- create subtitle object
        self.subtitle = QLabel("The games on Sephiroth's phone.")
        self.subtitle.setStyleSheet(styles.p_subtitle(tlib.CURRENT))

        # --- assemble titlebox
        self.titlebox.addWidget(self.title)
        self.titlebox.addWidget(self.subtitle)
        self.titlebox.addStretch()

        self.toprow.addLayout(self.titlebox)

        # --- add toprow stretch
        self.toprow.addStretch()

class AppsBar(QWidget):
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

        # --- apps title
        self.appstitle = QLabel("Apps")
        self.appstitle.setStyleSheet(styles.s_title(tlib.CURRENT))
        self.mainlayout.addWidget(self.appstitle)

        self.mainlayout.addSpacing(10)

        # --- buttons
        self.allbtn = QPushButton("All Apps")
        self.allbtn.setStyleSheet(styles.d_btn(tlib.CURRENT))
        self.mainlayout.addWidget(self.allbtn)

        self.favbtn = QPushButton("Favorites")
        self.favbtn.setStyleSheet(styles.d_btn(tlib.CURRENT))
        self.mainlayout.addWidget(self.favbtn)

        self.sysbtn = QPushButton("System")
        self.sysbtn.setStyleSheet(styles.d_btn(tlib.CURRENT))
        self.mainlayout.addWidget(self.sysbtn)

        self.probtn = QPushButton("Productivity")
        self.probtn.setStyleSheet(styles.d_btn(tlib.CURRENT))
        self.mainlayout.addWidget(self.probtn)

        self.devbtn = QPushButton("Development")
        self.devbtn.setStyleSheet(styles.d_btn(tlib.CURRENT))
        self.mainlayout.addWidget(self.devbtn)

        self.mulbtn = QPushButton("Multimedia")
        self.mulbtn.setStyleSheet(styles.d_btn(tlib.CURRENT))
        self.mainlayout.addWidget(self.mulbtn)

        self.intbtn = QPushButton("Internet")
        self.intbtn.setStyleSheet(styles.d_btn(tlib.CURRENT))
        self.mainlayout.addWidget(self.intbtn)

        self.utilbtn = QPushButton("Utilities")
        self.utilbtn.setStyleSheet(styles.d_btn(tlib.CURRENT))
        self.mainlayout.addWidget(self.utilbtn)

        self.gamebtn = QPushButton("Games")
        self.gamebtn.setStyleSheet(styles.d_btn(tlib.CURRENT))
        self.mainlayout.addWidget(self.gamebtn)

        self.pissbtn = QPushButton("Piss")
        self.pissbtn.setStyleSheet(styles.d_btn(tlib.CURRENT))
        self.mainlayout.addWidget(self.pissbtn)

        self.mainlayout.addSpacing(10)

        # --- div1
        self.div1 = QFrame()
        self.div1.setFrameShape(QFrame.Shape.HLine)
        self.div1.setFrameShadow(QFrame.Shadow.Sunken)
        self.div1.setStyleSheet(styles.d_div(tlib.CURRENT))
        self.div1.setFixedHeight(1)
        self.mainlayout.addWidget(self.div1)

        self.mainlayout.addSpacing(20)

        # --- collections title
        self.collstitle = QLabel("Collections")
        self.collstitle.setStyleSheet(styles.s_title(tlib.CURRENT))
        self.mainlayout.addWidget(self.collstitle)

        self.mainlayout.addSpacing(10)

        # --- buttons
        self.sephbtn = QPushButton("Sephiroth Approved")
        self.sephbtn.setStyleSheet(styles.d_btn(tlib.CURRENT))
        self.mainlayout.addWidget(self.sephbtn)

        self.wtfbtn = QPushButton("What The Actual Fuck Is This?")
        self.wtfbtn.setStyleSheet(styles.d_btn(tlib.CURRENT))
        self.mainlayout.addWidget(self.wtfbtn)

        self.mainlayout.addSpacing(10)

        # --- div2
        self.div2 = QFrame()
        self.div2.setFrameShape(QFrame.Shape.HLine)
        self.div2.setFrameShadow(QFrame.Shadow.Sunken)
        self.div2.setStyleSheet(styles.d_div(tlib.CURRENT))
        self.div2.setFixedHeight(1)
        self.mainlayout.addWidget(self.div2)

        self.mainlayout.addSpacing(20)

        # --- group box
        self.groupbox = QGroupBox()
        self.groupbox.setStyleSheet(styles.g_box(tlib.CURRENT))

        self.grouplayout = QVBoxLayout()
        self.grouplayout.setContentsMargins(10, 10, 10, 10)

        self.statuslabel = QLabel("Marketplace Status")
        self.statuslabel.setStyleSheet(styles.s_title(tlib.CURRENT))

        self.status = QLabel("Under Construction")
        self.status.setStyleSheet(styles.s_subtitle(tlib.CURRENT))

        self.subtitle = QLabel("Be patient, you fat fuck.")
        self.subtitle.setStyleSheet(styles.s_subtitle(tlib.CURRENT))

        self.groupbox.setLayout(self.grouplayout)

        self.grouplayout.addWidget(self.statuslabel)
        self.grouplayout.addWidget(self.status)

        self.grouplayout.addSpacing(10)
        self.grouplayout.addWidget(self.subtitle)
        self.mainlayout.addWidget(self.groupbox)
        self.mainlayout.addStretch()

        self.group = QButtonGroup(self)

        toindex = 0

        for btn in (
                self.allbtn,
                self.favbtn,
                self.sysbtn,
                self.probtn,
                self.devbtn,
                self.mulbtn,
                self.intbtn,
                self.utilbtn,
                self.gamebtn,
                self.pissbtn,
                self.sephbtn,
                self.wtfbtn,
        ):
            btn.setCheckable(True)
            self.group.addButton(btn, toindex)
            toindex += 1

        self.group.setExclusive(True)

        self.allbtn.setChecked(True)

        self.group.idClicked.connect(self.change_page)

    def change_page(self, index):
        self.stack.setCurrentIndex(index)