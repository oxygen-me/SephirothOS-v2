# --- imports
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFrame
from PySide6.QtCore import Qt

default_btn_qss = """
                QPushButton { background-color: transparent; color: white; font-family: Segoe UI; font-size: 16px; padding-top: 10px; padding-bottom: 10px; padding-right: 10px; padding-left: 10px; text-align: left;}
                QPushButton:hover { background-color: #1a1b20; }
                QPushButton:pressed { background-color: #1a1b1d }
                """

# --- create HomePage class
class SettingsPage(QWidget):
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
        self.title = QLabel("The Engine of Sephiroth's Toyota Supra")
        self.title.setStyleSheet("background-color: transparent; color: white; font-family: Segoe UI; font-size: 36px; font-weight: 500;")

        # --- create subtitle object
        self.subtitle = QLabel("I don't like these settings. Let's get a new one.")
        self.subtitle.setStyleSheet("background-color: transparent; color: #808080; font-family: Segoe UI; font-size: 18px; font-weight: 500;")

        # --- assemble titlebox
        self.titlebox.addWidget(self.title)
        self.titlebox.addWidget(self.subtitle)
        self.titlebox.addStretch()

        self.toprow.addLayout(self.titlebox)

        # --- add toprow stretch
        self.toprow.addStretch()

        # --- create sublayout
        self.seclayout = QVBoxLayout()
        self.seclayout.setContentsMargins(0, 0, 0, 0)
        self.seclayout.setSpacing(20)
        self.mainlayout.addLayout(self.seclayout, 1)

        # --- create hlayout
        self.hlayout = QHBoxLayout()
        self.hlayout.setContentsMargins(0, 0, 0, 0)
        self.hlayout.setSpacing(20)

        # --- create left layout
        self.leftlayout = QVBoxLayout()
        self.leftlayout.setContentsMargins(0, 0, 0, 0)
        self.leftlayout.setSpacing(20)

        # --- create right layout
        self.rightlayout = QVBoxLayout()
        self.rightlayout.setContentsMargins(0, 0, 0, 0)
        self.rightlayout.setSpacing(20)

        # --- make widgets
        # --------------------------

        # --- left
        self.syswidget = QWidget()
        self.syswidget.setStyleSheet("background-color: #1d1f22; border-radius: 0px;")

        self.syswidgetlayout = QVBoxLayout()
        self.syswidgetlayout.setContentsMargins(20, 20, 20, 20)
        self.syswidgetlayout.setSpacing(20)
        self.syswidget.setLayout(self.syswidgetlayout)

        self.systitle = QLabel("System Information")
        self.systitle.setStyleSheet(
            "background-color: transparent; color: white; font-family: Segoe UI; font-size: 18px; font-weight: 500;")
        self.syswidgetlayout.addWidget(self.systitle)

        self.syswidgetlayout.addStretch()



        self.updwidget = QWidget()
        self.updwidget.setStyleSheet("background-color: #1d1f22; border-radius: 0px;")

        self.updwidgetlayout = QVBoxLayout()
        self.updwidgetlayout.setContentsMargins(20, 20, 20, 20)
        self.updwidgetlayout.setSpacing(20)
        self.updwidget.setLayout(self.updwidgetlayout)

        self.updtitle = QLabel("Updates")
        self.updtitle.setStyleSheet(
            "background-color: transparent; color: white; font-family: Segoe UI; font-size: 18px; font-weight: 500;")
        self.updwidgetlayout.addWidget(self.updtitle)

        self.updwidgetlayout.addStretch()



        # --- right
        self.lrwidget = QWidget()
        self.lrwidget.setStyleSheet("background-color: #1d1f22; border-radius: 0px;")

        self.lrwidgetlayout = QVBoxLayout()
        self.lrwidgetlayout.setContentsMargins(20, 20, 20, 20)
        self.lrwidgetlayout.setSpacing(20)
        self.lrwidget.setLayout(self.lrwidgetlayout)

        self.lrtitle = QLabel("Language & Region")
        self.lrtitle.setStyleSheet(
            "background-color: transparent; color: white; font-family: Segoe UI; font-size: 18px; font-weight: 500;")
        self.lrwidgetlayout.addWidget(self.lrtitle)

        self.lrwidgetlayout.addStretch()



        self.startwidget = QWidget()
        self.startwidget.setStyleSheet("background-color: #1d1f22; border-radius: 0px;")

        self.startwidgetlayout = QVBoxLayout()
        self.startwidgetlayout.setContentsMargins(20, 20, 20, 20)
        self.startwidgetlayout.setSpacing(20)
        self.startwidget.setLayout(self.startwidgetlayout)

        self.starttitle = QLabel("Startup")
        self.starttitle.setStyleSheet(
            "background-color: transparent; color: white; font-family: Segoe UI; font-size: 18px; font-weight: 500;")
        self.startwidgetlayout.addWidget(self.starttitle)

        self.startwidgetlayout.addStretch()



        self.psecwidget = QWidget()
        self.psecwidget.setStyleSheet("background-color: #1d1f22; border-radius: 0px;")

        self.psecwidgetlayout = QVBoxLayout()
        self.psecwidgetlayout.setContentsMargins(20, 20, 20, 20)
        self.psecwidgetlayout.setSpacing(20)
        self.psecwidget.setLayout(self.psecwidgetlayout)

        self.psectitle = QLabel("Privacy & Security")
        self.psectitle.setStyleSheet(
            "background-color: transparent; color: white; font-family: Segoe UI; font-size: 18px; font-weight: 500;")
        self.psecwidgetlayout.addWidget(self.psectitle)

        self.psecwidgetlayout.addStretch()



        self.aboutwidget = QWidget()
        self.aboutwidget.setStyleSheet("background-color: #1d1f22; border-radius: 0px;")

        self.aboutwidgetlayout = QVBoxLayout()
        self.aboutwidgetlayout.setContentsMargins(20, 20, 20, 20)
        self.aboutwidgetlayout.setSpacing(20)
        self.aboutwidget.setLayout(self.aboutwidgetlayout)

        self.abouttitle = QLabel("About SephirothOS")
        self.abouttitle.setStyleSheet(
            "background-color: transparent; color: white; font-family: Segoe UI; font-size: 18px; font-weight: 500;")
        self.aboutwidgetlayout.addWidget(self.abouttitle)

        self.aboutwidgetlayout.addStretch()



        # --- assemble layouts
        self.seclayout.addLayout(self.hlayout)
        self.hlayout.addLayout(self.leftlayout)
        self.hlayout.addLayout(self.rightlayout)

        # --- add widgets to layouts
        self.leftlayout.addWidget(self.syswidget)
        self.leftlayout.addWidget(self.updwidget)

        self.rightlayout.addWidget(self.lrwidget)
        self.rightlayout.addWidget(self.startwidget)
        self.rightlayout.addWidget(self.psecwidget)

        self.seclayout.addWidget(self.aboutwidget)

