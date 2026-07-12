"""Theme palettes and Qt stylesheet generation."""

from __future__ import annotations

from dataclasses import dataclass

from sephirothos.services.display_scale import DisplayScaleService


@dataclass(frozen=True, slots=True)
class ThemePalette:
    """Semantic colors used to generate the application stylesheet."""

    background: str
    surface: str
    surface_raised: str

    text_primary: str
    text_secondary: str
    text_disabled: str

    accent: str
    accent_hover: str
    accent_pressed: str

    success: str
    warning: str
    error: str

    hover: str
    selected: str
    focus: str

    border: str
    border_strong: str

    glow: str


VOID_PALETTE = ThemePalette(
    background="#17171B",
    surface="#121214",
    surface_raised="#1D1E24",
    text_primary="#F5F5F7",
    text_secondary="#9A9AA3",
    text_disabled="#66666F",
    accent="#8F4FFF",
    accent_hover="#A66EFF",
    accent_pressed="#7341D9",
    success="#63E45F",
    warning="#F2C94C",
    error="#E45F5F",
    hover="#202126",
    selected="#17171B",
    focus="#B388FF",
    border="#2A2B31",
    border_strong="#41434D",
    glow="rgba(143, 79, 255, 0.20)",
)


def build_application_stylesheet(
    palette: ThemePalette,
    scale: DisplayScaleService,
) -> str:
    """Build the global Qt stylesheet for a palette and display scale."""

    base_font_size = scale.scale_pixels(14)
    small_radius = scale.scale_pixels(6)
    control_padding_vertical = scale.scale_pixels(8)
    control_padding_horizontal = scale.scale_pixels(12)
    border_width = max(1, scale.scale_pixels(1))

    return f"""
        QWidget {{
            background-color: {palette.background};
            color: {palette.text_primary};
            font-size: {base_font_size}px;
        }}

        QLabel:disabled,
        QPushButton:disabled {{
            color: {palette.text_disabled};
        }}

        QPushButton {{
            background-color: {palette.surface};
            color: {palette.text_primary};
            border: {border_width}px solid {palette.border};
            border-radius: {small_radius}px;
            padding: {control_padding_vertical}px {control_padding_horizontal}px;
        }}

        QPushButton:hover {{
            background-color: {palette.hover};
            border-color: {palette.border_strong};
        }}

        QPushButton:pressed {{
            background-color: {palette.accent_pressed};
        }}

        QPushButton:checked {{
            background-color: {palette.selected};
            border-color: {palette.accent};
        }}

        QPushButton:focus {{
            border-color: {palette.focus};
        }}

        QLineEdit,
        QTextEdit,
        QPlainTextEdit,
        QComboBox {{
            background-color: {palette.surface};
            color: {palette.text_primary};
            selection-background-color: {palette.accent};
            selection-color: {palette.text_primary};
            border: {border_width}px solid {palette.border};
            border-radius: {small_radius}px;
            padding: {control_padding_vertical}px;
        }}

        QLineEdit:focus,
        QTextEdit:focus,
        QPlainTextEdit:focus,
        QComboBox:focus {{
            border-color: {palette.focus};
        }}

        QToolTip {{
            background-color: {palette.surface_raised};
            color: {palette.text_primary};
            border: {border_width}px solid {palette.border_strong};
        }}
    """
