# --- imports
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout, QPushButton, QLineEdit, \
    QComboBox
from PySide6.QtCore import Qt

from eventbus import mainBus

from pathlib import Path

import json
import os

config_path = Path(str(os.getenv('APPDATA'))) / 'SephirothOS' / 'config.json'
license_path = Path(str(os.getenv('APPDATA'))) / 'SephirothOS' / 'license.json'


# --- globaL vars
username1 = ""

# --- create welcome class
class WelcomeWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("A Greeting Letter From Sephiroth")

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

        # --- stack
        self.stack = QStackedWidget()
        self.contentlayout.addWidget(self.stack)

        self.stack.addWidget(WelcomePage(self.stack))
        self.stack.addWidget(LanguagePage(self.stack))
        self.stack.addWidget(ThemePage(self.stack))
        self.stack.addWidget(AccountPage(self.stack))
        self.stack.addWidget(SettingsPage(self.stack))
        self.stack.addWidget(FinishPage(self.stack))

        self.stack.setCurrentIndex(0)

class WelcomePage(QWidget):
    def __init__(self, stack):
        super().__init__()

        self.stack = stack

        # --- init style
        self.setStyleSheet("background-color: transparent;")

        # --- title
        self.title = QLabel("Welcome to Sephiroth")
        self.title.setStyleSheet("background-color: transparent; color: white; font-family: Segoe UI; font-size: 72px; font-weight: bold;")

        # --- subtitle
        self.subtitle = QLabel()
        self.subtitle.setWordWrap(True)

        self.subtitle.setText("SephirothOS is an OS designed with Sephiroth. It is designed by Sephiroths, for Sephiroths, of Sephiroths. I think I lost my left shoe. Please help.")
        self.subtitle.setStyleSheet("background-color: transparent; color: white; font-family: Segoe UI; font-size: 24px; font-weight: 400;")

        # --- next button
        self.nextbtn = QPushButton("Get Started")
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

        self.subtitle.setText('All languages come with a complimentary BOMB mailed DIRECTLY TO YOUR HOME. Quoth the Sephiroth, "seaux de pisse."')
        self.subtitle.setStyleSheet("background-color: transparent; color: white; font-family: Segoe UI; font-size: 24px; font-weight: 400;")

        # --- selection
        self.selection = QComboBox()

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
            "日本語",
            "한국어",
            "中文",
            "Русский",
            "Latin",
            "Sephiroth",
            "Left Shoe",
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
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

class ThemePage(QWidget):
    def __init__(self, stack):
        super().__init__()

        self.stack = stack

        # --- init style
        self.setStyleSheet("background-color: transparent;")

        # --- title
        self.title = QLabel("Choose your theme")
        self.title.setStyleSheet("background-color: transparent; color: white; font-family: Segoe UI; font-size: 72px; font-weight: bold;")

        # --- subtitle
        self.subtitle = QLabel()
        self.subtitle.setWordWrap(True)

        self.subtitle.setText("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
        self.subtitle.setStyleSheet("background-color: transparent; color: white; font-family: Segoe UI; font-size: 24px; font-weight: 400;")

        # --- selection
        self.selection = QComboBox()

        self.selection.setStyleSheet("background-color: transparent;")

        themes = [
            "Dark",
            "Dark",
            "Dark",
            "Piss",
            "Dark",
            "Dark",
        ]

        self.selection.addItems(themes)

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

class AccountPage(QWidget):
    def __init__(self, stack):
        super().__init__()

        self.stack = stack
        self.usernameallowed = False

        # --- init style
        self.setStyleSheet("background-color: transparent;")

        # --- title
        self.title = QLabel("Create an account")
        self.title.setStyleSheet("background-color: transparent; color: white; font-family: Segoe UI; font-size: 72px; font-weight: bold;")

        # --- subtitle
        self.subtitle = QLabel()
        self.subtitle.setWordWrap(True)

        self.subtitle.setText("I don't have a good subtitle for this one, so fuck you. I bet you smell like crude oil.")
        self.subtitle.setStyleSheet("background-color: transparent; color: white; font-family: Segoe UI; font-size: 24px; font-weight: 400;")

        # --- account row
        self.accountrow = QHBoxLayout()
        self.accountrow.setContentsMargins(0, 0, 0, 0)
        self.accountrow.setSpacing(20)

        # --- account label
        self.accountlabel = QLabel("Username:")
        self.accountlabel.setStyleSheet("background-color: transparent; color: white; font-family: Segoe UI; font-size: 16px; font-weight: 400;")
        self.accountrow.addWidget(self.accountlabel)

        # --- username input
        self.username = QLineEdit()
        self.username.setStyleSheet("background-color: #15161a; color: white; font-family: Segoe UI; font-size: 16px; font-weight: 400;")
        self.username.textChanged.connect(self.username_changed)
        self.accountrow.addWidget(self.username)

        # --- status label
        self.statuslabel = QLabel("Username field is empty. Please enter a username to continue.")
        self.statuslabel.setStyleSheet("background-color: transparent; color: #ff6547; font-family: Segoe UI; font-size: 16px; font-weight: 400;")

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

        self.contentlayout.addLayout(self.accountrow)
        self.contentlayout.addWidget(self.statuslabel)

        self.contentlayout.addWidget(self.nextbtn)

        self.divlayout.addStretch()

    def next_page(self):
        if self.usernameallowed:
            next_index = self.stack.currentIndex() + 1
            self.stack.setCurrentIndex(next_index)
        else:
            pass

    def username_changed(self):
        global username1
        username1 = self.username.text()

        if username1 != "":
            if not username1.isalnum():
                self.statuslabel.setText("Username can only contain letters and numbers.")
                self.usernameallowed = False
            else:
                self.statuslabel.setText("")
                self.usernameallowed = True
        else:
            self.statuslabel.setText("Username field is empty. Please enter a username to continue.")
            self.usernameallowed = False

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
        self.pixmap = QPixmap("assets/CadenceAteThem.png")
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

        toWrite = {"username": username1}

        with open(config_path, "w") as f:
            json.dump(toWrite, f, indent=4)

        with open(license_path, "r") as f:
            license_data = json.load(f)

        license_data["flag"] = "sephiroth"

        with open(license_path, "w") as f:
            json.dump(license_data, f, indent=4)

        mainBus.restartRequested.emit()