# --- imports
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QPushButton
from PySide6.QtCore import Qt

default_btn_qss = """
                QPushButton { background-color: transparent; color: white; font-family: Segoe UI; font-size: 16px; padding-top: 10px; padding-bottom: 10px; padding-right: 10px; padding-left: 10px; text-align: left; border: 0px}
                QPushButton:hover { background-color: #1a1b20; }
                QPushButton:pressed { background-color: #1a1b1d }
                """

# --- create CLIPage class
class CLIPage(QWidget):
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
        self.title = QLabel("Sephiroth's Shed")
        self.title.setStyleSheet("background-color: transparent; color: white; font-family: Segoe UI; font-size: 36px; font-weight: 500;")
        self.mainlayout.addWidget(self.title)
        self.mainlayout.addStretch()

class CLIBar(QWidget):
    def __init__(self, stack):
        super().__init__()

        # --- configure bg to be transparent
        self.setStyleSheet("background-color: transparent;")

        # --- create mainlayout
        self.mainlayout = QVBoxLayout()
        self.mainlayout.setContentsMargins(0, 0, 0, 0)
        self.mainlayout.setSpacing(0)
        self.setLayout(self.mainlayout)

        # --- terminal title
        self.terminaltitle = QLabel("Terminal")
        self.terminaltitle.setStyleSheet("background-color: transparent; color: #808080; font-family: Segoe UI; font-size: 16px; font-weight: 650;")
        self.mainlayout.addWidget(self.terminaltitle)

        self.mainlayout.addSpacing(10)

        # --- buttons
        self.newtermbtn = QPushButton("New Terminal")
        self.newtermbtn.setStyleSheet(default_btn_qss)
        self.mainlayout.addWidget(self.newtermbtn)

        self.newtabbtn = QPushButton("New Tab")
        self.newtabbtn.setStyleSheet(default_btn_qss)
        self.mainlayout.addWidget(self.newtabbtn)

        self.splittermbtn = QPushButton("Split Terminal")
        self.splittermbtn.setStyleSheet(default_btn_qss)
        self.mainlayout.addWidget(self.splittermbtn)

        self.closebtn = QPushButton("Close Terminal")
        self.closebtn.setStyleSheet(default_btn_qss)
        self.mainlayout.addWidget(self.closebtn)

        self.mainlayout.addSpacing(10)

        # --- div1
        self.div1 = QFrame()
        self.div1.setFrameShape(QFrame.Shape.HLine)
        self.div1.setFrameShadow(QFrame.Shadow.Sunken)
        self.div1.setStyleSheet("background-color: #1b1c1e")
        self.div1.setFixedHeight(2)
        self.mainlayout.addWidget(self.div1)

        self.mainlayout.addSpacing(20)

        # --- sessions title
        self.sessionstitle = QLabel("Sessions")
        self.sessionstitle.setStyleSheet(
            "background-color: transparent; color: #808080; font-family: Segoe UI; font-size: 16px; font-weight: 650;")
        self.mainlayout.addWidget(self.sessionstitle)

        self.mainlayout.addSpacing(10)

        # --- more buttons
        self.sephshedbtn = QPushButton("Sephiroth's Shed")
        self.sephshedbtn.setStyleSheet(default_btn_qss)
        self.mainlayout.addWidget(self.sephshedbtn)

        self.managebtn = QPushButton("Manage Sessions")
        self.managebtn.setStyleSheet(default_btn_qss)
        self.mainlayout.addWidget(self.managebtn)

        self.mainlayout.addSpacing(10)

        # --- div2
        self.div2 = QFrame()
        self.div2.setFrameShape(QFrame.Shape.HLine)
        self.div2.setFrameShadow(QFrame.Shadow.Sunken)
        self.div2.setStyleSheet("background-color: #1b1c1e")
        self.div2.setFixedHeight(2)
        self.mainlayout.addWidget(self.div2)

        self.mainlayout.addSpacing(20)

        # --- history title
        self.historytitle = QLabel("History")
        self.historytitle.setStyleSheet(
            "background-color: transparent; color: #808080; font-family: Segoe UI; font-size: 16px; font-weight: 650;")
        self.mainlayout.addWidget(self.historytitle)

        self.mainlayout.addSpacing(10)

        # --- more buttons
        self.showfullbtn = QPushButton("Show Full History")
        self.showfullbtn.setStyleSheet(default_btn_qss)
        self.mainlayout.addWidget(self.showfullbtn)

        self.mainlayout.addSpacing(10)

        # --- div3
        self.div3 = QFrame()
        self.div3.setFrameShape(QFrame.Shape.HLine)
        self.div3.setFrameShadow(QFrame.Shadow.Sunken)
        self.div3.setStyleSheet("background-color: #1b1c1e")
        self.div3.setFixedHeight(2)
        self.mainlayout.addWidget(self.div3)

        self.mainlayout.addSpacing(20)

        # --- bookmarks title
        self.booktitle = QLabel("Bookmarks")
        self.booktitle.setStyleSheet(
            "background-color: transparent; color: #808080; font-family: Segoe UI; font-size: 16px; font-weight: 650;")
        self.mainlayout.addWidget(self.booktitle)

        self.mainlayout.addStretch()