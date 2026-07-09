# --- imports
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea, \
    QButtonGroup, QLineEdit
from PySide6.QtCore import Qt

from utils.themes import styles, tlib


# --- create languagepage class
class PersonalizationPage(QWidget):
    def __init__(self, stack):
        super().__init__()

        self.stack = stack

        # --- init style
        self.setStyleSheet("background-color: transparent;")

        # --- make titlebox
        self.titlebox = QVBoxLayout()
        self.titlebox.setContentsMargins(0, 0, 0, 0)
        self.titlebox.setSpacing(10)

        # --- title
        self.title = QLabel("Language")
        self.title.setStyleSheet(styles.w_title2(tlib.CURRENT))
        self.titlebox.addWidget(self.title)

        # --- subtitle
        self.subtitle = QLabel('Quoth the Roth, "seaux de pisse."')
        self.subtitle.setStyleSheet(styles.w_subtitle2(tlib.CURRENT))
        self.titlebox.addWidget(self.subtitle)

        self.titlebox.addStretch()

        # --- selection
        self.selectionscroll = QScrollArea()
        self.selectionscroll.setWidgetResizable(True)

        self.selectionscroll.setStyleSheet(styles.d_scroll(tlib.CURRENT))
        self.selectionscroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.selectionscroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.selectioncard = QWidget()
        self.selectioncard.setStyleSheet(styles.c_widget(tlib.CURRENT))

        self.layout = QVBoxLayout(self.selectioncard)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(0)

        self.group = QButtonGroup(self)

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

        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Search languages...")
        self.searchbar.setFixedHeight(40)
        self.searchbar.setStyleSheet(styles.d_sbar(tlib.CURRENT))

        self.layout.addWidget(self.searchbar)
        self.layout.addSpacing(10)

        self.group.setExclusive(True)
        self.language_buttons = []

        for lang in languages:
            btn = QPushButton(lang)
            btn.setFixedHeight(40)
            btn.setCheckable(True)
            btn.setStyleSheet(styles.o_btn(tlib.CURRENT))

            self.layout.addWidget(btn)
            self.group.addButton(btn)
            self.language_buttons.append(btn)

        self.layout.addStretch()
        self.selectionscroll.setWidget(self.selectioncard)

        self.language_buttons[0].setChecked(True)

        self.searchbar.textChanged.connect(self.filter_languages)

        # --- preview
        self.previewcard = QWidget()
        self.previewcard.setStyleSheet(styles.c_widget(tlib.CURRENT))

        self.previewlayout = QVBoxLayout()
        self.previewlayout.setContentsMargins(20, 20, 20, 20)
        self.previewlayout.setSpacing(10)

        self.previewtitle = QLabel("Preview")
        self.previewtitle.setStyleSheet(styles.a_subtitle(tlib.CURRENT))
        self.previewlayout.addWidget(self.previewtitle)

        self.previewsubtitle = QLabel("This is how SephirothOS will look.")
        self.previewsubtitle.setStyleSheet(styles.p_subtitle(tlib.CURRENT))
        self.previewlayout.addWidget(self.previewsubtitle)

        self.viewcard = QWidget()
        self.viewcard.setStyleSheet(styles.d_widget(tlib.CURRENT))

        self.viewlayout = QVBoxLayout(self.viewcard)
        self.viewlayout.setContentsMargins(0, 0, 0, 0)
        self.viewlayout.setSpacing(0)
        self.viewlayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.viewtitle = QLabel("PISS")
        self.viewtitle.setStyleSheet(styles.w_title(tlib.CURRENT))
        self.viewlayout.addWidget(self.viewtitle)

        self.viewcard.setLayout(self.viewlayout)
        self.previewlayout.addSpacing(10)
        self.previewlayout.addWidget(self.viewcard, 1)
        self.previewcard.setLayout(self.previewlayout)

        # --- note
        self.notecard = QWidget()
        self.notecard.setStyleSheet(styles.c_widget(tlib.CURRENT))

        self.notelayout = QVBoxLayout(self.notecard)
        self.notelayout.setContentsMargins(20, 20, 20, 20)
        self.notelayout.setSpacing(10)
        self.notecard.setLayout(self.notelayout)

        self.notetitle = QLabel("Note")
        self.notetitle.setStyleSheet(styles.a_subtitle(tlib.CURRENT))
        self.notelayout.addWidget(self.notetitle)

        self.notesubtitle = QLabel("Don't worry! All of these are 100% real languages.\n"
                                   "We definitely have transgenders.")
        self.notesubtitle.setStyleSheet(styles.p_subtitle(tlib.CURRENT))
        self.notelayout.addWidget(self.notesubtitle)

        self.notelayout.addStretch()

        # --- main layout
        self.mainlayout = QVBoxLayout()
        self.mainlayout.setContentsMargins(20, 20, 20, 20)
        self.mainlayout.setSpacing(20)

        # --- hlayout
        self.hlayout = QHBoxLayout()
        self.hlayout.setContentsMargins(0, 0, 0, 0)
        self.hlayout.setSpacing(20)

        # --- right layout
        self.rightlayout = QVBoxLayout()
        self.rightlayout.setContentsMargins(0, 0, 0, 0)
        self.rightlayout.setSpacing(20)

        # --- assembly
        self.setLayout(self.mainlayout)
        self.mainlayout.addLayout(self.titlebox)

        self.mainlayout.addLayout(self.hlayout, 1)
        self.hlayout.addWidget(self.selectionscroll, 1)
        self.hlayout.addLayout(self.rightlayout, 1)

        self.rightlayout.addWidget(self.previewcard, 4)
        self.rightlayout.addWidget(self.notecard, 1)

    def next_page(self):
        next_index = self.stack.currentIndex() + 1
        self.stack.setCurrentIndex(next_index)

    def filter_languages(self, text):
        text = text.lower().strip()

        for btn in self.language_buttons:
            btn.setVisible(text in btn.text().lower())