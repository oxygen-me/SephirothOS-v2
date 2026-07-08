# --- imports
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton

import utils.themes.tlib as tlib
import utils.themes.styles as styles


# --- create welcomepage class
class WelcomePage(QWidget):
    def __init__(self, stack):
        super().__init__()

        self.stack = stack

        # --- init style
        self.setStyleSheet(styles.t_widget(tlib.CURRENT))

        # --- titlebar
        self.titlebar = QHBoxLayout()
        self.titlebar.setContentsMargins(0, 0, 0, 0)
        self.titlebar.setSpacing(0)
        self.titlebar.addStretch()

        self.title = QLabel("Welcome to ")
        self.title.setStyleSheet(styles.w_title(tlib.CURRENT))
        self.titlebar.addWidget(self.title)

        self.word = QLabel("SephirothOS")
        self.word.setStyleSheet(styles.wa_title(tlib.CURRENT))
        self.titlebar.addWidget(self.word)

        self.titlebar.addStretch()

        # --- subtitle
        self.subtitle = QLabel("Who the fuck are you?")
        self.subtitle.setWordWrap(True)
        self.subtitle.setStyleSheet(styles.w_subtitle(tlib.CURRENT))
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- titlebox
        self.titlebox = QVBoxLayout()
        self.titlebox.setContentsMargins(0, 0, 0, 0)
        self.titlebox.setSpacing(10)
        self.titlebox.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.titlebox.addLayout(self.titlebar)
        self.titlebox.addWidget(self.subtitle)

        # --- welcome card
        self.welcomecard = QWidget()
        self.welcomecard.setStyleSheet(styles.s_widget(tlib.CURRENT))
        self.welcomecard.setFixedSize(760, 300)

        self.welcomelayout = QHBoxLayout(self.welcomecard)
        self.welcomelayout.setContentsMargins(24, 24, 24, 24)
        self.welcomelayout.setSpacing(18)

        # --- symbol
        self.symbol = QLabel(">_")
        self.symbol.setStyleSheet(styles.a_subtitle(tlib.CURRENT))
        self.symbol.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.welcomelayout.addWidget(self.symbol)

        # --- text column
        self.wbox2 = QVBoxLayout()
        self.wbox2.setContentsMargins(0, 0, 0, 0)
        self.wbox2.setSpacing(0)

        self.body1 = QLabel("You've made a good choice.")
        self.body1.setStyleSheet(styles.w_body(tlib.CURRENT))
        self.body1.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.body2 = QLabel(
            "SephirothOS is an OS designed with Sephiroth.\n"
            "It is designed by Sephiroths, for Sephiroths,\n"
            "of Sephiroths. I think I lost my left shoe.\n"
            "Please help."
        )
        self.body2.setStyleSheet(styles.w_body(tlib.CURRENT))
        self.body2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.body2.setWordWrap(False)

        self.body3 = QLabel("Let's set a few things up.")
        self.body3.setStyleSheet(styles.w_body(tlib.CURRENT))
        self.body3.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.wbox2.addWidget(self.body1)
        self.wbox2.addStretch(1)
        self.wbox2.addWidget(self.body2)
        self.wbox2.addStretch(1)
        self.wbox2.addWidget(self.body3)

        self.welcomelayout.addLayout(self.wbox2, 1)

        # --- next button
        self.nextbtn = QPushButton("Continue ⨠")
        self.nextbtn.setStyleSheet(styles.a_btn(tlib.CURRENT))

        # --- main layout
        self.mainlayout = QVBoxLayout(self)
        self.mainlayout.setContentsMargins(20, 20, 20, 20)
        self.mainlayout.setSpacing(0)

        self.mainlayout.addStretch(2)
        self.mainlayout.addLayout(self.titlebox)
        self.mainlayout.addSpacing(70)
        self.mainlayout.addWidget(
            self.welcomecard,
            alignment=Qt.AlignmentFlag.AlignHCenter
        )
        self.mainlayout.addStretch(3)
        self.mainlayout.addWidget(self.nextbtn, alignment=Qt.AlignmentFlag.AlignRight)

    def next_page(self):
        next_index = self.stack.currentIndex() + 1

        if next_index < self.stack.count():
            self.stack.setCurrentIndex(next_index)