class SettingsBar(QWidget):
    def __init__(self, stack):
        super().__init__()

        # --- configure bg to be transparent
        self.setStyleSheet("background-color: transparent;")

        # --- create mainlayout
        self.mainlayout = QVBoxLayout()
        self.mainlayout.setContentsMargins(0, 0, 0, 0)
        self.mainlayout.setSpacing(0)
        self.setLayout(self.mainlayout)

        # --- settings title
        self.settingstitle = QLabel("Settings")
        self.settingstitle.setStyleSheet("background-color: transparent; color: #808080; font-family: Segoe UI; font-size: 16px; font-weight: 650;")
        self.mainlayout.addWidget(self.settingstitle)

        self.mainlayout.addSpacing(10)

        # --- buttons
        self.generalbtn = QPushButton("General")
        self.generalbtn.setStyleSheet(default_btn_qss)
        self.mainlayout.addWidget(self.generalbtn)

        self.appearancebtn = QPushButton("Appearance")
        self.appearancebtn.setStyleSheet(default_btn_qss)
        self.mainlayout.addWidget(self.appearancebtn)

        self.notifbtn = QPushButton("Notifications")
        self.notifbtn.setStyleSheet(default_btn_qss)
        self.mainlayout.addWidget(self.notifbtn)

        self.soundbtn = QPushButton("Sound")
        self.soundbtn.setStyleSheet(default_btn_qss)
        self.mainlayout.addWidget(self.soundbtn)

        self.powerbtn = QPushButton("Power")
        self.powerbtn.setStyleSheet(default_btn_qss)
        self.mainlayout.addWidget(self.powerbtn)

        self.mainlayout.addSpacing(10)

        # --- div1
        self.div1 = QFrame()
        self.div1.setFrameShape(QFrame.Shape.HLine)
        self.div1.setFrameShadow(QFrame.Shadow.Sunken)
        self.div1.setStyleSheet("background-color: #1b1c1e")
        self.div1.setFixedHeight(2)
        self.mainlayout.addWidget(self.div1)

        self.mainlayout.addSpacing(20)

        # --- system title
        self.systemtitle = QLabel("System")
        self.systemtitle.setStyleSheet(
            "background-color: transparent; color: #808080; font-family: Segoe UI; font-size: 16px; font-weight: 650;")
        self.mainlayout.addWidget(self.systemtitle)

        self.mainlayout.addSpacing(10)

        # --- more buttons
        self.aboutbtn = QPushButton("About")
        self.aboutbtn.setStyleSheet(default_btn_qss)
        self.mainlayout.addWidget(self.aboutbtn)

        self.updatesbtn = QPushButton("Updates")
        self.updatesbtn.setStyleSheet(default_btn_qss)
        self.mainlayout.addWidget(self.updatesbtn)

        self.storagebtn = QPushButton("Storage")
        self.storagebtn.setStyleSheet(default_btn_qss)
        self.mainlayout.addWidget(self.storagebtn)

        self.backupbtn = QPushButton("Backup")
        self.backupbtn.setStyleSheet(default_btn_qss)
        self.mainlayout.addWidget(self.backupbtn)

        self.recoverybtn = QPushButton("Recovery")
        self.recoverybtn.setStyleSheet(default_btn_qss)
        self.mainlayout.addWidget(self.recoverybtn)

        self.mainlayout.addSpacing(10)

        # --- div2
        self.div2 = QFrame()
        self.div2.setFrameShape(QFrame.Shape.HLine)
        self.div2.setFrameShadow(QFrame.Shadow.Sunken)
        self.div2.setStyleSheet("background-color: #1b1c1e")
        self.div2.setFixedHeight(2)
        self.mainlayout.addWidget(self.div2)

        self.mainlayout.addSpacing(20)

        # --- advanced title
        self.advancedtitle = QLabel("Advanced")
        self.advancedtitle.setStyleSheet(
            "background-color: transparent; color: #808080; font-family: Segoe UI; font-size: 16px; font-weight: 650;")
        self.mainlayout.addWidget(self.advancedtitle)

        self.mainlayout.addSpacing(10)

        # --- more buttons
        self.devbtn = QPushButton("Developer Options")
        self.devbtn.setStyleSheet(default_btn_qss)
        self.mainlayout.addWidget(self.devbtn)

        self.expbtn = QPushButton("Experimental")
        self.expbtn.setStyleSheet(default_btn_qss)
        self.mainlayout.addWidget(self.expbtn)

        self.mainlayout.addSpacing(10)

        # --- div3
        self.div3 = QFrame()
        self.div3.setFrameShape(QFrame.Shape.HLine)
        self.div3.setFrameShadow(QFrame.Shadow.Sunken)
        self.div3.setStyleSheet("background-color: #1b1c1e")
        self.div3.setFixedHeight(2)
        self.mainlayout.addWidget(self.div3)