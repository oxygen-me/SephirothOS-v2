"""Cards displayed on the Appearance settings page."""

from __future__ import annotations

from functools import partial

from PySide6.QtCore import Qt, Signal
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

        self.title_label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )
        self.description_label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        self.option_layout = QVBoxLayout()
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
            self.option_layout.addWidget(button)

        self.buttons[self._current_theme].setChecked(True)

        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.description_label)
        self.main_layout.addStretch()
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
    """Display real Qt widgets using draft appearance settings."""

    def __init__(
        self,
        metrics: UiMetrics,
        appearance: AppearanceConfig,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName(
            "appearancePreview",
        )
        self.setAttribute(
            Qt.WidgetAttribute.WA_StyledBackground,
            True,
        )
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )
        self.setMinimumHeight(
            metrics.space_60 * 4,
        )

        self._build_ui()
        self._styler = AppearancePreviewStyler(
            root=self,
            main_layout=self.main_layout,
            control_layout=self.control_layout,
        )
        self.set_appearance(appearance)

    def _build_ui(self) -> None:
        self.main_layout = QVBoxLayout(self)

        # The preview helper owns these values because they change
        # according to the draft scale.
        self.main_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        self.main_layout.setSpacing(0)

        self.title_label = QLabel(
            "SephirothOS Preview",
        )
        self.title_label.setObjectName(
            "appearancePreviewTitle",
        )
        self.title_label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        self.body_label = QLabel(
            "Text, spacing, controls, and accent colors are rendered from the current draft."
        )
        self.body_label.setObjectName(
            "appearancePreviewBody",
        )
        self.body_label.setWordWrap(True)
        self.body_label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        self.control_layout = QHBoxLayout()
        self.control_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        self.control_layout.setSpacing(0)

        self.primary_button = QPushButton(
            "Primary Action",
        )
        self.primary_button.setObjectName(
            "appearancePreviewPrimary",
        )

        self.secondary_button = QPushButton(
            "Secondary Action",
        )
        self.secondary_button.setObjectName(
            "appearancePreviewSecondary",
        )

        self.control_layout.addWidget(
            self.primary_button,
        )
        self.control_layout.addWidget(
            self.secondary_button,
        )
        self.control_layout.addStretch()

        self.main_layout.addWidget(
            self.title_label,
        )
        self.main_layout.addWidget(
            self.body_label,
        )
        self.main_layout.addStretch()
        self.main_layout.addLayout(
            self.control_layout,
        )

    def set_appearance(
        self,
        appearance: AppearanceConfig,
    ) -> None:
        """Apply a new draft to the real preview widgets."""

        self._styler.apply(
            appearance,
        )


class AppearancePreviewCard(AppearanceCard):
    """Display real widgets using draft appearance settings."""

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
        self.title_label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        self.description_label = QLabel("Preview appearance changes before saving them.")
        self.description_label.setProperty(
            "textRole",
            TextRole.BODY_MUTED.value,
        )
        self.description_label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        self.preview = AppearancePreview(
            metrics=metrics,
            appearance=appearance,
        )

        self.main_layout.addWidget(
            self.title_label,
        )
        self.main_layout.addWidget(
            self.description_label,
        )
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


class AppearancePreviewStyler:
    """Apply draft appearance settings to the preview subtree."""

    def __init__(
        self,
        root: QWidget,
        main_layout: QVBoxLayout,
        control_layout: QHBoxLayout,
    ) -> None:
        self._root = root
        self._main_layout = main_layout
        self._control_layout = control_layout

    def apply(
        self,
        appearance: AppearanceConfig,
    ) -> None:
        """Apply an appearance draft without changing the real application."""

        palette = resolve_palette(
            appearance.theme_id,
            appearance.accent_id,
        )

        px = self._pixel_scaler(
            appearance.display_scale,
        )

        outer_margin = px(20)
        section_spacing = px(20)
        control_spacing = px(10)

        self._main_layout.setContentsMargins(
            outer_margin,
            outer_margin,
            outer_margin,
            outer_margin,
        )
        self._main_layout.setSpacing(
            section_spacing,
        )
        self._control_layout.setSpacing(
            control_spacing,
        )

        font = QFont(
            appearance.font_family,
        )
        font.setPixelSize(px(16))
        self._root.setFont(font)

        self._root.setStyleSheet(
            f"""
            QWidget#appearancePreview {{
                background-color: {palette.background};
                border: {px(1)}px solid {palette.border_strong};
                border-radius: {px(8)}px;
            }}

            QLabel#appearancePreviewTitle {{
                background-color: transparent;
                color: {palette.text_primary};
                border: 0;
                font-size: {px(24)}px;
                font-weight: 600;
            }}

            QLabel#appearancePreviewBody {{
                background-color: transparent;
                color: {palette.text_secondary};
                border: 0;
                font-size: {px(16)}px;
                font-weight: 400;
            }}

            QPushButton#appearancePreviewPrimary {{
                background-color: {palette.accent};
                color: {palette.text_primary};
                border: 0;
                border-radius: {px(8)}px;
                padding: {px(10)}px {px(20)}px;
                font-size: {px(16)}px;
                font-weight: 600;
            }}

            QPushButton#appearancePreviewPrimary:hover {{
                background-color: {palette.accent_hover};
            }}

            QPushButton#appearancePreviewPrimary:pressed {{
                background-color: {palette.accent_pressed};
            }}

            QPushButton#appearancePreviewSecondary {{
                background-color: {palette.surface};
                color: {palette.text_primary};
                border: {px(1)}px solid {palette.border_strong};
                border-radius: {px(8)}px;
                padding: {px(10)}px {px(20)}px;
                font-size: {px(16)}px;
                font-weight: 500;
            }}

            QPushButton#appearancePreviewSecondary:hover {{
                background-color: {palette.hover};
            }}

            QPushButton#appearancePreviewSecondary:pressed {{
                background-color: {palette.selected};
            }}
            """
        )

        self._root.updateGeometry()
        self._root.update()

    @staticmethod
    def _pixel_scaler(
        factor: float,
    ):
        def scale(value: int | float) -> int:
            return max(
                1,
                int((value * factor) + 0.5),
            )

        return scale
