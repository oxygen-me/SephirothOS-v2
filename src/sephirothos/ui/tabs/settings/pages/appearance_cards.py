"""Cards displayed on the Appearance settings page."""

from __future__ import annotations

from dataclasses import replace
from functools import partial

from PySide6.QtCore import QRectF, Qt, Signal
from PySide6.QtGui import (
    QColor,
    QFont,
    QPainter,
    QPaintEvent,
    QPen,
)
from PySide6.QtWidgets import (
    QAbstractButton,
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from sephirothos.config import AppearanceConfig
from sephirothos.services.display_scale import SUPPORTED_SCALE_FACTORS
from sephirothos.services.theme import (
    ACCENT_DISPLAY_NAMES,
    AVAILABLE_ACCENTS,
    AVAILABLE_THEMES,
    THEME_DISPLAY_NAMES,
    AccentId,
    AccentPalette,
    ThemeId,
    resolve_palette,
)
from sephirothos.ui.metrics import UiMetrics
from sephirothos.ui.roles import (
    ButtonVariant,
    CheckRole,
    InputRole,
    TextRole,
)
from sephirothos.ui.widgets.card import Card


class AppearanceCard(Card):
    """Base card that consumes only its required vertical space."""

    def __init__(
        self,
        metrics: UiMetrics,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(metrics, parent)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )


class ThemeSelectionCard(AppearanceCard):
    """Select from known application themes."""

    theme_selected = Signal(str)

    def __init__(
        self,
        metrics: UiMetrics,
        current_theme: str | ThemeId,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(metrics, parent)

        self._current_theme = ThemeId(current_theme)
        self._build_ui(metrics)

    def _build_ui(self, metrics: UiMetrics) -> None:
        self.title_label = QLabel("Theme")
        self.title_label.setProperty(
            "textRole",
            TextRole.CARD_TITLE.value,
        )

        self.description_label = QLabel("Choose the main color scheme used throughout SephirothOS.")
        self.description_label.setWordWrap(True)
        self.description_label.setProperty(
            "textRole",
            TextRole.BODY_MUTED.value,
        )

        self.option_layout = QHBoxLayout()
        self.option_layout.setContentsMargins(0, 0, 0, 0)
        self.option_layout.setSpacing(metrics.space_10)

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        self.buttons: dict[ThemeId, QPushButton] = {}

        for theme_id in ThemeId:
            available = theme_id in AVAILABLE_THEMES

            label = THEME_DISPLAY_NAMES[theme_id]

            if not available:
                label = f"{label}: Coming Soon"

            button = QPushButton(label)
            button.setCheckable(True)
            button.setEnabled(available)
            button.setProperty(
                "buttonVariant",
                ButtonVariant.THEME_OPTION.value,
            )
            button.clicked.connect(
                partial(
                    self._select_theme,
                    theme_id,
                )
            )

            self.button_group.addButton(button)
            self.buttons[theme_id] = button
            self.option_layout.addWidget(button, 1)

        self.buttons[self._current_theme].setChecked(True)

        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.description_label)
        self.main_layout.addLayout(self.option_layout)

    def _select_theme(
        self,
        theme_id: ThemeId,
        checked: bool,
    ) -> None:
        if checked:
            self.theme_selected.emit(theme_id.value)


class AccentSwatchButton(QAbstractButton):
    """Circular accent-color selection button."""

    def __init__(
        self,
        accent: AccentPalette,
        metrics: UiMetrics,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self._accent = accent
        self._border_width = metrics.border_strong

        extent = metrics.space_40

        self.setCheckable(True)
        self.setFixedSize(extent, extent)
        self.setCursor(
            Qt.CursorShape.PointingHandCursor,
        )

    def paintEvent(
        self,
        event: QPaintEvent,
    ) -> None:
        del event

        painter = QPainter(self)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing,
            True,
        )

        if self.isChecked():
            pen = QPen(
                QColor(self._accent.focus),
                self._border_width,
            )
        else:
            pen = QPen(
                QColor(self._accent.base),
                self._border_width,
            )

        painter.setPen(pen)
        painter.setBrush(
            QColor(self._accent.base),
        )

        inset = self._border_width

        painter.drawEllipse(
            self.rect().adjusted(
                inset,
                inset,
                -inset,
                -inset,
            )
        )


class AccentSelectionCard(AppearanceCard):
    """Select the accent used by themes supporting custom accents."""

    accent_selected = Signal(str)

    def __init__(
        self,
        metrics: UiMetrics,
        current_accent: str | AccentId,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(metrics, parent)

        self._current_accent = AccentId(current_accent)
        self._build_ui(metrics)

    def _build_ui(self, metrics: UiMetrics) -> None:
        self.title_label = QLabel("Accent Color")
        self.title_label.setProperty(
            "textRole",
            TextRole.CARD_TITLE.value,
        )

        self.description_label = QLabel(
            "Choose the accent used for selections, focus, and primary actions."
        )
        self.description_label.setWordWrap(True)
        self.description_label.setProperty(
            "textRole",
            TextRole.BODY_MUTED.value,
        )

        self.option_layout = QHBoxLayout()
        self.option_layout.setContentsMargins(0, 0, 0, 0)
        self.option_layout.setSpacing(metrics.space_20)

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        self.buttons: dict[
            AccentId,
            AccentSwatchButton,
        ] = {}

        for accent_id, palette in AVAILABLE_ACCENTS.items():
            option_layout = QVBoxLayout()
            option_layout.setContentsMargins(0, 0, 0, 0)
            option_layout.setSpacing(metrics.space_5)
            option_layout.setAlignment(
                Qt.AlignmentFlag.AlignHCenter,
            )

            button = AccentSwatchButton(
                accent=palette,
                metrics=metrics,
            )
            button.setToolTip(
                ACCENT_DISPLAY_NAMES[accent_id],
            )
            button.clicked.connect(
                partial(
                    self._select_accent,
                    accent_id,
                )
            )

            label = QLabel(
                ACCENT_DISPLAY_NAMES[accent_id],
            )
            label.setAlignment(
                Qt.AlignmentFlag.AlignHCenter,
            )
            label.setProperty(
                "textRole",
                TextRole.CAPTION.value,
            )

            self.button_group.addButton(button)
            self.buttons[accent_id] = button

            option_layout.addWidget(button)
            option_layout.addWidget(label)
            self.option_layout.addLayout(option_layout)

        self.option_layout.addStretch()

        self.buttons[self._current_accent].setChecked(True)

        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.description_label)
        self.main_layout.addLayout(self.option_layout)

    def _select_accent(
        self,
        accent_id: AccentId,
        checked: bool,
    ) -> None:
        if checked:
            self.accent_selected.emit(accent_id.value)


class ThemeCreatorCard(AppearanceCard):
    """Reserve space for the future custom-theme editor."""

    def __init__(
        self,
        metrics: UiMetrics,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(metrics, parent)

        self.title_label = QLabel("Theme Creator")
        self.title_label.setProperty(
            "textRole",
            TextRole.CARD_TITLE.value,
        )

        self.description_label = QLabel("Create, edit, import, and export custom themes.")
        self.description_label.setWordWrap(True)
        self.description_label.setProperty(
            "textRole",
            TextRole.BODY_MUTED.value,
        )

        self.status_label = QLabel("Coming Soon")
        self.status_label.setProperty(
            "textRole",
            TextRole.ACCENT_BODY.value,
        )

        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.description_label)
        self.main_layout.addWidget(self.status_label)


class DisplayScaleCard(AppearanceCard):
    """Select the interface scale applied after restarting."""

    scale_selected = Signal(float)

    def __init__(
        self,
        metrics: UiMetrics,
        current_scale: float,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(metrics, parent)

        self._factors = SUPPORTED_SCALE_FACTORS
        self._build_ui(metrics, current_scale)

    def _build_ui(
        self,
        metrics: UiMetrics,
        current_scale: float,
    ) -> None:
        self.header_layout = QHBoxLayout()
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        self.header_layout.setSpacing(metrics.space_10)

        self.title_label = QLabel("Display Scale")
        self.title_label.setProperty(
            "textRole",
            TextRole.CARD_TITLE.value,
        )

        self.value_label = QLabel()
        self.value_label.setProperty(
            "textRole",
            TextRole.ACCENT_BODY.value,
        )

        self.header_layout.addWidget(self.title_label)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.value_label)

        self.description_label = QLabel(
            "Adjust the size of interface elements. A restart is required."
        )
        self.description_label.setWordWrap(True)
        self.description_label.setProperty(
            "textRole",
            TextRole.BODY_MUTED.value,
        )

        self.slider = QSlider(
            Qt.Orientation.Horizontal,
        )
        self.slider.setProperty(
            "inputRole",
            InputRole.SCALE.value,
        )
        self.slider.setRange(
            0,
            len(self._factors) - 1,
        )
        self.slider.setSingleStep(1)
        self.slider.setPageStep(1)
        self.slider.setTickInterval(1)

        current_index = self._factors.index(
            float(current_scale),
        )
        self.slider.setValue(current_index)

        self.range_layout = QHBoxLayout()
        self.range_layout.setContentsMargins(0, 0, 0, 0)
        self.range_layout.setSpacing(metrics.space_10)

        self.minimum_label = QLabel(
            self._format_factor(self._factors[0]),
        )
        self.minimum_label.setProperty(
            "textRole",
            TextRole.CAPTION.value,
        )

        self.maximum_label = QLabel(
            self._format_factor(self._factors[-1]),
        )
        self.maximum_label.setProperty(
            "textRole",
            TextRole.CAPTION.value,
        )

        self.range_layout.addWidget(self.minimum_label)
        self.range_layout.addStretch()
        self.range_layout.addWidget(self.maximum_label)

        self.slider.valueChanged.connect(
            self._select_scale,
        )

        self._update_value_label(current_index)

        self.main_layout.addLayout(self.header_layout)
        self.main_layout.addWidget(self.description_label)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.slider)
        self.main_layout.addLayout(self.range_layout)

    def _select_scale(
        self,
        index: int,
    ) -> None:
        factor = self._factors[index]

        self._update_value_label(index)
        self.scale_selected.emit(factor)

    def _update_value_label(
        self,
        index: int,
    ) -> None:
        self.value_label.setText(
            self._format_factor(
                self._factors[index],
            )
        )

    @staticmethod
    def _format_factor(
        factor: float,
    ) -> str:
        return f"{round(factor * 100)}%"


