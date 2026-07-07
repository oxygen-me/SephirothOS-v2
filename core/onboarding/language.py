# --- imports
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox

# --- create languagepage class
class LanguagePage(QWidget):
    def __init__(self, stack):
        super().__init__()

        self.stack = stack

        # --- init style
        self.setStyleSheet("background-color: transparent;")

        # --- title
        self.title = QLabel("Select a language")
        self.title.setStyleSheet("background-color: transparent; color: white; font-family: Segoe UI; font-size: 72px; font-weight: bold;")

        # --- subtitle
        self.subtitle = QLabel()
        self.subtitle.setWordWrap(True)

        self.subtitle.setText('All languages come with a complimentary BOMB mailed DIRECTLY TO YOUR HOME. Quoth the Roth, "seaux de pisse."')
        self.subtitle.setStyleSheet("background-color: transparent; color: white; font-family: Segoe UI; font-size: 24px; font-weight: 400;")

        # --- selection
        self.selection = QComboBox()
        self.selection.setStyleSheet("background-color: #15161a; color: white; font-family: Segoe UI; font-size: 16px; font-weight: 400;")

        languages = [
            "Normal",
            "English (Simplified)",
            "English (Traditional)",
            "English (French)",
            "English 2",
            "Español",
            "Français",
            "Deutsch",
            "Homosexual",
            "Italiano",
            "Português",
            "Left Shoe",
            "日本語",
            "한국어",
            "中文",
            "Craigish",
            "Русский",
            "Latin",
            "Sephiroth",
        ]

        self.selection.addItems(languages)

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
        self.contentlayout.addWidget(self.selection)
        self.contentlayout.addWidget(self.nextbtn)

        self.divlayout.addStretch()

    def next_page(self):
        next_index = self.stack.currentIndex() + 1
        self.stack.setCurrentIndex(next_index)