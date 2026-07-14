"""Cards displayed on the Home dashboard."""

from __future__ import annotations

from collections.abc import Sequence
from random import choice, randrange

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from sephirothos.content.quotes import QUOTES, Quote
from sephirothos.content.tips import TIPS
from sephirothos.services.announcements import Announcement
from sephirothos.services.performance import (
    PerformanceSnapshot,
)
from sephirothos.services.storage import StorageSnapshot
from sephirothos.ui.metrics import UiMetrics
from sephirothos.ui.roles import (
    ButtonVariant,
    DividerRole,
    ProgressRole,
    ProgressVariant,
    ScrollRole,
    SurfaceRole,
    TextRole,
)
from sephirothos.ui.widgets.card import Card


class SystemStatusCard(Card):
    """Display SephirothOS's highly scientific system assessment."""

    def __init__(
        self,
        metrics: UiMetrics,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(metrics, parent)

        self._build_ui(metrics)

    def _build_ui(self, metrics: UiMetrics) -> None:
        self.title_label = QLabel("System Status")
        self.title_label.setProperty(
            "textRole",
            TextRole.CARD_TITLE.value,
        )

        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(metrics.space_10)

        for status in (
            "Running",
            "Chud-Like in Nature",
            "Mining Bitcoin",
        ):
            status_label = QLabel(status)
            status_label.setProperty(
                "textRole",
                TextRole.BODY.value,
            )
            self.content_layout.addWidget(status_label)

        self.divider = QFrame()
        self.divider.setFrameShape(QFrame.Shape.NoFrame)
        self.divider.setProperty(
            "dividerRole",
            DividerRole.DEFAULT.value,
        )
        self.divider.setFixedHeight(metrics.border_thin)

        self.footer_layout = QHBoxLayout()
        self.footer_layout.setContentsMargins(0, 0, 0, 0)
        self.footer_layout.setSpacing(metrics.space_10)

        self.checked_label = QLabel("Last checked: just now")
        self.checked_label.setProperty(
            "textRole",
            TextRole.CAPTION.value,
        )

        self.check_button = QPushButton("Check Again")
        self.check_button.setProperty(
            "buttonVariant",
            ButtonVariant.CARD_ACTION.value,
        )

        self.footer_layout.addWidget(self.checked_label)
        self.footer_layout.addStretch()
        self.footer_layout.addWidget(self.check_button)

        self.main_layout.addWidget(self.title_label)
        self.main_layout.addLayout(self.content_layout)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.divider)
        self.main_layout.addLayout(self.footer_layout)


class TipCard(Card):
    """Cycle through helpful and questionably helpful application tips."""

    def __init__(
        self,
        metrics: UiMetrics,
        parent: QWidget | None = None,
        *,
        tips: Sequence[str] = TIPS,
    ) -> None:
        super().__init__(metrics, parent)

        self._tips = tuple(tips)

        if not self._tips:
            raise ValueError("TipCard requires at least one tip.")

        self._tip_index = randrange(len(self._tips))

        self._build_ui(metrics)
        self._display_current_tip()

    def _build_ui(self, metrics: UiMetrics) -> None:
        self.title_label = QLabel("Daily Tip")
        self.title_label.setProperty(
            "textRole",
            TextRole.CARD_TITLE.value,
        )

        self.tip_label = QLabel()
        self.tip_label.setWordWrap(True)
        self.tip_label.setProperty(
            "textRole",
            TextRole.BODY.value,
        )

        self.divider = QFrame()
        self.divider.setFrameShape(QFrame.Shape.NoFrame)
        self.divider.setProperty(
            "dividerRole",
            DividerRole.DEFAULT.value,
        )
        self.divider.setFixedHeight(metrics.border_thin)

        self.footer_layout = QHBoxLayout()
        self.footer_layout.setContentsMargins(0, 0, 0, 0)
        self.footer_layout.setSpacing(metrics.space_10)

        self.tip_number_label = QLabel()
        self.tip_number_label.setProperty(
            "textRole",
            TextRole.CAPTION.value,
        )

        self.next_tip_button = QPushButton("Next Tip")
        self.next_tip_button.setProperty(
            "buttonVariant",
            ButtonVariant.CARD_ACTION.value,
        )
        self.next_tip_button.clicked.connect(
            self._show_next_tip,
        )

        self.footer_layout.addWidget(self.tip_number_label)
        self.footer_layout.addStretch()
        self.footer_layout.addWidget(self.next_tip_button)

        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.tip_label)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.divider)
        self.main_layout.addLayout(self.footer_layout)

    def _show_next_tip(self) -> None:
        self._tip_index = (self._tip_index + 1) % len(self._tips)
        self._display_current_tip()

    def _display_current_tip(self) -> None:
        self.tip_label.setText(
            self._tips[self._tip_index],
        )
        self.tip_number_label.setText(
            f"Tip #{self._tip_index + 1}",
        )


