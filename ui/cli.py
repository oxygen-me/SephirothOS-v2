# --- imports
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, QStackedWidget, QButtonGroup, QHBoxLayout
from PySide6.QtCore import Qt

from utils.themes import styles, tlib

# --- create CLITab class
class CLITab(QWidget):
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
        self.clistack = QStackedWidget()

        self.clistack.addWidget(ShedPage(self.clistack))

        self.clistack.setCurrentIndex(0)

        self.mainlayout.addWidget(self.clistack, 1)

# --- create Sephiroth's Shed Page
class ShedPage(QWidget):
    def __init__(self, clistack):
        super().__init__()

        # --- store stack
        self.stack = clistack

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
        self.title = QLabel("Sephiroth's Shed")
        self.title.setStyleSheet(styles.p_title(tlib.CURRENT))

        # --- create subtitle object
        self.subtitle = QLabel("There is a bomb in your mailbox.")
        self.subtitle.setStyleSheet(styles.p_subtitle(tlib.CURRENT))

        # --- assemble titlebox
        self.titlebox.addWidget(self.title)
        self.titlebox.addWidget(self.subtitle)
        self.titlebox.addStretch()

        self.toprow.addLayout(self.titlebox)

        # --- add toprow stretch
        self.toprow.addStretch()

class CLIBar(QWidget):
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

        # --- terminal title
        self.terminaltitle = QLabel("Terminal")
        self.terminaltitle.setStyleSheet(styles.s_title(tlib.CURRENT))
        self.mainlayout.addWidget(self.terminaltitle)

        self.mainlayout.addSpacing(10)

        # --- buttons
        self.newtermbtn = QPushButton("New Terminal")
        self.newtermbtn.setStyleSheet(styles.d_btn(tlib.CURRENT))
        self.mainlayout.addWidget(self.newtermbtn)

        self.newtabbtn = QPushButton("New Tab")
        self.newtabbtn.setStyleSheet(styles.d_btn(tlib.CURRENT))
        self.mainlayout.addWidget(self.newtabbtn)

        self.splittermbtn = QPushButton("Split Terminal")
        self.splittermbtn.setStyleSheet(styles.d_btn(tlib.CURRENT))
        self.mainlayout.addWidget(self.splittermbtn)

        self.closebtn = QPushButton("Close Terminal")
        self.closebtn.setStyleSheet(styles.d_btn(tlib.CURRENT))
        self.mainlayout.addWidget(self.closebtn)

        self.mainlayout.addSpacing(10)

        # --- div1
        self.div1 = QFrame()
        self.div1.setFrameShape(QFrame.Shape.HLine)
        self.div1.setFrameShadow(QFrame.Shadow.Sunken)
        self.div1.setStyleSheet(styles.d_div(tlib.CURRENT))
        self.div1.setFixedHeight(1)
        self.mainlayout.addWidget(self.div1)

        self.mainlayout.addSpacing(20)

        # --- sessions title
        self.sessionstitle = QLabel("Sessions")
        self.sessionstitle.setStyleSheet(styles.s_title(tlib.CURRENT))
        self.mainlayout.addWidget(self.sessionstitle)

        self.mainlayout.addSpacing(10)

        # --- more buttons
        self.sephshedbtn = QPushButton("Sephiroth's Shed")
        self.sephshedbtn.setStyleSheet(styles.d_btn(tlib.CURRENT))
        self.mainlayout.addWidget(self.sephshedbtn)

        self.managebtn = QPushButton("Manage Sessions")
        self.managebtn.setStyleSheet(styles.d_btn(tlib.CURRENT))
        self.mainlayout.addWidget(self.managebtn)

        self.mainlayout.addSpacing(10)

        # --- div2
        self.div2 = QFrame()
        self.div2.setFrameShape(QFrame.Shape.HLine)
        self.div2.setFrameShadow(QFrame.Shadow.Sunken)
        self.div2.setStyleSheet(styles.d_div(tlib.CURRENT))
        self.div2.setFixedHeight(1)
        self.mainlayout.addWidget(self.div2)

        self.mainlayout.addSpacing(20)

        # --- history title
        self.historytitle = QLabel("History")
        self.historytitle.setStyleSheet(styles.s_title(tlib.CURRENT))
        self.mainlayout.addWidget(self.historytitle)

        self.mainlayout.addSpacing(10)

        # --- more buttons
        self.showfullbtn = QPushButton("Show Full History")
        self.showfullbtn.setStyleSheet(styles.d_btn(tlib.CURRENT))
        self.mainlayout.addWidget(self.showfullbtn)

        self.mainlayout.addSpacing(10)

        # --- div3
        self.div3 = QFrame()
        self.div3.setFrameShape(QFrame.Shape.HLine)
        self.div3.setFrameShadow(QFrame.Shadow.Sunken)
        self.div3.setStyleSheet(styles.d_div(tlib.CURRENT))
        self.div3.setFixedHeight(1)
        self.mainlayout.addWidget(self.div3)

        self.mainlayout.addSpacing(20)

        # --- bookmarks title
        self.booktitle = QLabel("Bookmarks")
        self.booktitle.setStyleSheet(styles.s_title(tlib.CURRENT))
        self.mainlayout.addWidget(self.booktitle)

        self.mainlayout.addStretch()

        self.group = QButtonGroup(self)

        toindex = 0

        for btn in (
                self.newtermbtn,
                self.newtabbtn,
                self.splittermbtn,
                self.closebtn,
                self.sephshedbtn,
                self.managebtn,
        ):
            btn.setCheckable(True)
            self.group.addButton(btn, toindex)
            toindex += 1

        self.group.setExclusive(True)

        self.sephshedbtn.setChecked(True)

        self.group.idClicked.connect(self.change_page)

    def change_page(self, index):
        self.stack.setCurrentIndex(index)