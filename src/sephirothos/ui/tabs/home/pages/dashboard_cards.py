"""Cards displayed on the Home dashboard."""

from __future__ import annotations

from collections.abc import Sequence
from random import choice, randrange

from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from sephirothos.content.quotes import QUOTES, Quote
from sephirothos.content.tips import TIPS
from sephirothos.ui.metrics import UiMetrics
from sephirothos.ui.roles import (
    ButtonVariant,
    DividerRole,
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
