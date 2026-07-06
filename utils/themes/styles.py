# styles of death and despair
# ---------------------------

# --- default buttons
def d_btn(t) -> str:
    return f"""
    QPushButton {{
        background: transparent;
        color: {t.fg};
        border: 0px;
        border-radius: 0px;
        font-family: Segoe UI;
        font-size: 16px;
        padding-top: 10px;
        padding-bottom: 10px;
        padding-right: 10px;
        padding-left: 10px;
        text-align: left;
    }}
    
    QPushButton:hover {{
        background-color: {t.hover};
    }}
    
    QPushButton:pressed {{
        background-color: {t.selected};
    }}
    QPushButton:checked {{
        background-color: {t.selected};
    }}
"""


def n_btn(t) -> str:
    return f"""
    QPushButton {{
        background: transparent;
        color: {t.fg};
        border: 1px solid {t.border};
        border-radius: 0px;
        font-family: Segoe UI;
        font-size: 16px;
        padding-top: 10px;
        padding-bottom: 10px;
        padding-right: 10px;
        padding-left: 10px;
        text-align: left;
    }}

    QPushButton:hover {{
        background-color: {t.hover};
    }}

    QPushButton:pressed {{
        background-color: {t.selected};
    }}
    QPushButton:checked {{
        background-color: {t.selected};
    }}
"""

# --- default widgets/backgrounds
def d_widget(t) -> str:
    return f"""
    QWidget {{
        background-color: {t.mg};
        border: 0px;
        border-radius: 0px;
    }}
"""

def b_widget(t) -> str:
    return f"""
    QWidget {{
        background-color: {t.bg};
        border: 0px;
        border-radius: 0px;
    }}
"""

def c_widget(t) -> str:
    return f"""
    QWidget {{
        background-color: {t.bg};
        border: 0px;
        border-radius: 0px;
    }}
"""

# --- transparent widgets such as those used in stack areas
def t_widget(t) -> str:
    return f"""
    QWidget {{
        background-color: transparent;
        border: 0px;
        border-radius: 0px;
    }}
"""

# --- page labels (titles, subtitles, etc.)
def p_title(t) -> str:
    return f"""
    QLabel {{
        background-color: transparent;
        color: {t.fg};
        font-family: Segoe UI;
        font-size: 36px;
        font-weight: 500;
        border: 0px;
        border-radius: 0px;
    }}
    """

def p_subtitle(t) -> str:
    return f"""
    QLabel {{
        background-color: transparent;
        color: {t.sub};
        font-family: Segoe UI;
        font-size: 18px;
        font-weight: 500;
        border: 0px;
        border-radius: 0px;
    }}
    """

# --- card titles
def c_title(t) -> str:
    return f"""
    QLabel {{
        background-color: transparent;
        color: {t.fg};
        font-family: Segoe UI;
        font-size: 18px;
        font-weight: 500;
        border: 0px;
        border-radius: 0px;
    }}
    """

def c_subtitle(t) -> str:
    return f"""
    QLabel {{
        background-color: transparent;
        color: {t.sub};
        font-family: Segoe UI;
        font-size: 14px;
        font-weight: 500;
        border: 0px;
        border-radius: 0px;
    }}
    """

# --- outlines
def g_box(t) -> str:
    return f"""
    QWidget {{
        background-color: transparent;
        border: 1px solid {t.border};
        border-radius: 0px;
    }}
    """

def d_div(t) -> str:
    return f"""
    QWidget {{
        background-color: {t.border};
        border: 0px;
        border-radius: 0px;
    }}
    """

# --- others
def u_title(t) -> str:
    return f"""
    QLabel {{
        background-color: transparent;
        color: {t.fg};
        font-family: Segoe UI;
        font-size: 18px;
        font-weight: 600;
        border: 0px;
        border-radius: 0px;
    }}
    """

def s_title(t) -> str:
    return f"""
    QLabel {{
        background-color: transparent;
        color: {t.sub};
        font-family: Segoe UI;
        font-size: 18px;
        font-weight: 600;
        border: 0px;
        border-radius: 0px;
    }}
    """

def s_subtitle(t) -> str:
    return f"""
    QLabel {{
        background-color: transparent;
        color: {t.sub};
        font-family: Segoe UI;
        font-size: 12px;
        font-weight: 500;
        border: 0px;
        border-radius: 0px;
    }}
    """

def d_scroll(theme):
    return f"""
    QScrollArea {{
        border: none;
        background: transparent;
    }}

    QScrollArea > QWidget > QWidget {{
        background: transparent;
    }}

    QScrollBar:vertical {{
        background: transparent;
        width: 8px;
        margin: 4px 2px;
    }}

    QScrollBar::handle:vertical {{
        background: {theme.selected};
        border-radius: 0px;
        min-height: 32px;
    }}

    QScrollBar::handle:vertical:hover {{
        background: {theme.hover};
    }}

    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {{
        height: 0px;
        border: none;
        background: transparent;
    }}

    QScrollBar::add-page:vertical,
    QScrollBar::sub-page:vertical {{
        background: transparent;
    }}

    QScrollBar:horizontal {{
        background: transparent;
        height: 8px;
        margin: 2px 4px;
    }}

    QScrollBar::handle:horizontal {{
        background: {theme.selected};
        border-radius: 0px;
        min-width: 32px;
    }}

    QScrollBar::handle:horizontal:hover {{
        background: {theme.hover};
    }}

    QScrollBar::add-line:horizontal,
    QScrollBar::sub-line:horizontal {{
        width: 0px;
        border: none;
        background: transparent;
    }}

    QScrollBar::add-page:horizontal,
    QScrollBar::sub-page:horizontal {{
        background: transparent;
    }}
    """