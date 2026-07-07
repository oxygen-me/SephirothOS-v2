# --- imports
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit

# --- create finishpage class
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