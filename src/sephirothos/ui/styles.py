"""Theme palettes and property-based Qt stylesheet generation."""

from __future__ import annotations

from dataclasses import dataclass, replace

from sephirothos.ui.metrics import UiMetrics


@dataclass(frozen=True, slots=True)
class AccentPalette:
    """Interactive colors belonging to one accent family."""

    base: str
    hover: str
    pressed: str
    focus: str
    glow: str


PURPLE_ACCENT_PALETTE = AccentPalette(
    base="#8F4FFF",
    hover="#A66EFF",
    pressed="#7341D9",
    focus="#B388FF",
    glow="rgba(143, 79, 255, 0.20)",
)


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

    progress_cpu: str
    progress_memory: str
    progress_disk: str
    progress_piss: str

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
    accent=PURPLE_ACCENT_PALETTE.base,
    accent_hover=PURPLE_ACCENT_PALETTE.hover,
    accent_pressed=PURPLE_ACCENT_PALETTE.pressed,
    progress_cpu="#38BDF8",
    progress_memory="#FF6229",
    progress_disk="#63E45F",
    progress_piss="#FFFF00",
    success="#63E45F",
    warning="#F2C94C",
    error="#E45F5F",
    hover="#202126",
    selected="#17171B",
    focus=PURPLE_ACCENT_PALETTE.focus,
    border="#2A2B31",
    border_strong="#41434D",
    glow=PURPLE_ACCENT_PALETTE.glow,
)


def build_application_stylesheet(
    palette: ThemePalette,
    metrics: UiMetrics,
) -> str:
    """Build one application-wide stylesheet from a palette and resolved metrics."""

    return "\n".join(
        (
            _base_styles(palette, metrics),
            _surface_styles(palette, metrics),
            _text_styles(palette, metrics),
            _button_styles(palette, metrics),
            _input_styles(palette, metrics),
            _structural_styles(palette, metrics),
            _table_styles(palette, metrics),
            _progress_styles(palette, metrics),
        )
    )


def _base_styles(palette: ThemePalette, metrics: UiMetrics) -> str:
    return f"""
        * {{
            color: {palette.text_primary};
            font-size: {metrics.font_body}px;
        }}

        *:disabled {{
            color: {palette.text_disabled};
        }}

        QToolTip {{
            background-color: {palette.surface_raised};
            color: {palette.text_primary};
            border: {metrics.border_thin}px solid {palette.border_strong};
            padding: {metrics.space_5}px;
        }}
    """


def _surface_styles(palette: ThemePalette, metrics: UiMetrics) -> str:
    return f"""
        QWidget[surfaceRole="background"] {{
            background-color: {palette.background};
            border: 0;
        }}

        QWidget[surfaceRole="chrome"] {{
            background-color: {palette.surface};
            border: 0;
        }}

        QWidget[surfaceRole="panel"] {{
            background-color: {palette.surface};
            border: 0;
            border-radius: {metrics.radius_medium}px;
        }}

        QWidget[surfaceRole="card"] {{
            background-color: {palette.background};
            border: 0;
            border-radius: {metrics.radius_medium}px;
        }}

        QWidget[surfaceRole="transparent"] {{
            background-color: transparent;
            border: 0;
        }}

        QWidget[surfaceRole="outlined"] {{
            background-color: transparent;
            border: {metrics.border_thin}px solid {palette.border};
            border-radius: {metrics.radius_medium}px;
        }}

        QWidget[surfaceRole="accent-outlined"] {{
            background-color: {palette.surface};
            border: {metrics.border_thin}px solid {palette.accent};
            border-radius: {metrics.radius_medium}px;
        }}
    """


