# --- imports
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
import json

from eventbus import mainBus

# --- create finishpage class
class FinishPage(QWidget):
    def __init__(self, stack):
        super().__init__()

        self.stack = stack

        # --- init style
        self.setStyleSheet("background-color: transparent;")

        # --- title
        self.title = QLabel("Your Sephiroth is ready")
        self.title.setStyleSheet("background-color: transparent; color: white; font-family: Segoe UI; font-size: 72px; font-weight: bold;")

        # --- subtitle
        self.subtitle = QLabel()
        self.subtitle.setWordWrap(True)

        self.subtitle.setText("Wait no. I don't have the title. My name is Denny's Sephiroth. I am legally divorced by the way.")
        self.subtitle.setStyleSheet(
            "background-color: transparent; color: white; font-family: Segoe UI; font-size: 24px; font-weight: 400;")

        # --- next button
        self.nextbtn = QPushButton("Finished")
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

        toWrite = {}

        with open(config_path, "w") as f:
            json.dump(toWrite, f, indent=4)

        with open(license_path, "r") as f:
            license_data = json.load(f)

        license_data["flag"] = "sephiroth"

        with open(license_path, "w") as f:
            json.dump(license_data, f, indent=4)

        mainBus.restartRequested.emit()