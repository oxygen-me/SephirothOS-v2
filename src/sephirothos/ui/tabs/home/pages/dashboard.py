"""Home dashboard page."""

import logging
from datetime import datetime
from random import choice

from PySide6.QtCore import QThreadPool, QTimer
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from sephirothos.content.subtitles import HOME_SUBTITLES
from sephirothos.services.announcements import (
    AnnouncementFeed,
    AnnouncementService,
)
from sephirothos.ui.metrics import UiMetrics
from sephirothos.ui.roles import SurfaceRole, TextRole
from sephirothos.ui.tabs.home.pages.dashboard_cards import (
    AnnouncementsCard,
    QuoteCard,
    SystemStatusCard,
    TipCard,
)
from sephirothos.ui.workers import AnnouncementWorker

logger = logging.getLogger(__name__)


class DashboardPage(QWidget):
    """Primary Home dashboard."""

    def __init__(
        self,
        metrics: UiMetrics,
        announcement_service: AnnouncementService | None = None,
    ) -> None:
        super().__init__()

        self.metrics = metrics
        self.announcement_service = announcement_service or AnnouncementService()
        self._announcement_worker: AnnouncementWorker | None = None

        self.setProperty(
            "surfaceRole",
            SurfaceRole.TRANSPARENT.value,
        )

        self._build_ui()
        self._configure_clock()
        self._start_announcement_load()

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

        self.system_status_card = SystemStatusCard(
            self.metrics,
        )
        self.tip_card = TipCard(
            self.metrics,
        )
        self.quote_card = QuoteCard(
            self.metrics,
        )
        self.announcements_card = AnnouncementsCard(
            self.metrics,
        )

        # Entire area beneath the dashboard header.
        self.dashboard_layout = QHBoxLayout()
        self.dashboard_layout.setContentsMargins(0, 0, 0, 0)
        self.dashboard_layout.setSpacing(
            self.metrics.space_20,
        )

        # Left side: top and bottom card rows.
        self.left_column_layout = QVBoxLayout()
        self.left_column_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        self.left_column_layout.setSpacing(
            self.metrics.space_20,
        )

        self.top_left_layout = QHBoxLayout()
        self.top_left_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        self.top_left_layout.setSpacing(
            self.metrics.space_20,
        )

        self.bottom_left_layout = QHBoxLayout()
        self.bottom_left_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        self.bottom_left_layout.setSpacing(
            self.metrics.space_20,
        )

        # Right side: Performance and Storage will be added here.
        self.right_column_layout = QVBoxLayout()
        self.right_column_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        self.right_column_layout.setSpacing(
            self.metrics.space_20,
        )

        self.top_left_layout.addWidget(
            self.system_status_card,
            1,
        )
        self.top_left_layout.addWidget(
            self.tip_card,
            1,
        )
        self.top_left_layout.addWidget(
            self.quote_card,
            1,
        )

        self.bottom_left_layout.addWidget(
            self.announcements_card,
            1,
        )

        self.left_column_layout.addLayout(
            self.top_left_layout,
            1,
        )
        self.left_column_layout.addLayout(
            self.bottom_left_layout,
            1,
        )

        self.dashboard_layout.addLayout(
            self.left_column_layout,
            3,
        )
        self.dashboard_layout.addLayout(
            self.right_column_layout,
            1,
        )

        self.main_layout.addLayout(
            self.header_layout,
        )
        self.main_layout.addLayout(
            self.dashboard_layout,
            1,
        )

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

    def _start_announcement_load(self) -> None:
        worker = AnnouncementWorker(
            self.announcement_service,
        )
        worker.signals.loaded.connect(
            self._apply_announcement_feed,
        )
        worker.signals.failed.connect(
            self._handle_announcement_failure,
        )
        worker.signals.finished.connect(
            self._release_announcement_worker,
        )

        self._announcement_worker = worker

        QThreadPool.globalInstance().start(worker)

    def _apply_announcement_feed(
        self,
        feed: object,
    ) -> None:
        if not isinstance(feed, AnnouncementFeed):
            logger.error("Announcement worker returned an invalid result")
            return

        self.announcements_card.set_announcements(
            feed.announcements,
        )

        logger.info(
            "Loaded %d announcements from %s",
            len(feed.announcements),
            feed.source.value,
        )

    def _handle_announcement_failure(
        self,
        message: str,
    ) -> None:
        logger.warning(
            "Announcements are unavailable: %s",
            message,
        )

    def _release_announcement_worker(self) -> None:
        self._announcement_worker = None
