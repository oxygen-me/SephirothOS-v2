# --- imports
from PySide6.QtWidgets import QDialog, QGridLayout, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, \
    QFileDialog, QLineEdit, QCheckBox, QSizePolicy, QComboBox
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QPainter, QPainterPath, QIcon

from utils.themes import styles, tlib
import random

import assets.pfps_rc as pfps_rc

# --- create accountpage class
class AccountPage(QWidget):
    def __init__(self, stack):
        super().__init__()

        self.stack = stack

        # --- init style
        self.setStyleSheet("background-color: transparent;")

        # --- make titlebox
        self.titlebox = QVBoxLayout()
        self.titlebox.setContentsMargins(0, 0, 0, 0)
        self.titlebox.setSpacing(10)

        # --- title
        self.title = QLabel("Account")
        self.title.setStyleSheet(styles.w_title2(tlib.CURRENT))
        self.titlebox.addWidget(self.title)

        # --- subtitle
        self.subtitle = QLabel("I don't have a good subtitle for this one, so fuck you. I bet you smell like crude oil.")
        self.subtitle.setStyleSheet(styles.w_subtitle2(tlib.CURRENT))
        self.titlebox.addWidget(self.subtitle)

        self.titlebox.addStretch()

        # --- details card
        self.detailscard = QWidget()
        self.detailscard.setStyleSheet(styles.c_widget(tlib.CURRENT))

        self.detailslayout = QVBoxLayout(self.detailscard)
        self.detailslayout.setContentsMargins(20, 20, 20, 20)
        self.detailslayout.setSpacing(20)

        self.detailcontentlayout = QHBoxLayout()
        self.detailcontentlayout.setContentsMargins(0, 0, 0, 0)
        self.detailcontentlayout.setSpacing(20)

        self.detailsleft = QVBoxLayout()
        self.detailsleft.setContentsMargins(0, 0, 0, 0)
        self.detailsleft.setSpacing(20)

        self.detailsright = QVBoxLayout()
        self.detailsright.setContentsMargins(0, 0, 0, 0)
        self.detailsright.setSpacing(20)

        self.detailstitle = QLabel("Profile Details")
        self.detailstitle.setStyleSheet(styles.a_subtitle(tlib.CURRENT))
        self.detailslayout.addWidget(self.detailstitle)

        self.detailslayout.addLayout(self.detailcontentlayout)

        self.pfplabel = QLabel("Profile Picture")
        self.pfplabel.setStyleSheet(styles.c_body(tlib.CURRENT))
        self.detailsleft.addWidget(self.pfplabel, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.pfp_preview = CircleImage(140)
        self.detailsleft.addWidget(self.pfp_preview, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.change_pfp_btn = QPushButton("Change Picture")
        self.change_pfp_btn.setStyleSheet(styles.n_btn(tlib.CURRENT))
        self.change_pfp_btn.clicked.connect(self.choose_pfp)
        self.detailsleft.addWidget(self.change_pfp_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.detailsleft.addStretch()

        self.usernamebox = QVBoxLayout()

        self.fullnamebox = QVBoxLayout()
        self.fullnamerow = QHBoxLayout()

        self.fullnamerow.setSpacing(5)
        self.fullnamerow.setContentsMargins(0, 0, 0, 0)

        self.biobox = QVBoxLayout()
        self.biorow = QHBoxLayout()

        self.biorow.setSpacing(5)
        self.biorow.setContentsMargins(0, 0, 0, 0)

        self.usernamebox.setSpacing(5)
        self.fullnamebox.setSpacing(5)
        self.biobox.setSpacing(5)

        self.usernamebox.setContentsMargins(0, 0, 0, 0)
        self.fullnamebox.setContentsMargins(0, 0, 0, 0)
        self.biobox.setContentsMargins(0, 0, 0, 0)

        self.usernametitle = QLabel("Username")
        self.usernameentry = QLineEdit()
        self.usernameentry.setPlaceholderText("Enter username...")

        self.usernamebox.addWidget(self.usernametitle)
        self.usernamebox.addWidget(self.usernameentry)

        self.fullnametitle = QLabel("Full Name")
        self.fullnamedisclaimer = QLabel("(optional)")
        self.fullnameentry = QLineEdit()
        self.fullnameentry.setPlaceholderText("Enter name...")
        self.fullnamesubtitle = QLabel("This is how your name will appear.")
        self.fullnamerow.addWidget(self.fullnametitle)
        self.fullnamerow.addWidget(self.fullnamedisclaimer)
        self.fullnamerow.addStretch()

        self.fullnamebox.addLayout(self.fullnamerow)
        self.fullnamebox.addWidget(self.fullnameentry)
        self.fullnamebox.addWidget(self.fullnamesubtitle)

        self.biotitle = QLabel("Bio")
        self.biodisclaimer = QLabel("(optional)")
        self.bioentry = QLineEdit()
        self.bioentry.setPlaceholderText("Enter bio...")
        self.biosubtitle = QLabel("A short bio about yourself.")
        self.biorow.addWidget(self.biotitle)
        self.biorow.addWidget(self.biodisclaimer)
        self.biorow.addStretch()

        self.bioentry.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.biobox.addLayout(self.biorow)
        self.biobox.addWidget(self.bioentry)
        self.biobox.addWidget(self.biosubtitle)

        for fish in [
            self.usernametitle,
            self.fullnametitle,
            self.biotitle
        ]:
            fish.setStyleSheet(styles.c_body(tlib.CURRENT))

        for cat in [
            self.usernameentry,
            self.fullnameentry
        ]:
            cat.setStyleSheet(styles.d_sbar(tlib.CURRENT))

        self.bioentry.setStyleSheet(styles.d_sbar(tlib.CURRENT))

        self.fullnamedisclaimer.setStyleSheet(styles.c_body2(tlib.CURRENT))
        self.biodisclaimer.setStyleSheet(styles.c_body2(tlib.CURRENT))

        self.fullnamesubtitle.setStyleSheet(styles.c_subtitle(tlib.CURRENT))
        self.biosubtitle.setStyleSheet(styles.c_subtitle(tlib.CURRENT))

        self.detailsright.addLayout(self.usernamebox)
        self.detailsright.addLayout(self.fullnamebox)
        self.detailsright.addLayout(self.biobox)

        self.detailcontentlayout.addLayout(self.detailsleft, 1)
        self.detailcontentlayout.addLayout(self.detailsright, 2)

        # --- account settings
        self.accountcard = QWidget()
        self.accountcard.setStyleSheet(styles.c_widget(tlib.CURRENT))

        self.accountlayout = QVBoxLayout()
        self.accountlayout.setContentsMargins(20, 20, 20, 20)
        self.accountlayout.setSpacing(20)
        self.accountcard.setLayout(self.accountlayout)

        self.accounttitlebox = QVBoxLayout()
        self.accounttitlebox.setContentsMargins(0, 0, 0, 0)
        self.accounttitlebox.setSpacing(10)

        self.accounttitle = QLabel("Account Settings")
        self.accounttitle.setStyleSheet(styles.a_subtitle(tlib.CURRENT))
        self.accounttitlebox.addWidget(self.accounttitle)

        self.accountsubtitle = QLabel("These settings control how your account works on this device")
        self.accountsubtitle.setStyleSheet(styles.p_subtitle(tlib.CURRENT))
        self.accounttitlebox.addWidget(self.accountsubtitle)

        self.accounttitlebox.addStretch()
        self.accountlayout.addLayout(self.accounttitlebox)

        self.div1 = QFrame()
        self.div1.setStyleSheet(styles.d_div(tlib.CURRENT))
        self.div1.setFrameShadow(QFrame.Shadow.Sunken)
        self.div1.setFrameShape(QFrame.Shape.HLine)
        self.div1.setFixedHeight(2)
        self.accountlayout.addWidget(self.div1)

        self.accountrow1 = QHBoxLayout()
        self.accountrow1.setContentsMargins(0, 0, 0, 0)
        self.accountrow1.setSpacing(0)
        self.accountlayout.addLayout(self.accountrow1)

        self.accountv1 = QVBoxLayout()
        self.accountv1.setContentsMargins(0, 0, 0, 0)
        self.accountv1.setSpacing(5)
        self.accountrow1.addLayout(self.accountv1)

        self.accounttitle1 = QLabel("Account Type")
        self.accounttitle1.setStyleSheet(styles.c_body(tlib.CURRENT))
        self.accountv1.addWidget(self.accounttitle1)

        self.accountsubtitle1 = QLabel("Standard accounts have limited system access.")
        self.accountsubtitle1.setStyleSheet(styles.c_subtitle(tlib.CURRENT))
        self.accountv1.addWidget(self.accountsubtitle1)

        self.userbox = QComboBox()
        self.userbox.setStyleSheet(styles.d_combo(tlib.CURRENT))

        self.userbox.addItems(["Standard User", "James", "Better User", "Aura Monster", "Single Mother", "Fish", "Golden Shower", "Sephiroth"])
        self.userbox.setCurrentIndex(0)

        self.accountrow1.addStretch()
        self.accountrow1.addWidget(self.userbox)

        self.div2 = QFrame()
        self.div2.setStyleSheet(styles.d_div(tlib.CURRENT))
        self.div2.setFrameShadow(QFrame.Shadow.Sunken)
        self.div2.setFrameShape(QFrame.Shape.HLine)
        self.div2.setFixedHeight(2)
        self.accountlayout.addWidget(self.div2)

        self.accountrow2 = QHBoxLayout()
        self.accountrow2.setContentsMargins(0, 0, 0, 0)
        self.accountrow2.setSpacing(0)
        self.accountlayout.addLayout(self.accountrow2)

        self.accountv2 = QVBoxLayout()
        self.accountv2.setContentsMargins(0, 0, 0, 0)
        self.accountv2.setSpacing(5)
        self.accountrow2.addLayout(self.accountv2)

        self.accounttitle2 = QLabel("Administrator Password")
        self.accounttitle2.setStyleSheet(styles.c_body(tlib.CURRENT))
        self.accountv2.addWidget(self.accounttitle2)

        self.accountsubtitle2 = QLabel("Required for making system-wide changes")
        self.accountsubtitle2.setStyleSheet(styles.c_subtitle(tlib.CURRENT))
        self.accountv2.addWidget(self.accountsubtitle2)

        self.passwordbtn = QPushButton("Set Password")
        self.passwordbtn.setStyleSheet(styles.n_btn(tlib.CURRENT))

        self.accountrow2.addStretch()
        self.accountrow2.addWidget(self.passwordbtn)

        self.div3 = QFrame()
        self.div3.setStyleSheet(styles.d_div(tlib.CURRENT))
        self.div3.setFrameShadow(QFrame.Shadow.Sunken)
        self.div3.setFrameShape(QFrame.Shape.HLine)
        self.div3.setFixedHeight(2)
        self.accountlayout.addWidget(self.div3)

        self.accountrow3 = QHBoxLayout()
        self.accountrow3.setContentsMargins(0, 0, 0, 0)
        self.accountrow3.setSpacing(0)
        self.accountlayout.addLayout(self.accountrow3)

        self.accountv3 = QVBoxLayout()
        self.accountv3.setContentsMargins(0, 0, 0, 0)
        self.accountv3.setSpacing(5)
        self.accountrow3.addLayout(self.accountv3)

        self.accounttitle3 = QLabel("Auto Login")
        self.accounttitle3.setStyleSheet(styles.c_body(tlib.CURRENT))
        self.accountv3.addWidget(self.accounttitle3)

        self.accountsubtitle3 = QLabel("+35 Piss Productivity")
        self.accountsubtitle3.setStyleSheet(styles.c_subtitle(tlib.CURRENT))
        self.accountv3.addWidget(self.accountsubtitle3)

        self.checkbox = QCheckBox()
        self.checkbox.setStyleSheet(styles.d_check(tlib.CURRENT))

        self.accountrow3.addStretch()
        self.accountrow3.addWidget(self.checkbox)

        self.div4 = QFrame()
        self.div4.setStyleSheet(styles.d_div(tlib.CURRENT))
        self.div4.setFrameShadow(QFrame.Shadow.Sunken)
        self.div4.setFrameShape(QFrame.Shape.HLine)
        self.div4.setFixedHeight(2)
        self.accountlayout.addWidget(self.div4)

        self.accountrow4 = QHBoxLayout()
        self.accountrow4.setContentsMargins(0, 0, 0, 0)
        self.accountrow4.setSpacing(0)
        self.accountlayout.addLayout(self.accountrow4)

        self.accountv4 = QVBoxLayout()
        self.accountv4.setContentsMargins(0, 0, 0, 0)
        self.accountv4.setSpacing(5)
        self.accountrow4.addLayout(self.accountv4)

        self.act4row = QHBoxLayout()
        self.act4row.setContentsMargins(0, 0, 0, 0)
        self.act4row.setSpacing(5)

        self.accounttitle4 = QLabel("Link GitHub Account")
        self.accounttitle4.setStyleSheet(styles.c_body(tlib.CURRENT))
        self.act4row.addWidget(self.accounttitle4)

        self.acctitle4sub = QLabel("(optional)")
        self.acctitle4sub.setStyleSheet(styles.c_body2(tlib.CURRENT))
        self.act4row.addWidget(self.acctitle4sub)

        self.act4row.addStretch()
        self.accountv4.addLayout(self.act4row)

        self.accountsubtitle4 = QLabel("Allows in-app issue reporting, development tools, etc.")
        self.accountsubtitle4.setStyleSheet(styles.c_subtitle(tlib.CURRENT))
        self.accountv4.addWidget(self.accountsubtitle4)

        self.linkbtn = QPushButton("Connect")
        self.linkbtn.setStyleSheet(styles.n_btn(tlib.CURRENT))

        self.accountrow4.addStretch()
        self.accountrow4.addWidget(self.linkbtn)

        # --- preview
        self.previewcard = QWidget()
        self.previewcard.setStyleSheet(styles.c_widget(tlib.CURRENT))

        self.previewlayout = QVBoxLayout()
        self.previewlayout.setContentsMargins(20, 20, 20, 20)
        self.previewlayout.setSpacing(10)

        self.previewtitle = QLabel("Preview")
        self.previewtitle.setStyleSheet(styles.a_subtitle(tlib.CURRENT))
        self.previewlayout.addWidget(self.previewtitle)

        self.previewsubtitle = QLabel("This is how your profile will appear.")
        self.previewsubtitle.setStyleSheet(styles.p_subtitle(tlib.CURRENT))
        self.previewlayout.addWidget(self.previewsubtitle)

        self.viewcard = QWidget()
        self.viewcard.setStyleSheet(styles.d_widget(tlib.CURRENT))

        self.viewlayout = QVBoxLayout(self.viewcard)
        self.viewlayout.setContentsMargins(0, 0, 0, 0)
        self.viewlayout.setSpacing(0)
        self.viewlayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.viewtitle = QLabel("PISS")
        self.viewtitle.setStyleSheet(styles.w_title(tlib.CURRENT))
        self.viewlayout.addWidget(self.viewtitle)

        self.viewcard.setLayout(self.viewlayout)
        self.previewlayout.addSpacing(10)
        self.previewlayout.addWidget(self.viewcard, 1)
        self.previewcard.setLayout(self.previewlayout)

        # --- note
        self.factcard = QWidget()
        self.factcard.setStyleSheet(styles.c_widget(tlib.CURRENT))

        self.factlayout = QVBoxLayout(self.factcard)
        self.factlayout.setContentsMargins(20, 20, 20, 20)
        self.factlayout.setSpacing(10)
        self.factcard.setLayout(self.factlayout)

        self.facttitle = QLabel("Fun Facts")
        self.facttitle.setStyleSheet(styles.a_subtitle(tlib.CURRENT))
        self.factlayout.addWidget(self.facttitle)

        self.factsubtitle1 = QLabel("Did you know?")
        self.factsubtitle1.setStyleSheet(styles.c_subtitle(tlib.CURRENT))
        self.factlayout.addWidget(self.factsubtitle1)

        random_number = random.randint(1, 99999999999)

        self.factemphasis = QLabel(f"{random_number:,}")
        self.factemphasis.setStyleSheet(styles.a_subtitle(tlib.CURRENT))
        self.factlayout.addWidget(self.factemphasis)

        self.factsubtitle2 = QLabel('SephirothOS users have the username "Sephiroth"')
        self.factsubtitle2.setStyleSheet(styles.c_subtitle(tlib.CURRENT))
        self.factlayout.addWidget(self.factsubtitle2)

        self.factdiv = QFrame()
        self.factdiv.setStyleSheet(styles.d_div(tlib.CURRENT))
        self.factdiv.setFixedHeight(1)
        self.factdiv.setFrameShadow(QFrame.Shadow.Sunken)
        self.factdiv.setFrameShape(QFrame.Shape.HLine)
        self.factlayout.addWidget(self.factdiv)

        self.factsubtitle3 = QLabel('Your data is auctioned off to foreign governments and third parties for our benefit!')
        self.factsubtitle3.setStyleSheet(styles.c_subtitle(tlib.CURRENT))
        self.factlayout.addWidget(self.factsubtitle3)

        self.factlayout.addStretch()

        # --- disclaimer
        self.disclaimercard = QWidget()
        self.disclaimercard.setStyleSheet(styles.c_widget(tlib.CURRENT))

        self.disclaimerlayout = QVBoxLayout(self.disclaimercard)
        self.disclaimerlayout.setContentsMargins(20, 20, 20, 20)
        self.disclaimerlayout.setSpacing(20)
        self.disclaimercard.setLayout(self.disclaimerlayout)

        self.distitle = QLabel("Privacy Note")
        self.distitle.setStyleSheet(styles.a_subtitle(tlib.CURRENT))
        self.disclaimerlayout.addWidget(self.distitle)

        self.disclaimer = QLabel("💀")
        self.disclaimer.setStyleSheet(styles.c_subtitle(tlib.CURRENT))
        self.disclaimerlayout.addWidget(self.disclaimer)

        self.disclaimerlayout.addStretch()

        # --- main layout
        self.mainlayout = QVBoxLayout()
        self.mainlayout.setContentsMargins(20, 20, 20, 20)
        self.mainlayout.setSpacing(20)

        # --- hlayout
        self.hlayout = QHBoxLayout()
        self.hlayout.setContentsMargins(0, 0, 0, 0)
        self.hlayout.setSpacing(20)

        # --- left layout
        self.leftlayout = QVBoxLayout()
        self.leftlayout.setContentsMargins(0, 0, 0, 0)
        self.leftlayout.setSpacing(20)

        # --- right layout
        self.rightlayout = QVBoxLayout()
        self.rightlayout.setContentsMargins(0, 0, 0, 0)
        self.rightlayout.setSpacing(20)

        # --- assembly
        self.setLayout(self.mainlayout)
        self.mainlayout.addLayout(self.titlebox)

        self.mainlayout.addLayout(self.hlayout, 1)
        self.hlayout.addLayout(self.leftlayout, 1)
        self.hlayout.addLayout(self.rightlayout, 1)

        self.leftlayout.addWidget(self.detailscard)
        self.leftlayout.addWidget(self.accountcard, 1)

        self.rightlayout.addWidget(self.previewcard, 3)
        self.rightlayout.addWidget(self.factcard, 2)
        self.rightlayout.addWidget(self.disclaimercard, 1)

    def next_page(self):
        next_index = self.stack.currentIndex() + 1
        self.stack.setCurrentIndex(next_index)

    def choose_pfp(self):
        dialog = AvatarPicker(self)

        if dialog.exec() == QDialog.DialogCode.Accepted and dialog.selected_path:
            self.pfp_preview.set_image(dialog.selected_path)

class CircleImage(QWidget):
    def __init__(self, size=140, parent=None):
        super().__init__(parent)
        self.setFixedSize(size, size)
        self.pixmap = None

    def set_image(self, path):
        pixmap = QPixmap(path)
        if not pixmap.isNull():
            self.pixmap = pixmap
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        path = QPainterPath()
        path.addEllipse(self.rect())
        painter.setClipPath(path)

        if self.pixmap:
            scaled = self.pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )

            x = (self.width() - scaled.width()) // 2
            y = (self.height() - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)
        else:
            painter.fillRect(self.rect(), tlib.CURRENT.surface)

class AvatarPicker(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selectedpath = None
        self.setWindowTitle("Choose Profile Picture")
        self.setModal(True)

        main = QVBoxLayout(self)
        grid = QGridLayout()

        avatars = [
            ":/avatars/default1.jpg",
            ":/avatars/default2.jpg",
            ":/avatars/default3.png",
            ":/avatars/default4.png",
            ":/avatars/default5.png",
        ]

        for i, path in enumerate(avatars):
            btn = QPushButton()
            btn.setFixedSize(90, 90)
            btn.setIcon(QIcon(path))
            btn.setIconSize(QSize(72, 72))
            btn.clicked.connect(lambda checked=False, p=path: self.pick(p))

            row = i // 3
            col = i % 3
            grid.addWidget(btn, row, col)

        main.addLayout(grid)

        custom_btn = QPushButton("Custom Picture...")
        custom_btn.clicked.connect(self.pick_custom)
        main.addWidget(custom_btn)

    def pick(self, path):
        self.selected_path = path
        self.accept()

    def pick_custom(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose Profile Picture",
            "",
            "Images (*.png *.jpg *.jpeg *.webp)"
        )

        if path:
            self.selected_path = path
            self.accept()