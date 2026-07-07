from dataclasses import dataclass
from eventbus import mainBus

@dataclass(frozen=True)
class Theme:
    bg: str
    mg: str
    fg: str
    sub: str
    accent: str
    hover: str
    selected: str
    border: str
    border2: str

DARK = Theme(
    bg="#1d1f22",
    mg="#111215",
    fg="#ffffff",
    sub="#808080",
    accent="#63e45f",
    hover="#202226",
    selected="#1a1b1d",
    border="#1b1c1e",
    border2="#808080"
)

LIGHT = Theme(
    bg="#1d1f22",
    mg="#111215",
    fg="#ffffff",
    sub="#808080",
    accent="#1d1f22",
    hover="#1d1f22",
    selected="#1a1b1d",
    border="#1b1c1e",
    border2="#808080"
)

CURRENT = DARK

def set_theme(theme_name: str):
    global CURRENT
    CURRENT = globals()[theme_name]

mainBus.themeUpdate.connect(set_theme)