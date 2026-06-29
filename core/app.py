# --- imports
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QSizePolicy
from PySide6.QtCore import Qt, QRect

# --- create app class
class AppShell(QWidget):
    def __init__(self, lcn=None, config=None):
        super().__init__()

        # --- immediately store reference
        self.lcn = lcn
        lcn = self.lcn

        # --- set fullscreen by default
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.showFullScreen()

        # --- set main layout
        self.content = BackgroundWidget("assets/wallpaper2.png")

        self.rootlayout = QVBoxLayout()
        self.rootlayout.setContentsMargins(0,0,0,0)
        self.rootlayout.setSpacing(0)

        self.rootlayout.addWidget(self.content)

        self.mainlayout = QVBoxLayout()
        self.mainlayout.setContentsMargins(0,0,0,0)
        self.mainlayout.setSpacing(0)

        self.content.setLayout(self.mainlayout)

        self.topbar = QWidget()
        self.topbar.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.topbar.setMinimumHeight(100)
        self.mainlayout.addWidget(self.topbar)

        self.hbox = QHBoxLayout()
        self.hbox.setContentsMargins(0,0,0,0)
        self.hbox.setSpacing(0)

        self.mainlayout.addLayout(self.hbox)

        self.sidebar = QWidget()
        self.sidebar.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.sidebar.setMinimumWidth(300)
        self.sidebar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.hbox.addWidget(self.sidebar, alignment=Qt.AlignmentFlag.AlignLeft)

        self.setLayout(self.rootlayout)

class BackgroundWidget(QWidget):
    def __init__(self, image):
        super().__init__()
        self.pixmap = QPixmap(image)

    def paintEvent(self, event):
        if self.pixmap.isNull():
            return

        painter = QPainter(self)

        scaled = self.pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )

        x = (self.width() - scaled.width()) // 2
        y = (self.height() - scaled.height()) // 2

        painter.drawPixmap(x, y, scaled)