SUPPORTED_FONT_FAMILIES = ("Segoe UI",)


class FontSelectionCard(AppearanceCard):
    """Select the application font applied after restarting."""

    font_selected = Signal(str)

    def __init__(
        self,
        metrics: UiMetrics,
        current_font: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(metrics, parent)

        self._build_ui(current_font)

    def _build_ui(
        self,
        current_font: str,
    ) -> None:
        self.title_label = QLabel("Font")
        self.title_label.setProperty(
            "textRole",
            TextRole.CARD_TITLE.value,
        )

        self.description_label = QLabel(
            "Choose the font used throughout SephirothOS. A restart is required."
        )
        self.description_label.setWordWrap(True)
        self.description_label.setProperty(
            "textRole",
            TextRole.BODY_MUTED.value,
        )

        self.font_combo = QComboBox()
        self.font_combo.setProperty(
            "inputRole",
            InputRole.COMBO.value,
        )
        self.font_combo.addItems(
            SUPPORTED_FONT_FAMILIES,
        )

        if current_font in SUPPORTED_FONT_FAMILIES:
            self.font_combo.setCurrentText(
                current_font,
            )

        self.font_combo.currentTextChanged.connect(
            self.font_selected.emit,
        )

        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.description_label)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.font_combo)


class ExtraSettingsCard(AppearanceCard):
    """Contain additional binary appearance settings."""

    option_changed = Signal(str, bool)

    def __init__(
        self,
        metrics: UiMetrics,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(metrics, parent)

        self.metrics = metrics
        self.options: dict[str, QCheckBox] = {}

        self._build_ui()

    def _build_ui(self) -> None:
        self.title_label = QLabel("Extra Settings")
        self.title_label.setProperty(
            "textRole",
            TextRole.CARD_TITLE.value,
        )

        self.description_label = QLabel("Additional interface preferences will appear here.")
        self.description_label.setWordWrap(True)
        self.description_label.setProperty(
            "textRole",
            TextRole.BODY_MUTED.value,
        )

        self.option_layout = QVBoxLayout()
        self.option_layout.setContentsMargins(0, 0, 0, 0)
        self.option_layout.setSpacing(
            self.metrics.space_10,
        )

        self.empty_label = QLabel("No additional options are available yet.")
        self.empty_label.setProperty(
            "textRole",
            TextRole.CAPTION.value,
        )

        self.option_layout.addWidget(
            self.empty_label,
        )

        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.description_label)
        self.main_layout.addLayout(self.option_layout)
        self.main_layout.addStretch()

    def add_option(
        self,
        option_id: str,
        label: str,
        checked: bool = False,
    ) -> QCheckBox:
        """Add a binary option to the card."""

        if option_id in self.options:
            raise ValueError(f"Duplicate appearance option: {option_id!r}.")

        if self.empty_label is not None:
            self.option_layout.removeWidget(
                self.empty_label,
            )
            self.empty_label.deleteLater()
            self.empty_label = None

        checkbox = QCheckBox(label)
        checkbox.setChecked(checked)
        checkbox.setProperty(
            "checkRole",
            CheckRole.DEFAULT.value,
        )
        checkbox.toggled.connect(
            lambda enabled, key=option_id: self.option_changed.emit(
                key,
                enabled,
            )
        )

        self.options[option_id] = checkbox
        self.option_layout.addWidget(checkbox)

        return checkbox