def _text_styles(palette: ThemePalette, metrics: UiMetrics) -> str:
    return f"""
        QLabel[textRole] {{
            background-color: transparent;
            border: 0;
        }}

        QLabel[textRole="page-title"] {{
            color: {palette.text_primary};
            font-size: {metrics.font_page_title}px;
            font-weight: 500;
        }}

        QLabel[textRole="page-subtitle"] {{
            color: {palette.text_secondary};
            font-size: {metrics.font_subtitle}px;
            font-weight: 500;
        }}

        QLabel[textRole="card-title"] {{
            color: {palette.text_primary};
            font-size: {metrics.font_subtitle}px;
            font-weight: 500;
        }}

        QLabel[textRole="caption"] {{
            color: {palette.text_secondary};
            font-size: {metrics.font_small}px;
            font-weight: 500;
        }}

        QLabel[textRole="body"] {{
            color: {palette.text_primary};
            font-size: {metrics.font_body}px;
            font-weight: 500;
        }}

        QLabel[textRole="body-muted"] {{
            color: {palette.text_secondary};
            font-size: {metrics.font_body}px;
            font-weight: 500;
        }}

        QLabel[textRole="username"] {{
            color: {palette.text_primary};
            font-size: {metrics.font_subtitle}px;
            font-weight: 600;
        }}

        QLabel[textRole="section-title"] {{
            color: {palette.text_secondary};
            font-size: {metrics.font_subtitle}px;
            font-weight: 600;
        }}

        QLabel[textRole="section-caption"] {{
            color: {palette.text_secondary};
            font-size: {metrics.font_caption}px;
            font-weight: 500;
        }}

        QLabel[textRole="welcome-title"] {{
            color: {palette.text_primary};
            font-size: {metrics.font_hero_title}px;
            font-weight: 600;
        }}

        QLabel[textRole="welcome-title-accent"] {{
            color: {palette.accent};
            font-size: {metrics.font_hero_title}px;
            font-weight: 600;
        }}

        QLabel[textRole="welcome-subtitle"] {{
            color: {palette.text_secondary};
            font-size: {metrics.font_hero_subtitle}px;
            font-weight: 500;
        }}

        QLabel[textRole="welcome-body"] {{
            color: {palette.text_primary};
            font-family: "Consolas";
            font-size: {metrics.font_emphasis}px;
            font-weight: 500;
        }}

        QLabel[textRole="welcome-page-title"] {{
            color: {palette.text_primary};
            font-size: {metrics.font_page_title}px;
            font-weight: 600;
        }}

        QLabel[textRole="welcome-page-subtitle"] {{
            color: {palette.text_secondary};
            font-size: {metrics.font_emphasis}px;
            font-weight: 500;
        }}

        QLabel[textRole="accent-subtitle"] {{
            color: {palette.accent};
            font-size: {metrics.font_emphasis}px;
            font-weight: 500;
        }}

        QLabel[textRole="accent-body"] {{
            color: {palette.accent};
            font-family: "Consolas";
            font-size: {metrics.font_emphasis}px;
            font-weight: 500;
        }}
    """


def _button_styles(palette: ThemePalette, metrics: UiMetrics) -> str:
    return f"""
        QPushButton[buttonVariant] {{
            background-color: transparent;
            color: {palette.text_primary};
            border: 0;
            border-radius: {metrics.radius_medium}px;
            font-size: {metrics.font_body}px;
            padding: {metrics.space_10}px;
            text-align: left;
        }}

        QPushButton[buttonVariant]:hover {{
            background-color: {palette.hover};
        }}

        QPushButton[buttonVariant]:pressed,
        QPushButton[buttonVariant]:checked {{
            background-color: {palette.selected};
        }}

        QPushButton[buttonVariant="secondary"] {{
            border: {metrics.border_thin}px solid {palette.border};
        }}

        QPushButton[buttonVariant="selectable"] {{
            border: {metrics.border_thin}px solid {palette.border};
            padding: {metrics.space_5}px {metrics.space_10}px;
        }}

        QPushButton[buttonVariant="selectable"]:checked,
        QPushButton[buttonVariant="theme-option"]:checked {{
            border: {metrics.border_strong}px solid {palette.accent};
        }}

        QPushButton[buttonVariant="card-action"] {{
            border: {metrics.border_thin}px solid {palette.border_strong};
        }}

        QPushButton[buttonVariant="primary"] {{
            background-color: {palette.accent};
            font-size: {metrics.font_subtitle}px;
            font-weight: 600;
        }}

        QPushButton[buttonVariant="primary"]:hover {{
            background-color: {palette.accent_hover};
        }}

        QPushButton[buttonVariant="primary"]:pressed,
        QPushButton[buttonVariant="primary"]:checked {{
            background-color: {palette.accent_pressed};
        }}

        QPushButton[buttonVariant="accent-outline"] {{
            border: {metrics.border_thin}px solid {palette.accent};
        }}

        QPushButton[buttonVariant="theme-option"] {{
            border: {metrics.border_thin}px solid {palette.border};
        }}
        
        QPushButton[buttonVariant="link"] {{
            background-color: transparent;
            color: {palette.accent};
            border: 0;
            border-radius: 0;
            padding: 0;
        }}

        QPushButton[buttonVariant="link"]:hover {{
            background-color: transparent;
            color: {palette.accent_hover};
        }}

        QPushButton[buttonVariant="link"]:pressed {{
            background-color: transparent;
            color: {palette.accent_pressed};
        }}
    """


