# --- imports
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, QGroupBox
from PySide6.QtCore import Qt

default_btn_qss = """
                QPushButton { background-color: transparent; color: white; font-family: Segoe UI; font-size: 16px; padding-top: 10px; padding-bottom: 10px; padding-right: 10px; padding-left: 10px; text-align: left; border: 0px}
                QPushButton:hover { background-color: #1a1b20; }
                QPushButton:pressed { background-color: #1a1b1d }
                """

# --- create AppsPage class
class AppsPage(QWidget):
    def __init__(self, stack):
        super().__init__()

        # --- store stack
        self.stack = stack

        # --- configure bg to be transparent
        self.setStyleSheet("background-color: transparent;")

        # --- create mainlayout
        self.mainlayout = QVBoxLayout()
        self.mainlayout.setContentsMargins(18, 10, 10, 10)
        self.mainlayout.setSpacing(10)
        self.setLayout(self.mainlayout)

        # --- create title
        self.title = QLabel("Sephiroth's Wing Clipping Startup")
        self.title.setStyleSheet("background-color: transparent; color: white; font-family: Segoe UI; font-size: 36px; font-weight: 500;")
        self.mainlayout.addWidget(self.title)
        self.mainlayout.addStretch()

class AppsBar(QWidget):
    def __init__(self, stack):
        super().__init__()

        # --- configure bg to be transparent
        self.setStyleSheet("background-color: transparent;")

        # --- create mainlayout
        self.mainlayout = QVBoxLayout()
        self.mainlayout.setContentsMargins(0, 0, 0, 0)
        self.mainlayout.setSpacing(0)
        self.setLayout(self.mainlayout)

        # --- apps title
        self.appstitle = QLabel("Apps")
        self.appstitle.setStyleSheet("background-color: transparent; color: #808080; font-family: Segoe UI; font-size: 16px; font-weight: 650;")
        self.mainlayout.addWidget(self.appstitle)

        self.mainlayout.addSpacing(10)

        # --- buttons
        self.allbtn = QPushButton("All Apps")
        self.allbtn.setStyleSheet(default_btn_qss)
        self.mainlayout.addWidget(self.allbtn)

        self.favbtn = QPushButton("Favorites")
        self.favbtn.setStyleSheet(default_btn_qss)
        self.mainlayout.addWidget(self.favbtn)

        self.sysbtn = QPushButton("System")
        self.sysbtn.setStyleSheet(default_btn_qss)
        self.mainlayout.addWidget(self.sysbtn)

        self.probtn = QPushButton("Productivity")
        self.probtn.setStyleSheet(default_btn_qss)
        self.mainlayout.addWidget(self.probtn)

        self.devbtn = QPushButton("Development")
        self.devbtn.setStyleSheet(default_btn_qss)
        self.mainlayout.addWidget(self.devbtn)

        self.mulbtn = QPushButton("Multimedia")
        self.mulbtn.setStyleSheet(default_btn_qss)
        self.mainlayout.addWidget(self.mulbtn)

        self.intbtn = QPushButton("Internet")
        self.intbtn.setStyleSheet(default_btn_qss)
        self.mainlayout.addWidget(self.intbtn)

        self.utilbtn = QPushButton("Utilities")
        self.utilbtn.setStyleSheet(default_btn_qss)
        self.mainlayout.addWidget(self.utilbtn)

        self.gamebtn = QPushButton("Games")
        self.gamebtn.setStyleSheet(default_btn_qss)
        self.mainlayout.addWidget(self.gamebtn)

        self.pissbtn = QPushButton("Piss")
        self.pissbtn.setStyleSheet(default_btn_qss)
        self.mainlayout.addWidget(self.pissbtn)

        self.mainlayout.addSpacing(10)

        # --- div1
        self.div1 = QFrame()
        self.div1.setFrameShape(QFrame.Shape.HLine)
        self.div1.setFrameShadow(QFrame.Shadow.Sunken)
        self.div1.setStyleSheet("background-color: #1b1c1e")
        self.div1.setFixedHeight(2)
        self.mainlayout.addWidget(self.div1)

        self.mainlayout.addSpacing(20)

        # --- collections title
        self.collstitle = QLabel("Collections")
        self.collstitle.setStyleSheet(
            "background-color: transparent; color: #808080; font-family: Segoe UI; font-size: 16px; font-weight: 650;")
        self.mainlayout.addWidget(self.collstitle)

        self.mainlayout.addSpacing(10)

        # --- buttons
        self.sephbtn = QPushButton("Sephiroth Approved")
        self.sephbtn.setStyleSheet(default_btn_qss)
        self.mainlayout.addWidget(self.sephbtn)

        self.wtfbtn = QPushButton("What the actual fuck is this?")
        self.wtfbtn.setStyleSheet(default_btn_qss)
        self.mainlayout.addWidget(self.wtfbtn)

        self.mainlayout.addSpacing(10)

        # --- div2
        self.div2 = QFrame()
        self.div2.setFrameShape(QFrame.Shape.HLine)
        self.div2.setFrameShadow(QFrame.Shadow.Sunken)
        self.div2.setStyleSheet("background-color: #1b1c1e")
        self.div2.setFixedHeight(2)
        self.mainlayout.addWidget(self.div2)

        self.mainlayout.addSpacing(20)

        # --- group box
        self.groupbox = QGroupBox()
        self.groupbox.setStyleSheet("border: 2px solid #1b1c1e")

        self.grouplayout = QVBoxLayout()
        self.grouplayout.setContentsMargins(10, 10, 10, 10)

        self.statuslabel = QLabel("Marketplace Status")
        self.statuslabel.setStyleSheet("background-color: transparent; color: #ffffff; font-family: Segoe UI; font-size: 16px; font-weight: 650; border: 0px")

        self.status = QLabel("Under Construction")
        self.status.setStyleSheet("background-color: transparent; color: #808080; font-family: Segoe UI; font-size: 12px; border: 0px")

        self.subtitle = QLabel("Be patient, you fat fuck.")
        self.subtitle.setStyleSheet("background-color: transparent; color: #ffffff; font-family: Segoe UI; font-size: 12px; border: 0px")

        self.groupbox.setLayout(self.grouplayout)

        self.grouplayout.addWidget(self.statuslabel)
        self.grouplayout.addWidget(self.status)

        self.grouplayout.addSpacing(10)

        self.grouplayout.addWidget(self.subtitle)

        self.mainlayout.addWidget(self.groupbox)

        self.mainlayout.addStretch()