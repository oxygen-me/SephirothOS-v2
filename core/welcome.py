# --- imports
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget
from PySide6.QtCore import Qt

# --- create welcome class
class WelcomeWindow(QWidget):
    def __init__(self, lcn=None):
        super().__init__()

        self.setWindowTitle("A Greeting Letter From Sephiroth")

        # --- immediately store reference
        self.lcn = lcn
        lcn = self.lcn

        # --- set fullscreen by default
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.showFullScreen()

        # --- set theme
        self.setStyleSheet("background-color: #15161a;")

        # --- set main layout
        self.mainlayout = QVBoxLayout()
        self.mainlayout.setContentsMargins(20, 20, 20, 20)
        self.mainlayout.setSpacing(0)
        self.setLayout(self.mainlayout)

        # --- content area creation
        self.contentarea = QWidget()
        self.contentarea.setStyleSheet("background-color: #1f2024;")
        self.mainlayout.addWidget(self.contentarea)

        # --- content layout setup
        self.contentlayout = QVBoxLayout()
        self.contentlayout.setContentsMargins(0, 0, 0, 0)
        self.contentlayout.setSpacing(0)
        self.contentarea.setLayout(self.contentlayout)

        # --- stacks
        self.stack = QStackedWidget()
        self.contentlayout.addWidget(self.stack)

        self.stack.addWidget(WelcomePage(self.stack))

        self.stack.setCurrentIndex(0)

class WelcomePage(QWidget):
    def __init__(self, stack):
        super().__init__()

        # --- init style
        self.setStyleSheet("background-color: transparent;")

        # --- layout
        self.mainlayout = QVBoxLayout()
        self.mainlayout.setContentsMargins(40, 40, 40, 40)
        self.mainlayout.setSpacing(0)
        self.setLayout(self.mainlayout)

        # --- welcome label
        self.welcomelabel = QLabel("Welcome to SephirothOS")
        self.welcomelabel.setStyleSheet("background-color: transparent; color: white; font-weight: bold; font-family: Segoe UI; font-size: 84px; font-style: italic;")
        self.mainlayout.addWidget(self.welcomelabel)

        self.mainlayout.addStretch()