def _input_styles(palette: ThemePalette, metrics: UiMetrics) -> str:
    return f"""
        QLineEdit[inputRole="search"],
        QTextEdit[inputRole="editor"],
        QPlainTextEdit[inputRole="editor"],
        QComboBox[inputRole="combo"] {{
            background-color: {palette.surface};
            color: {palette.text_primary};
            selection-background-color: {palette.accent};
            selection-color: {palette.text_primary};
            border: {metrics.border_thin}px solid {palette.border};
            padding: {metrics.space_10}px;
            font-size: {metrics.font_subtitle}px;
            font-weight: 500;
        }}

        QLineEdit[inputRole="search"]:hover,
        QTextEdit[inputRole="editor"]:hover,
        QPlainTextEdit[inputRole="editor"]:hover,
        QComboBox[inputRole="combo"]:hover {{
            background-color: {palette.hover};
        }}

        QLineEdit[inputRole="search"]:focus,
        QTextEdit[inputRole="editor"]:focus,
        QPlainTextEdit[inputRole="editor"]:focus,
        QComboBox[inputRole="combo"]:focus {{
            background-color: {palette.surface};
            border-color: {palette.border_strong};
        }}

        QComboBox[inputRole="combo"]::drop-down {{
            border: 0;
            width: {metrics.space_30}px;
        }}

        QComboBox[inputRole="combo"] QAbstractItemView {{
            background-color: {palette.surface};
            color: {palette.text_primary};
            border: {metrics.border_thin}px solid {palette.border};
            selection-background-color: {palette.selected};
            selection-color: {palette.text_primary};
            outline: 0;
        }}

        QCheckBox[checkRole="default"] {{
            background-color: transparent;
            color: {palette.text_primary};
            font-size: {metrics.font_body}px;
            font-weight: 500;
            spacing: {metrics.space_10}px;
        }}

        QCheckBox[checkRole="default"]::indicator {{
            width: {metrics.checkbox_extent}px;
            height: {metrics.checkbox_extent}px;
            background-color: {palette.surface};
            border: {metrics.border_thin}px solid {palette.border};
            border-radius: {metrics.radius_small}px;
        }}

        QCheckBox[checkRole="default"]::indicator:hover {{
            background-color: {palette.hover};
            border-color: {palette.border_strong};
        }}

        QCheckBox[checkRole="default"]::indicator:checked {{
            background-color: {palette.accent};
            border-color: {palette.accent};
        }}

        QCheckBox[checkRole="default"]::indicator:checked:hover {{
            background-color: {palette.accent_hover};
            border-color: {palette.accent_hover};
        }}

        QCheckBox[checkRole="default"]::indicator:pressed {{
            background-color: {palette.selected};
        }}
        
                QSlider[inputRole="scale"]::groove:horizontal {{
            height: {metrics.progress_height}px;
            background-color: {palette.border};
            border: 0;
        }}

        QSlider[inputRole="scale"]::sub-page:horizontal {{
            background-color: {palette.accent};
            border: 0;
        }}

        QSlider[inputRole="scale"]::add-page:horizontal {{
            background-color: {palette.border};
            border: 0;
        }}

        QSlider[inputRole="scale"]::handle:horizontal {{
            width: {metrics.space_20}px;
            height: {metrics.space_20}px;
            margin: -{metrics.space_10}px 0;
            background-color: {palette.accent};
            border: {metrics.border_strong}px solid {palette.focus};
            border-radius: {metrics.space_10}px;
        }}

        QSlider[inputRole="scale"]::handle:horizontal:hover {{
            background-color: {palette.accent_hover};
        }}

        QSlider[inputRole="scale"]::handle:horizontal:pressed {{
            background-color: {palette.accent_pressed};
        }}
    """


