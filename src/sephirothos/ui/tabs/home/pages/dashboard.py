"""Home dashboard page."""

from datetime import datetime
from random import choice

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from sephirothos.content.subtitles import HOME_SUBTITLES
from sephirothos.ui.metrics import UiMetrics
from sephirothos.ui.roles import SurfaceRole, TextRole
from sephirothos.ui.tabs.home.pages.dashboard_cards import QuoteCard, SystemStatusCard, TipCard


class DashboardPage(QWidget):
    """Primary Home dashboard."""

    def __init__(self, metrics: UiMetrics) -> None:
        super().__init__()

        self.metrics = metrics

        self.setProperty(
            "surfaceRole",
            SurfaceRole.TRANSPARENT.value,
        )

        self._build_ui()
        self._configure_clock()

    def _build_ui(self) -> None:
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(
            self.metrics.space_20,
            self.metrics.space_20,
            self.metrics.space_20,
            self.metrics.space_20,
        )
        self.main_layout.setSpacing(
            self.metrics.space_20,
        )

        self.header_layout = QHBoxLayout()
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        self.header_layout.setSpacing(
            self.metrics.space_20,
        )

        self.title_layout = QVBoxLayout()
        self.title_layout.setContentsMargins(0, 0, 0, 0)
        self.title_layout.setSpacing(
            self.metrics.space_10,
        )

        self.title_label = QLabel("Welcome to Sephiroth's House")
        self.title_label.setProperty(
            "textRole",
            TextRole.PAGE_TITLE.value,
        )

        self.subtitle_label = QLabel(choice(HOME_SUBTITLES))
        self.subtitle_label.setProperty(
            "textRole",
            TextRole.PAGE_SUBTITLE.value,
        )

        self.clock_layout = QVBoxLayout()
        self.clock_layout.setContentsMargins(0, 0, 0, 0)
        self.clock_layout.setSpacing(
            self.metrics.space_10,
        )

        self.time_label = QLabel()
        self.time_label.setProperty(
            "textRole",
            TextRole.PAGE_TITLE.value,
        )

        self.date_label = QLabel()
        self.date_label.setProperty(
            "textRole",
            TextRole.PAGE_SUBTITLE.value,
        )

        self.title_layout.addWidget(self.title_label)
        self.title_layout.addWidget(self.subtitle_label)

        self.clock_layout.addWidget(self.time_label)
        self.clock_layout.addWidget(self.date_label)

        self.header_layout.addLayout(self.title_layout)
        self.header_layout.addStretch()
        self.header_layout.addLayout(self.clock_layout)

        self.system_status_card = SystemStatusCard(self.metrics)
        self.tip_card = TipCard(self.metrics)
        self.quote_card = QuoteCard(self.metrics)

        self.card_layout = QHBoxLayout()
        self.card_layout.setContentsMargins(0, 0, 0, 0)
        self.card_layout.setSpacing(self.metrics.space_20)

        self.card_layout.addWidget(self.system_status_card, 1)
        self.card_layout.addWidget(self.tip_card, 1)
        self.card_layout.addWidget(self.quote_card, 1)

        self.main_layout.addLayout(self.header_layout)
        self.main_layout.addLayout(self.card_layout)
        self.main_layout.addStretch()

    def _configure_clock(self) -> None:
        self.clock_timer = QTimer(self)
        self.clock_timer.setInterval(1000)
        self.clock_timer.timeout.connect(
            self._update_clock,
        )

        self._update_clock()
        self.clock_timer.start()

    def _update_clock(self) -> None:
        now = datetime.now()

        formatted_time = now.strftime("%I:%M %p").lstrip("0")
        formatted_date = now.strftime("%A, %B %d, %Y").replace(" 0", " ")

        self.time_label.setText(formatted_time)
        self.date_label.setText(formatted_date)