class QuoteCard(Card):
    """Display a randomly selected attributed quote."""

    def __init__(
        self,
        metrics: UiMetrics,
        parent: QWidget | None = None,
        *,
        quotes: Sequence[Quote] = QUOTES,
    ) -> None:
        super().__init__(metrics, parent)

        self._quotes = tuple(quotes)

        if not self._quotes:
            raise ValueError("QuoteCard requires at least one quote.")

        self._quote = choice(self._quotes)

        self._build_ui(metrics)

    def _build_ui(self, metrics: UiMetrics) -> None:
        self.title_label = QLabel("Quote of the Day")
        self.title_label.setProperty(
            "textRole",
            TextRole.CARD_TITLE.value,
        )

        self.quote_label = QLabel(
            f'"{self._quote.text}"',
        )
        self.quote_label.setWordWrap(True)
        self.quote_label.setProperty(
            "textRole",
            TextRole.BODY.value,
        )

        self.author_label = QLabel(
            f"– {self._quote.author}",
        )
        self.author_label.setProperty(
            "textRole",
            TextRole.BODY.value,
        )

        self.divider = QFrame()
        self.divider.setFrameShape(QFrame.Shape.NoFrame)
        self.divider.setProperty(
            "dividerRole",
            DividerRole.DEFAULT.value,
        )
        self.divider.setFixedHeight(metrics.border_thin)

        self.footer_layout = QHBoxLayout()
        self.footer_layout.setContentsMargins(0, 0, 0, 0)
        self.footer_layout.setSpacing(metrics.space_10)

        self.inspire_button = QPushButton("Inspire Me")
        self.inspire_button.setProperty(
            "buttonVariant",
            ButtonVariant.CARD_ACTION.value,
        )

        self.footer_layout.addStretch()
        self.footer_layout.addWidget(self.inspire_button)

        self.main_layout.addWidget(self.title_label)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.quote_label)
        self.main_layout.addWidget(self.author_label)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.divider)
        self.main_layout.addLayout(self.footer_layout)


MAX_VISIBLE_ANNOUNCEMENTS = 10


class _AnnouncementEntry(QWidget):
    """Visual representation of one dashboard announcement."""

    def __init__(
        self,
        announcement: Announcement,
        metrics: UiMetrics,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.setProperty(
            "surfaceRole",
            SurfaceRole.TRANSPARENT.value,
        )

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(metrics.space_5)

        self.title_label = QLabel(announcement.title)
        self.title_label.setWordWrap(True)
        self.title_label.setProperty(
            "textRole",
            TextRole.BODY.value,
        )

        self.body_label = QLabel(announcement.body)
        self.body_label.setWordWrap(True)
        self.body_label.setProperty(
            "textRole",
            TextRole.BODY_MUTED.value,
        )

        local_time = announcement.published_at.astimezone()
        formatted_date = local_time.strftime(
            "%B %d, %Y",
        ).replace(" 0", " ")

        self.date_label = QLabel(formatted_date)
        self.date_label.setProperty(
            "textRole",
            TextRole.CAPTION.value,
        )

        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.body_label)
        self.main_layout.addWidget(self.date_label)


