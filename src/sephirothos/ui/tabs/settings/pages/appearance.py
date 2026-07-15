"""Appearance settings page."""

from __future__ import annotations

from dataclasses import replace

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from sephirothos.config import AppearanceConfig
from sephirothos.ui.metrics import UiMetrics
from sephirothos.ui.roles import (
    ButtonVariant,
    ScrollRole,
    SurfaceRole,
    TextRole,
)
from sephirothos.ui.tabs.settings.pages.appearance_cards import (
    AccentSelectionCard,
    AppearancePreviewCard,
    DisplayScaleCard,
    ExtraSettingsCard,
    FontSelectionCard,
    ThemeCreatorCard,
    ThemeSelectionCard,
)


class AppearancePage(QWidget):
    """Display and edit application appearance settings."""

    draft_changed = Signal(object)
    apply_requested = Signal(object)

    def __init__(
        self,
        metrics: UiMetrics,
        appearance: AppearanceConfig,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.metrics = metrics
        self._saved = replace(appearance)
        self._draft = replace(appearance)

        self.setProperty(
            "surfaceRole",
            SurfaceRole.TRANSPARENT.value,
        )

        self._build_ui()
        self._connect_events()

    @property
    def draft(self) -> AppearanceConfig:
        """Return a copy of the current uncommitted appearance."""

        return replace(self._draft)

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

        self.title_label = QLabel("Appearance")
        self.title_label.setProperty(
            "textRole",
            TextRole.PAGE_TITLE.value,
        )

        self.subtitle_label = QLabel("Customize how SephirothOS looks and feels.")
        self.subtitle_label.setProperty(
            "textRole",
            TextRole.PAGE_SUBTITLE.value,
        )

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setProperty(
            "scrollRole",
            ScrollRole.DEFAULT.value,
        )

        self.scroll_content = QWidget()
        self.scroll_content.setProperty(
            "surfaceRole",
            SurfaceRole.TRANSPARENT.value,
        )

        self.card_layout = QVBoxLayout(
            self.scroll_content,
        )
        self.card_layout.setContentsMargins(
            0,
            0,
            self.metrics.space_10,
            0,
        )
        self.card_layout.setSpacing(
            self.metrics.space_20,
        )

        self.top_row_layout = QHBoxLayout()
        self.top_row_layout.setContentsMargins(0, 0, 0, 0)
        self.top_row_layout.setSpacing(
            self.metrics.space_20,
        )

        self.middle_row_layout = QHBoxLayout()
        self.middle_row_layout.setContentsMargins(0, 0, 0, 0)
        self.middle_row_layout.setSpacing(
            self.metrics.space_20,
        )

        self.bottom_row_layout = QHBoxLayout()
        self.bottom_row_layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_row_layout.setSpacing(
            self.metrics.space_20,
        )

        self.theme_card = ThemeSelectionCard(
            metrics=self.metrics,
            current_theme=self._draft.theme_id,
        )
        self.preview_card = AppearancePreviewCard(
            metrics=self.metrics,
            appearance=self._draft,
        )

        self.theme_card.setMinimumHeight(
            self.metrics.appearance_feature_card_height,
        )
        self.preview_card.setMinimumHeight(
            self.metrics.appearance_feature_card_height,
        )

        self.accent_card = AccentSelectionCard(
            metrics=self.metrics,
            current_accent=self._draft.accent_id,
        )
        self.scale_card = DisplayScaleCard(
            metrics=self.metrics,
            current_scale=self._draft.display_scale,
        )
        self.font_card = FontSelectionCard(
            metrics=self.metrics,
            current_font=self._draft.font_family,
        )
        self.extra_settings_card = ExtraSettingsCard(
            metrics=self.metrics,
        )
        self.theme_creator_card = ThemeCreatorCard(
            metrics=self.metrics,
        )

        self.top_row_layout.addWidget(
            self.theme_card,
            2,
        )
        self.top_row_layout.addWidget(
            self.preview_card,
            3,
        )

        self.middle_row_layout.addWidget(
            self.accent_card,
            3,
        )
        self.middle_row_layout.addWidget(
            self.scale_card,
            2,
        )

        self.bottom_row_layout.addWidget(
            self.font_card,
            2,
        )
        self.bottom_row_layout.addWidget(
            self.extra_settings_card,
            3,
        )

        self.card_layout.addLayout(
            self.top_row_layout,
        )
        self.card_layout.addLayout(
            self.middle_row_layout,
        )
        self.card_layout.addLayout(
            self.bottom_row_layout,
        )
        self.card_layout.addWidget(
            self.theme_creator_card,
        )
        self.card_layout.addStretch()

        self.scroll_area.setWidget(
            self.scroll_content,
        )

        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.subtitle_label)
        self.main_layout.addWidget(
            self.scroll_area,
            1,
        )

        self.apply_layout = QHBoxLayout()
        self.apply_layout.setContentsMargins(0, 0, 0, 0)
        self.apply_layout.setSpacing(
            self.metrics.space_20,
        )

        self.apply_status_label = QLabel()
        self.apply_status_label.setProperty(
            "textRole",
            TextRole.CAPTION.value,
        )

        self.apply_button = QPushButton("Apply")
        self.apply_button.setProperty(
            "buttonVariant",
            ButtonVariant.PRIMARY.value,
        )
        self.apply_button.setMinimumWidth(
            self.metrics.space_50 * 2,
        )
        self.apply_button.setEnabled(False)

        self.apply_layout.addWidget(
            self.apply_status_label,
        )
        self.apply_layout.addStretch()
        self.apply_layout.addWidget(
            self.apply_button,
        )

        self.main_layout.addLayout(
            self.apply_layout,
        )

        self.apply_button.clicked.connect(
            self._request_apply,
        )

    def _connect_events(self) -> None:
        self.theme_card.theme_selected.connect(
            self._set_theme,
        )
        self.accent_card.accent_selected.connect(
            self._set_accent,
        )
        self.scale_card.scale_selected.connect(
            self._set_scale,
        )
        self.font_card.font_selected.connect(
            self._set_font,
        )
        self.draft_changed.connect(
            self.preview_card.set_appearance,
        )

    def _set_theme(
        self,
        theme_id: str,
    ) -> None:
        self._replace_draft(
            theme_id=theme_id,
        )

    def _set_accent(
        self,
        accent_id: str,
    ) -> None:
        self._replace_draft(
            accent_id=accent_id,
        )

    def _replace_draft(
        self,
        **changes: object,
    ) -> None:
        updated = replace(
            self._draft,
            **changes,
        )

        if updated == self._draft:
            return

        self._draft = updated

        self.apply_status_label.clear()
        self.apply_button.setEnabled(
            self._draft != self._saved,
        )

        self.draft_changed.emit(
            replace(self._draft),
        )

    def _set_scale(
        self,
        display_scale: float,
    ) -> None:
        self._replace_draft(
            display_scale=display_scale,
        )

    def _set_font(
        self,
        font_family: str,
    ) -> None:
        self._replace_draft(
            font_family=font_family,
        )

    def _request_apply(self) -> None:
        """Request application and persistence of the current draft."""

        if self._draft == self._saved:
            return

        self.apply_button.setEnabled(False)
        self.apply_button.setText("Applying...")
        self.apply_status_label.clear()

        self.apply_requested.emit(
            replace(self._draft),
        )

    def mark_applied(
        self,
        appearance: AppearanceConfig,
        restart_required: bool,
    ) -> None:
        """Record a successfully applied appearance."""

        self._saved = replace(appearance)
        self._draft = replace(appearance)

        self.apply_button.setText("Apply")
        self.apply_button.setEnabled(False)

        if restart_required:
            self.apply_status_label.setText("Restart required to apply display scale.")
        else:
            self.apply_status_label.setText("Appearance applied.")

    def mark_apply_failed(
        self,
        message: str,
    ) -> None:
        """Restore the Apply button after persistence fails."""

        self.apply_button.setText("Apply")
        self.apply_button.setEnabled(
            self._draft != self._saved,
        )
        self.apply_status_label.setText(message)