def _structural_styles(palette: ThemePalette, metrics: UiMetrics) -> str:
    return f"""
        *[dividerRole="default"] {{
            background-color: {palette.border};
            border: 0;
        }}

        *[dividerRole="strong"] {{
            background-color: {palette.border_strong};
            border: 0;
        }}

        QLabel[indicatorRole="default-circle"] {{
            background-color: transparent;
            border: {metrics.border_strong}px solid {palette.border};
            border-radius: {metrics.space_20}px;
            font-size: {metrics.font_subtitle}px;
            font-weight: 500;
        }}

        QLabel[indicatorRole="accent-circle"] {{
            background-color: transparent;
            border: {metrics.border_strong}px solid {palette.accent};
            border-radius: {metrics.space_20}px;
            font-size: {metrics.font_subtitle}px;
            font-weight: 500;
        }}

        QScrollArea[scrollRole="default"] {{
            background-color: transparent;
            border: 0;
        }}

        QScrollArea[scrollRole="default"] > QWidget > QWidget {{
            background-color: transparent;
        }}

        QScrollBar:vertical {{
            background-color: transparent;
            width: {metrics.scrollbar_extent}px;
            margin: {metrics.space_5}px 0;
        }}

        QScrollBar::handle:vertical {{
            background-color: {palette.selected};
            min-height: {metrics.space_30}px;
        }}

        QScrollBar:horizontal {{
            background-color: transparent;
            height: {metrics.scrollbar_extent}px;
            margin: 0 {metrics.space_5}px;
        }}

        QScrollBar::handle:horizontal {{
            background-color: {palette.selected};
            min-width: {metrics.space_30}px;
        }}

        QScrollBar::handle:hover {{
            background-color: {palette.hover};
        }}

        QScrollBar::add-line,
        QScrollBar::sub-line {{
            width: 0;
            height: 0;
            border: 0;
            background-color: transparent;
        }}

        QScrollBar::add-page,
        QScrollBar::sub-page {{
            background-color: transparent;
        }}
    """


def _table_styles(palette: ThemePalette, metrics: UiMetrics) -> str:
    return f"""
        QTableWidget[tableRole="default"] {{
            background-color: {palette.surface};
            color: {palette.text_primary};
            border: {metrics.border_thin}px solid {palette.border};
            gridline-color: {palette.border};
            font-size: {metrics.font_small}px;
        }}

        QTableWidget[tableRole="default"] QHeaderView::section {{
            background-color: {palette.surface};
            color: {palette.text_primary};
            border: 0;
            border-bottom: {metrics.border_thin}px solid {palette.border};
            padding: {metrics.space_10}px;
        }}

        QTableWidget[tableRole="default"]::item {{
            padding: {metrics.space_10}px;
            border-bottom: {metrics.border_thin}px solid {palette.border};
        }}

        QTableWidget[tableRole="default"]::item:selected {{
            background-color: {palette.selected};
        }}
    """


def _progress_styles(palette: ThemePalette, metrics: UiMetrics) -> str:
    return f"""
        QProgressBar[progressRole="default"] {{
            background-color: {palette.surface};
            border: 0;
            border-radius: {metrics.radius_small}px;
            color: {palette.text_primary};
            min-height: {metrics.progress_height}px;
            max-height: {metrics.progress_height}px;
        }}

        QProgressBar[progressRole="default"]::chunk,
        QProgressBar[progressRole="default"][tone="accent"]::chunk {{
            background-color: {palette.accent};
        }}

        QProgressBar[progressRole="default"][tone="success"]::chunk {{
            background-color: {palette.success};
        }}

        QProgressBar[progressRole="default"][tone="warning"]::chunk {{
            background-color: {palette.warning};
        }}

        QProgressBar[progressRole="default"][tone="error"]::chunk {{
            background-color: {palette.error};
        }}
        
        QProgressBar[progressRole="default"][progressVariant="cpu"]::chunk {{
            background-color: {palette.progress_cpu};
        }}

        QProgressBar[progressRole="default"][progressVariant="memory"]::chunk {{
            background-color: {palette.progress_memory};
        }}

        QProgressBar[progressRole="default"][progressVariant="disk"]::chunk {{
            background-color: {palette.progress_disk};
        }}

        QProgressBar[progressRole="default"][progressVariant="piss"]::chunk {{
            background-color: {palette.progress_piss};
        }}
    """


def apply_accent_palette(
    palette: ThemePalette,
    accent: AccentPalette,
) -> ThemePalette:
    """Return a theme palette with an accent family applied."""

    return replace(
        palette,
        accent=accent.base,
        accent_hover=accent.hover,
        accent_pressed=accent.pressed,
        focus=accent.focus,
        glow=accent.glow,
    )