class AnnouncementsCard(Card):
    """Display the ten newest applicable announcements."""

    view_all_requested = Signal()

    def __init__(
        self,
        metrics: UiMetrics,
        announcements: Sequence[Announcement] = (),
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(metrics, parent)

        self._metrics = metrics
        self._announcements: tuple[Announcement, ...] = ()

        self._build_ui(self._metrics)
        self.set_announcements(announcements)

    def _build_ui(self, metrics: UiMetrics) -> None:
        self.title_label = QLabel("Announcements")
        self.title_label.setProperty(
            "textRole",
            TextRole.CARD_TITLE.value,
        )

        self.scroll_area = QScrollArea()
        self.scroll_area.setProperty(
            "scrollRole",
            ScrollRole.DEFAULT.value,
        )
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff,
        )
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded,
        )

        self.scroll_content = QWidget()
        self.scroll_content.setProperty(
            "surfaceRole",
            SurfaceRole.TRANSPARENT.value,
        )

        self.announcement_layout = QVBoxLayout(
            self.scroll_content,
        )
        self.announcement_layout.setContentsMargins(
            0,
            0,
            self._metrics.space_5,
            0,
        )
        self.announcement_layout.setSpacing(
            self._metrics.space_15,
        )

        self.scroll_area.setWidget(self.scroll_content)

        self.footer_layout = QHBoxLayout()
        self.footer_layout.setContentsMargins(0, 0, 0, 0)
        self.footer_layout.setSpacing(
            self._metrics.space_10,
        )

        self.view_all_button = QPushButton(
            "View all announcements",
        )
        self.view_all_button.setProperty(
            "buttonVariant",
            ButtonVariant.LINK.value,
        )
        self.view_all_button.setCursor(
            Qt.CursorShape.PointingHandCursor,
        )
        self.view_all_button.clicked.connect(
            self.view_all_requested.emit,
        )

        self.footer_layout.addWidget(self.view_all_button)
        self.footer_layout.addStretch()

        self.footer_divider = QFrame()
        self.footer_divider.setFrameShape(QFrame.Shape.NoFrame)
        self.footer_divider.setProperty(
            "dividerRole",
            DividerRole.DEFAULT.value,
        )
        self.footer_divider.setFixedHeight(metrics.border_thin)

        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.scroll_area, 1)
        self.main_layout.addWidget(self.footer_divider)
        self.main_layout.addLayout(self.footer_layout)

    def set_announcements(
        self,
        announcements: Sequence[Announcement],
    ) -> None:
        """Replace the announcements displayed by the card."""

        self._announcements = tuple(announcements)
        self._clear_announcement_layout()

        visible_announcements = self._announcements[:MAX_VISIBLE_ANNOUNCEMENTS]

        if not visible_announcements:
            empty_label = QLabel("No announcements available.")
            empty_label.setProperty(
                "textRole",
                TextRole.BODY_MUTED.value,
            )
            self.announcement_layout.addWidget(empty_label)
        else:
            for index, announcement in enumerate(
                visible_announcements,
            ):
                entry = _AnnouncementEntry(
                    announcement,
                    self._metrics,
                )
                self.announcement_layout.addWidget(entry)

                if index < len(visible_announcements) - 1:
                    divider = QFrame()
                    divider.setFrameShape(QFrame.Shape.NoFrame)
                    divider.setProperty(
                        "dividerRole",
                        DividerRole.DEFAULT.value,
                    )
                    divider.setFixedHeight(
                        self._metrics.border_thin,
                    )
                    self.announcement_layout.addWidget(divider)

        self.announcement_layout.addStretch()

    def _clear_announcement_layout(self) -> None:
        while self.announcement_layout.count():
            item = self.announcement_layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.deleteLater()


class TopAppsCard(Card):
    """Display frequently used SephirothOS applications."""

    def __init__(
        self,
        metrics: UiMetrics,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(metrics, parent)

        self._build_ui(metrics)

    def _build_ui(self, metrics: UiMetrics) -> None:
        self.title_label = QLabel("Top Apps")
        self.title_label.setProperty(
            "textRole",
            TextRole.CARD_TITLE.value,
        )

        self.placeholder_label = QLabel("No app has earned the right to be here yet.")
        self.placeholder_label.setWordWrap(True)
        self.placeholder_label.setProperty(
            "textRole",
            TextRole.BODY_MUTED.value,
        )

        self.footer_layout = QHBoxLayout()
        self.footer_layout.setContentsMargins(0, 0, 0, 0)
        self.footer_layout.setSpacing(0)

        self.browse_apps_button = QPushButton("Browse All Apps")
        self.browse_apps_button.setProperty(
            "buttonVariant",
            ButtonVariant.LINK.value,
        )
        self.browse_apps_button.setCursor(
            Qt.CursorShape.PointingHandCursor,
        )

        self.footer_layout.addWidget(self.browse_apps_button)
        self.footer_layout.addStretch()

        self.footer_divider = QFrame()
        self.footer_divider.setFrameShape(QFrame.Shape.NoFrame)
        self.footer_divider.setProperty(
            "dividerRole",
            DividerRole.DEFAULT.value,
        )
        self.footer_divider.setFixedHeight(metrics.border_thin)

        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.placeholder_label)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.footer_divider)
        self.main_layout.addLayout(self.footer_layout)


