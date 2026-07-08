# --- imports
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QLabel
from PySide6.QtCore import Qt

from pathlib import Path
import os

import utils.themes.tlib as tlib
import utils.themes.styles as styles

from core.onboarding.start import WelcomePage
from core.onboarding.language import LanguagePage

config_path = Path(str(os.getenv('APPDATA'))) / 'SephirothOS' / 'config.json'
license_path = Path(str(os.getenv('APPDATA'))) / 'SephirothOS' / 'license.json'


# --- globaL vars
username1 = ""

# --- create onboarding class
class WelcomeWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("A Greeting Letter From Sephiroth")

        # --- set fullscreen by default
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.showFullScreen()

        # --- set theme
        self.setStyleSheet(styles.b_widget(tlib.CURRENT))

        # --- set main layout
        self.mainlayout = QHBoxLayout()
        self.mainlayout.setContentsMargins(20, 20, 20, 20)
        self.mainlayout.setSpacing(20)
        self.setLayout(self.mainlayout)

        # --- sidebar
        self.sidebar = QWidget()
        self.sidebar.setStyleSheet(styles.d_widget(tlib.CURRENT))
        self.mainlayout.addWidget(self.sidebar)

        # --- sidebar layout
        self.sidelayout = QVBoxLayout()
        self.sidelayout.setContentsMargins(20, 20, 20, 20)
        self.sidelayout.setSpacing(10)
        self.sidebar.setLayout(self.sidelayout)

        steps = [
            ("Welcome", "You're in the right place."),
            ("Language", "Pick your favorite."),
            ("Profile", "Chud tycoon."),
            ("Personalization", "Make SephirothOS feel Sephirothish."),
            ("Settings", "You're a needy bastard."),
            ("All Set", "Entree Sansdan."),
        ]

        current_step = 1

        for i, (title, desc) in enumerate(steps, start=1):
            if i < current_step:
                state = "done"
            elif i == current_step:
                state = "active"
            else:
                state = "todo"

            self.sidelayout.addWidget(StepItem(i, title, desc, state))

        self.sidelayout.addStretch()

        self.tipcard = QWidget()
        self.tipcard.setStyleSheet(styles.c_widget(tlib.CURRENT))
        self.sidelayout.addWidget(self.tipcard)

        self.welcomelayout = QHBoxLayout(self.tipcard)
        self.welcomelayout.setContentsMargins(20, 20, 20, 20)
        self.welcomelayout.setSpacing(20)

        # --- symbol
        self.symbol = QLabel(">_")
        self.symbol.setStyleSheet(styles.a_subtitle(tlib.CURRENT))
        self.symbol.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.welcomelayout.addWidget(self.symbol)

        # --- text column
        self.wbox2 = QVBoxLayout()
        self.wbox2.setContentsMargins(0, 0, 0, 0)
        self.wbox2.setSpacing(0)

        self.body1 = QLabel("TIP")
        self.body1.setStyleSheet(styles.a_body(tlib.CURRENT))
        self.body1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.wbox2.addWidget(self.body1, alignment=Qt.AlignmentFlag.AlignTop)

        self.body2 = QLabel("You can change all of this later in Settings.")
        self.body2.setStyleSheet(styles.p_subtitle(tlib.CURRENT))
        self.body2.setWordWrap(True)
        self.wbox2.addWidget(self.body2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.welcomelayout.addLayout(self.wbox2)

        # --- content area creation
        self.contentarea = QWidget()
        self.contentarea.setStyleSheet(styles.d_widget(tlib.CURRENT))
        self.mainlayout.addWidget(self.contentarea, 1)

        # --- content layout setup
        self.contentlayout = QVBoxLayout()
        self.contentlayout.setContentsMargins(0, 0, 0, 0)
        self.contentlayout.setSpacing(0)
        self.contentarea.setLayout(self.contentlayout)

        # --- stack
        self.stack = QStackedWidget()
        self.contentlayout.addWidget(self.stack)

        self.stack.addWidget(WelcomePage(self.stack))
        self.stack.addWidget(LanguagePage(self.stack))

        self.stack.setCurrentIndex(1)

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout


class StepItem(QWidget):
    def __init__(self, number, title, desc, state="todo"):
        super().__init__()

        self.setFixedHeight(82)

        row = QHBoxLayout(self)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(12)

        circle = QLabel(str(number))
        circle.setFixedSize(40, 40)
        circle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if state == "active":
            circle.setStyleSheet(styles.s_circle(tlib.CURRENT))
        elif state == "done":
            circle.setStyleSheet(styles.s_circle(tlib.CURRENT))
        else:
            circle.setStyleSheet(styles.d_circle(tlib.CURRENT))

        text_col = QVBoxLayout()
        text_col.setContentsMargins(0, 0, 0, 0)
        text_col.setSpacing(4)

        title_label = QLabel(title)
        desc_label = QLabel(desc)

        title_label.setStyleSheet(styles.c_title(tlib.CURRENT))
        desc_label.setStyleSheet(styles.c_subtitle(tlib.CURRENT))

        text_col.addStretch()
        text_col.addWidget(title_label)
        text_col.addWidget(desc_label)
        text_col.addStretch()

        row.addWidget(circle, alignment=Qt.AlignmentFlag.AlignVCenter)
        row.addLayout(text_col, 1)

        if state == "active":
            self.setStyleSheet("""
                StepItem {
                    background: transparent;
                    border: 1px solid rgba(155, 77, 255, 0.35);
                    border-radius: 10px;
                }
            """)
        else:
            self.setStyleSheet("background: transparent;")