class AppearancePreview(QWidget):
    """Paint a miniature representation of draft appearance settings."""

    def __init__(
        self,
        metrics: UiMetrics,
        appearance: AppearanceConfig,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self._appearance = replace(appearance)
        self._minimum_height = metrics.space_60 * 3
        self._border_width = metrics.border_thin
        self._radius = metrics.radius_medium

        self.setMinimumHeight(
            self._minimum_height,
        )

    def set_appearance(
        self,
        appearance: AppearanceConfig,
    ) -> None:
        """Replace the previewed settings and repaint."""

        self._appearance = replace(appearance)
        self.update()

    def paintEvent(
        self,
        event: QPaintEvent,
    ) -> None:
        del event

        palette = resolve_palette(
            self._appearance.theme_id,
            self._appearance.accent_id,
        )

        painter = QPainter(self)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing,
            True,
        )

        outer = QRectF(self.rect()).adjusted(
            self._border_width,
            self._border_width,
            -self._border_width,
            -self._border_width,
        )

        painter.setPen(
            QPen(
                QColor(palette.border_strong),
                self._border_width,
            )
        )
        painter.setBrush(
            QColor(palette.background),
        )
        painter.drawRoundedRect(
            outer,
            self._radius,
            self._radius,
        )

        unit = max(
            1,
            round(10 * self._appearance.display_scale),
        )

        top_bar = QRectF(
            outer.left(),
            outer.top(),
            outer.width(),
            unit * 3,
        )
        painter.fillRect(
            top_bar,
            QColor(palette.surface),
        )

        body_top = top_bar.bottom()
        sidebar_width = outer.width() * 0.24

        sidebar = QRectF(
            outer.left(),
            body_top,
            sidebar_width,
            outer.bottom() - body_top,
        )
        painter.fillRect(
            sidebar,
            QColor(palette.surface),
        )

        content = QRectF(
            sidebar.right() + unit,
            body_top + unit,
            outer.right() - sidebar.right() - (unit * 2),
            outer.bottom() - body_top - (unit * 2),
        )

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(
            QColor(palette.surface_raised),
        )
        painter.drawRoundedRect(
            content,
            self._radius,
            self._radius,
        )

        font = QFont(
            self._appearance.font_family,
        )
        font.setPixelSize(
            max(
                1,
                round(12 * self._appearance.display_scale),
            )
        )
        font.setBold(True)

        painter.setFont(font)
        painter.setPen(
            QColor(palette.text_primary),
        )
        painter.drawText(
            content.adjusted(
                unit,
                unit,
                -unit,
                -unit,
            ),
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft,
            "Preview",
        )

        button_width = max(
            unit * 6,
            content.width() * 0.25,
        )
        button_height = unit * 3

        button = QRectF(
            content.right() - button_width - unit,
            content.bottom() - button_height - unit,
            button_width,
            button_height,
        )

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(
            QColor(palette.accent),
        )
        painter.drawRoundedRect(
            button,
            self._radius,
            self._radius,
        )


class AppearancePreviewCard(AppearanceCard):
    """Display a miniature preview of draft appearance settings."""

    def __init__(
        self,
        metrics: UiMetrics,
        appearance: AppearanceConfig,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(metrics, parent)

        self.title_label = QLabel("Preview")
        self.title_label.setProperty(
            "textRole",
            TextRole.CARD_TITLE.value,
        )

        self.description_label = QLabel("Preview appearance changes before saving them.")
        self.description_label.setProperty(
            "textRole",
            TextRole.BODY_MUTED.value,
        )

        self.preview = AppearancePreview(
            metrics=metrics,
            appearance=appearance,
        )

        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.description_label)
        self.main_layout.addWidget(
            self.preview,
            1,
        )

    def set_appearance(
        self,
        appearance: AppearanceConfig,
    ) -> None:
        self.preview.set_appearance(
            appearance,
        )
