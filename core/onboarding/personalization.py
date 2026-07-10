# --- imports
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QButtonGroup
from PySide6.QtCore import Qt

from utils.themes import styles, tlib


# --- create personalizationpage class
class PersonalizationPage(QWidget):
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
        self.title = QLabel("Personalization")
        self.title.setStyleSheet(styles.w_title2(tlib.CURRENT))
        self.titlebox.addWidget(self.title)

        # --- subtitle
        self.subtitle = QLabel("You're taking forever. Hurry the fuck up.")
        self.subtitle.setStyleSheet(styles.w_subtitle2(tlib.CURRENT))
        self.titlebox.addWidget(self.subtitle)

        # --- theme card
        self.themecard = QWidget()
        self.themecard.setStyleSheet(styles.c_widget(tlib.CURRENT))

        self.themelayout = QVBoxLayout(self.themecard)
        self.themelayout.setContentsMargins(20, 20, 20, 20)
        self.themelayout.setSpacing(20)

        self.themetitlebox = QVBoxLayout()
        self.themetitlebox.setContentsMargins(0, 0, 0, 0)
        self.themetitlebox.setSpacing(10)

        self.themetitle = QLabel("Theme")
        self.themetitle.setStyleSheet(styles.a_subtitle(tlib.CURRENT))
        self.themetitlebox.addWidget(self.themetitle)

        self.themesubtitle = QLabel("Pick your favorite.")
        self.themesubtitle.setStyleSheet(styles.p_subtitle(tlib.CURRENT))
        self.themetitlebox.addWidget(self.themesubtitle)

        self.themelayout.addLayout(self.themetitlebox)

        self.voidbtn = QPushButton("Void")
        self.voidbtn.setStyleSheet(styles.o_btn(tlib.CURRENT))

        self.sunbtn = QPushButton("The Fucking Sun")
        self.sunbtn.setStyleSheet(styles.o_btn(tlib.CURRENT))

        self.pissbtn = QPushButton("Piss")
        self.pissbtn.setStyleSheet(styles.o_btn(tlib.CURRENT))

        self.randbtn = QPushButton("Random")
        self.randbtn.setStyleSheet(styles.o_btn(tlib.CURRENT))

        self.themegroup = QButtonGroup()
        self.themegroup.setExclusive(True)

        self.theme_btns = []

        for btn in [self.voidbtn, self.sunbtn, self.pissbtn, self.randbtn]:

            btn.setCheckable(True)
            btn.setFixedHeight(40)

            self.themelayout.addWidget(btn)
            self.themegroup.addButton(btn)
            self.theme_btns.append(btn)

        self.theme_btns[0].setChecked(True)

        self.themelayout.addStretch()

        # --- common card
        self.commoncard = QWidget()
        self.commoncard.setStyleSheet(styles.c_widget(tlib.CURRENT))

        self.commonlayout = QVBoxLayout(self.commoncard)
        self.commonlayout.setContentsMargins(20, 20, 20, 20)
        self.commonlayout.setSpacing(20)

        self.commontitlebox = QVBoxLayout()
        self.commontitlebox.setContentsMargins(0, 0, 0, 0)
        self.commontitlebox.setSpacing(10)

        self.commontitle = QLabel("Common Settings")
        self.commontitle.setStyleSheet(styles.a_subtitle(tlib.CURRENT))
        self.commontitlebox.addWidget(self.commontitle)

        self.commonsubtitle = QLabel("Pre-Configure a few things.")
        self.commonsubtitle.setStyleSheet(styles.p_subtitle(tlib.CURRENT))
        self.commontitlebox.addWidget(self.commonsubtitle)

        self.commonlayout.addLayout(self.commontitlebox)
        self.commonlayout.addStretch()

        # --- accent card
        self.accentcard = QWidget()
        self.accentcard.setStyleSheet(styles.c_widget(tlib.CURRENT))

        self.accentlayout = QVBoxLayout(self.accentcard)
        self.accentlayout.setContentsMargins(20, 20, 20, 20)
        self.accentlayout.setSpacing(20)

        self.accenttitlebox = QVBoxLayout()
        self.accenttitlebox.setContentsMargins(0, 0, 0, 0)
        self.accenttitlebox.setSpacing(10)

        self.accenttitle = QLabel("Accent Color")
        self.accenttitle.setStyleSheet(styles.a_subtitle(tlib.CURRENT))
        self.accenttitlebox.addWidget(self.accenttitle)

        self.accentsubtitle = QLabel("Oh boohoohoo I don't like purple.")
        self.accentsubtitle.setStyleSheet(styles.p_subtitle(tlib.CURRENT))
        self.accenttitlebox.addWidget(self.accentsubtitle)

        self.accentlayout.addLayout(self.accenttitlebox)
        self.accentlayout.addStretch()

        # --- main layout
        self.mainlayout = QVBoxLayout()
        self.mainlayout.setContentsMargins(20, 20, 20, 20)
        self.mainlayout.setSpacing(20)

        # --- hlayout
        self.hlayout = QHBoxLayout()
        self.hlayout.setContentsMargins(0, 0, 0, 0)
        self.hlayout.setSpacing(20)

        # --- assembly
        self.setLayout(self.mainlayout)
        self.mainlayout.addLayout(self.titlebox)

        self.hlayout.addWidget(self.themecard, 3)
        self.hlayout.addWidget(self.commoncard, 3)
        self.hlayout.addWidget(self.accentcard, 2)

        self.mainlayout.addLayout(self.hlayout, 1)

    def next_page(self):
        next_index = self.stack.currentIndex() + 1
        self.stack.setCurrentIndex(next_index)