class StorageCard(Card):
    """Display capacity information for the system drive."""

    def __init__(
        self,
        metrics: UiMetrics,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(metrics, parent)

        self._build_ui(metrics)

    def _build_ui(self, metrics: UiMetrics) -> None:
        self.title_label = QLabel("Storage")
        self.title_label.setProperty(
            "textRole",
            TextRole.CARD_TITLE.value,
        )

        self.drive_label = QLabel("Loading storage information...")
        self.drive_label.setProperty(
            "textRole",
            TextRole.BODY.value,
        )

        self.usage_bar = QProgressBar()
        self.usage_bar.setRange(0, 100)
        self.usage_bar.setValue(0)
        self.usage_bar.setTextVisible(False)
        self.usage_bar.setProperty(
            "progressRole",
            ProgressRole.DEFAULT.value,
        )

        self.information_layout = QHBoxLayout()
        self.information_layout.setContentsMargins(0, 0, 0, 0)
        self.information_layout.setSpacing(0)

        self.capacity_label = QLabel()
        self.capacity_label.setProperty(
            "textRole",
            TextRole.CAPTION.value,
        )

        self.percentage_label = QLabel()
        self.percentage_label.setProperty(
            "textRole",
            TextRole.BODY.value,
        )

        self.information_layout.addWidget(self.capacity_label)
        self.information_layout.addStretch()
        self.information_layout.addWidget(self.percentage_label)

        self.footer_layout = QHBoxLayout()
        self.footer_layout.setContentsMargins(0, 0, 0, 0)
        self.footer_layout.setSpacing(0)

        self.disk_management_button = QPushButton("Disk Management")
        self.disk_management_button.setProperty(
            "buttonVariant",
            ButtonVariant.LINK.value,
        )
        self.disk_management_button.setCursor(
            Qt.CursorShape.PointingHandCursor,
        )

        self.footer_layout.addWidget(
            self.disk_management_button,
        )
        self.footer_layout.addStretch()

        self.footer_divider = QFrame()
        self.footer_divider.setFrameShape(QFrame.Shape.NoFrame)
        self.footer_divider.setProperty(
            "dividerRole",
            DividerRole.DEFAULT.value,
        )
        self.footer_divider.setFixedHeight(metrics.border_thin)

        self.main_layout.addWidget(self.title_label)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.drive_label)
        self.main_layout.addWidget(self.usage_bar)
        self.main_layout.addLayout(self.information_layout)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.footer_divider)
        self.main_layout.addLayout(self.footer_layout)

    def set_storage(
        self,
        snapshot: StorageSnapshot,
    ) -> None:
        """Display a new storage snapshot."""

        self.drive_label.setText(
            str(snapshot.root) + " (Your Mom's House)",
        )
        self.capacity_label.setText(
            f"{snapshot.free_gibibytes:.1f} GiB free of {snapshot.total_gibibytes:.1f} GiB"
        )
        self.percentage_label.setText(f"{snapshot.used_percentage:.1f}%")
        self.usage_bar.setValue(round(snapshot.used_percentage))


