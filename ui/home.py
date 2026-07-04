# --- imports
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtCore import Qt

from eventbus import mainBus

from utils.fun.headliners import home_subtitles
import random

home_subtitle = random.choice(home_subtitles)

# --- create HomePage class
class HomePage(QWidget):
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
        self.title = QLabel("Welcome to Sephiroth's House")
        self.title.setStyleSheet("background-color: transparent; color: white; font-family: Segoe UI; font-size: 36px; font-weight: 500;")

        # --- create subtitle object
        self.subtitle = QLabel(home_subtitle)
        self.subtitle.setStyleSheet("background-color: transparent; color: #808080; font-family: Segoe UI; font-size: 18px; font-weight: 500;")

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
        self.clock.setStyleSheet(
            "background-color: transparent; color: white; font-family: Segoe UI; font-size: 36px; font-weight: 500;")

        # --- create date object
        self.date = QLabel()
        self.date.setStyleSheet(
            "background-color: transparent; color: #808080; font-family: Segoe UI; font-size: 18px; font-weight: 500;")

        # --- allow updates
        mainBus.clockUpdated.connect(self.onClockUpdated)

        # --- assemble clockbox
        self.clockbox.addWidget(self.clock)
        self.clockbox.addWidget(self.date)
        self.clockbox.addStretch()

        self.toprow.addLayout(self.clockbox)

    # --- clock update function
    def onClockUpdated(self, now):
        self.clock.setText(now.strftime("%I:%M %p"))
        self.date.setText(now.strftime("%A, %B %d, %Y"))