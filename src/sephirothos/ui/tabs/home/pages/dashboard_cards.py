"""Cards displayed on the Home dashboard."""

from __future__ import annotations

from collections.abc import Sequence
from random import choice, randrange

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from sephirothos.content.quotes import QUOTES, Quote
from sephirothos.content.tips import TIPS
from sephirothos.services.announcements import Announcement
from sephirothos.ui.metrics import UiMetrics
from sephirothos.ui.roles import (
    ButtonVariant,
    DividerRole,
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

        self._build_ui()
        self.set_announcements(announcements)

    def _build_ui(self) -> None:
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

        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.scroll_area, 1)
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