class _PerformanceMetric(QWidget):
    """One labelled performance percentage and progress bar."""

    def __init__(
        self,
        title: str,
        caption: str,
        metrics: UiMetrics,
        variant: ProgressVariant,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.setProperty(
            "surfaceRole",
            SurfaceRole.TRANSPARENT.value,
        )

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.header_layout = QHBoxLayout()
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        self.header_layout.setSpacing(0)

        self.label_layout = QVBoxLayout()
        self.label_layout.setContentsMargins(0, 0, 0, 0)
        self.label_layout.setSpacing(0)

        self.title_label = QLabel(title)
        self.title_label.setProperty(
            "textRole",
            TextRole.BODY.value,
        )

        self.caption_label = QLabel(caption)
        self.caption_label.setProperty(
            "textRole",
            TextRole.CAPTION.value,
        )

        self.value_label = QLabel("—")
        self.value_label.setProperty(
            "textRole",
            TextRole.BODY.value,
        )

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setProperty(
            "progressRole",
            ProgressRole.DEFAULT.value,
        )
        self.progress_bar.setProperty(
            "progressVariant",
            variant.value,
        )

        self.label_layout.addWidget(self.title_label)
        self.label_layout.addWidget(self.caption_label)

        self.header_layout.addLayout(self.label_layout)
        self.header_layout.addStretch()
        self.header_layout.addWidget(
            self.value_label,
            alignment=Qt.AlignmentFlag.AlignRight,
        )

        self.main_layout.addLayout(self.header_layout)
        self.main_layout.addSpacing(metrics.space_10)
        self.main_layout.addWidget(self.progress_bar)
        self.main_layout.addStretch()

    def set_percentage(self, percentage: float) -> None:
        self.value_label.setText(f"{percentage:.1f}%")
        self.progress_bar.setValue(round(percentage))


class PerformanceCard(Card):
    """Display live system performance information."""

    def __init__(
        self,
        metrics: UiMetrics,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(metrics, parent)

        self._build_ui(metrics)

    def _build_ui(self, metrics: UiMetrics) -> None:
        self.title_label = QLabel("Performance")
        self.title_label.setProperty(
            "textRole",
            TextRole.CARD_TITLE.value,
        )

        self.divider = QFrame()
        self.divider.setFrameShape(QFrame.Shape.NoFrame)
        self.divider.setProperty(
            "dividerRole",
            DividerRole.DEFAULT.value,
        )
        self.divider.setFixedHeight(metrics.border_thin)

        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        self.cpu_metric = _PerformanceMetric(
            "CPU Usage",
            "Thinking very hard. Hahaha. Hard...",
            metrics,
            ProgressVariant.CPU,
        )

        self.memory_metric = _PerformanceMetric(
            "RAM",
            "Apparently enough to run this.",
            metrics,
            ProgressVariant.MEMORY,
        )

        self.disk_metric = _PerformanceMetric(
            "Disk",
            "I am selling your data as we speak.",
            metrics,
            ProgressVariant.DISK,
        )

        self.piss_metric = _PerformanceMetric(
            "Piss",
            "Bottom text",
            metrics,
            ProgressVariant.PISS,
        )

        self.content_layout.addWidget(self.cpu_metric, 1)
        self.content_layout.addWidget(self.memory_metric, 1)
        self.content_layout.addWidget(self.disk_metric, 1)
        self.content_layout.addWidget(self.piss_metric, 1)

        self.footer_layout = QHBoxLayout()
        self.footer_layout.setContentsMargins(0, 0, 0, 0)
        self.footer_layout.setSpacing(0)

        self.performance_monitor_button = QPushButton("Open Performance Monitor")
        self.performance_monitor_button.setProperty(
            "buttonVariant",
            ButtonVariant.LINK.value,
        )
        self.performance_monitor_button.setCursor(
            Qt.CursorShape.PointingHandCursor,
        )

        self.footer_layout.addWidget(
            self.performance_monitor_button,
        )
        self.footer_layout.addStretch()

        self.footer_divider = QFrame()
        self.footer_divider.setFrameShape(QFrame.Shape.NoFrame)
        self.footer_divider.setProperty(
            "dividerRole",
            DividerRole.DEFAULT.value,
        )
        self.footer_divider.setFixedHeight(metrics.border_thin)

        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.divider)
        self.main_layout.addLayout(self.content_layout, 1)
        self.main_layout.addWidget(self.footer_divider)
        self.main_layout.addLayout(self.footer_layout)

    def set_performance(
        self,
        snapshot: PerformanceSnapshot,
    ) -> None:
        """Display a new performance snapshot."""

        self.cpu_metric.set_percentage(
            snapshot.cpu_percentage,
        )
        self.memory_metric.set_percentage(
            snapshot.memory_percentage,
        )
        self.disk_metric.set_percentage(
            snapshot.disk_activity_percentage,
        )
        self.piss_metric.set_percentage(
            snapshot.piss_percentage,
        )
