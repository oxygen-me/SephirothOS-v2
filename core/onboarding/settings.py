# --- imports
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QPixmap

import assets.resource_rc as resource_rc

# --- create settingspage class
class SettingsPage(QWidget):
    def __init__(self, stack):
        super().__init__()

        self.stack = stack

        # --- init style
        self.setStyleSheet("background-color: transparent;")

        # --- title
        self.title = QLabel("Adjust your settings")
        self.title.setStyleSheet("background-color: transparent; color: white; font-family: Segoe UI; font-size: 72px; font-weight: bold;")

        # --- subtitle
        self.pixmap = QPixmap(":/CadenceAteThem.png")
        self.subtitle = QLabel()
        self.subtitle.setPixmap(self.pixmap)

        # --- next button
        self.nextbtn = QPushButton("Continue")
        self.nextbtn.setStyleSheet("""
        QPushButton { background-color: transparent; border: 2px solid #63e45f; color: #63e45f; font-family: Segoe UI; font-size: 24px; font-weight: 400; }
        QPushButton:hover { background-color: #27292e; }
        QPushButton:pressed { background-color: #15161a; }
        """)
        self.nextbtn.clicked.connect(self.next_page)

        # --- main layout
        self.mainlayout = QVBoxLayout()
        self.mainlayout.setContentsMargins(20, 20, 20, 20)
        self.mainlayout.setSpacing(0)

        # --- div layout
        self.divlayout = QHBoxLayout()
        self.divlayout.setContentsMargins(0, 0, 0, 0)
        self.divlayout.setSpacing(0)

        # --- content layout
        self.contentlayout = QVBoxLayout()
        self.contentlayout.setContentsMargins(0, 0, 0, 0)
        self.contentlayout.setSpacing(20)

        # --- assembly
        self.setLayout(self.mainlayout)
        self.mainlayout.addLayout(self.divlayout)
        self.divlayout.addLayout(self.contentlayout)

        self.contentlayout.addStretch()

        self.contentlayout.addWidget(self.title)
        self.contentlayout.addWidget(self.subtitle)



        self.contentlayout.addWidget(self.nextbtn)

        self.divlayout.addStretch()

    def next_page(self):
        next_index = self.stack.currentIndex() + 1
        self.stack.setCurrentIndex(next_index)