from dataclasses import dataclass
from eventbus import mainBus

@dataclass(frozen=True)
class Theme:
    bg: str
    surface: str
    surface2: str

    fg: str
    sub: str
    disabled: str

    accent: str
    accenthover: str
    accentpressed: str

    success: str
    warning: str
    error: str

    hover: str
    selected: str
    focus: str

    border: str
    borderstrong: str

    glow: str

DARK = Theme(
    bg="#17171B",        # main app/window
    surface="#121214",   # cards/panels
    surface2="#1D1E24",  # hover/raised/selected surfaces

    fg="#F5F5F7",
    sub="#9A9AA3",
    disabled="#66666F",

    accent="#8F4FFF",
    accenthover="#A66EFF",
    accentpressed="#7341D9",

    success="#63E45F",
    warning="#F2C94C",
    error="#E45F5F",

    hover="#202126",
    selected="#17171b",
    focus="#B388FF",

    border="#2A2B31",
    borderstrong="#41434D",

    glow="rgba(143,79,255,0.20)"
)
CURRENT = DARK

def set_theme(theme_name: str):
    global CURRENT
    CURRENT = globals()[theme_name]

mainBus.themeUpdate.connect(set_theme)