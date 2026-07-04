# --- imports
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

# --- create SettingsPage class
class SettingsPage(QWidget):
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
        self.title = QLabel("The Engine of Sephiroth's Toyota Supra")
        self.title.setStyleSheet("background-color: transparent; color: white; font-family: Segoe UI; font-size: 36px; font-weight: 500;")
        self.mainlayout.addWidget(self.title)
        self.mainlayout.addStretch()