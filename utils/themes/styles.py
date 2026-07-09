# styles of death and despair
# ---------------------------

# --- default buttons
def d_btn(t) -> str:
    return f"""
    QPushButton {{
        background: transparent;
        color: {t.fg};
        border: 0px;
        border-radius: 6px;
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
        border-radius: 6px;
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

def o_btn(t) -> str:
    return f"""
    QPushButton {{
        background: transparent;
        color: {t.fg};
        border: 1px solid {t.border};
        border-radius: 6px;
        font-family: Segoe UI;
        font-size: 16px;
        padding-top: 5px;
        padding-bottom: 5px;
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
        border: 2px solid {t.accent};
        background-color: {t.selected};
    }}
"""

def c_btn(t) -> str:
    return f"""
    QPushButton {{
        background: transparent;
        color: {t.fg};
        border: 1px solid {t.borderstrong};
        border-radius: 6px;
        font-family: Segoe UI;
        font-size: 16px;
        padding-top: 8px;
        padding-bottom: 8px;
        padding-right: 8px;
        padding-left: 8px;
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

def a_btn(t) -> str:
    return f"""
    QPushButton {{
        background: {t.accent};
        color: {t.fg};
        border: 0px;
        border-radius: 6px;
        font-family: Segoe UI;
        font-size: 18px;
        font-weight: 600;
        padding-top: 8px;
        padding-bottom: 8px;
        padding-right: 8px;
        padding-left: 8px;
        text-align: left;
    }}

    QPushButton:hover {{
        background-color: {t.accenthover};
    }}

    QPushButton:pressed {{
        background-color: {t.accentpressed};
    }}
    QPushButton:checked {{
        background-color: {t.accentpressed};
    }}
"""

def s_btn(t) -> str:
    return f"""
    QPushButton {{
        background: transparent;
        color: {t.fg};
        border: 1px solid {t.accent};
        border-radius: 6px;
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
        background-color: {t.surface};
        border: 0px;
        border-radius: 8px;
    }}
"""

def l_widget(t) -> str:
    return f"""
    QWidget {{
        background-color: {t.surface};
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
        border-radius: 8px;
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

def c_body(t) -> str:
    return f"""
    QLabel {{
        background-color: transparent;
        color: {t.fg};
        font-family: Segoe UI;
        font-size: 16px;
        font-weight: 500;
        border: 0px;
        border-radius: 0px;
    }}
    """

def c_body2(t) -> str:
    return f"""
    QLabel {{
        background-color: transparent;
        color: {t.sub};
        font-family: Segoe UI;
        font-size: 16px;
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

def c_div(t) -> str:
    return f"""
    QWidget {{
        background-color: {t.borderstrong};
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

# --- special
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

def s_widget(t) -> str:
    return f"""
    QWidget {{
        background-color: {t.surface};
        border: 1px solid {t.accent};
        border-radius: 0px;
    }}
"""

def s_circle(t) -> str:
    return f"""
    QLabel {{
        background-color: transparent;
        border: 2px solid {t.accent};
        border-radius: 20px;
        
        font-family: Segoe UI;
        font-size: 18px;
        font-weight: 500;
    }}
"""

def d_circle(t) -> str:
    return f"""
    QLabel {{
        background-color: transparent;
        border: 2px solid {t.border};
        border-radius: 20px;
        
        font-family: Segoe UI;
        font-size: 18px;
        font-weight: 500;
    }}
"""

def d_scroll(t) -> str:
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
        background: {t.selected};
        border-radius: 0px;
        min-height: 32px;
    }}

    QScrollBar::handle:vertical:hover {{
        background: {t.hover};
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
        background: {t.selected};
        border-radius: 0px;
        min-width: 32px;
    }}

    QScrollBar::handle:horizontal:hover {{
        background: {t.hover};
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

def d_sbar(t) -> str:
    return f"""
    QLineEdit {{
        background-color: {t.surface};
        color: {t.fg};
        placeholder-text-color: {t.sub};
        font-family: Segoe UI;
        font-size: 18px;
        font-weight: 500;
        border: 1px solid {t.border};
        padding: 10px 10px 10px 10px;
    }}
    
    QLineEdit:hover {{
        background-color: {t.hover};
    }}
    
    QLineEdit:focus {{
        background-color: {t.surface};
        color: {t.fg};
    }}
    """


def d_tedit(t) -> str:
    return f"""
    QTextEdit {{
        background-color: {t.surface};
        color: {t.fg};
        placeholder-text-color: {t.sub};
        font-family: Segoe UI;
        font-size: 18px;
        font-weight: 500;
        border: 1px solid {t.border};
        padding: 10px 10px 10px 10px;
    }}

    QTextEdit:hover {{
        background-color: {t.hover};
    }}

    QTextEdit:focus {{
        background-color: {t.surface};
        color: {t.fg};
    }}
    """

def d_table(t) -> str:
    return f"""
    QTableWidget {{
        background-color: {t.surface};
        color: {t.fg};
        border: 1px solid {t.border};
        gridline-color: {t.border};
        font-size: 14px;
    }}

    QHeaderView::section {{
        background-color: {t.surface};
        color: {t.fg};
        border: none;
        border-bottom: 1px solid {t.border};
        padding: 10px;
    }}

    QTableWidget::item {{
        padding: 8px;
        border-bottom: 1px solid {t.border};
    }}

    QTableWidget::item:selected {{
        background-color: {t.selected};
    }}
"""

# --- progress bar + other stuff that needs more customization
def x_pbar(t, color) -> str:
    return f"""
    QProgressBar {{
        background-color: {t.surface};
        border-radius: 2px;
        color: {t.fg};
        height: 2px;
    }}

    QProgressBar::chunk {{
        background-color: {color};
    }}
    """

# --- welcome screen specialized titles
def w_title(t) -> str:
    return f"""
    QLabel {{
        background-color: transparent;
        color: {t.fg};
        font-family: Segoe UI;
        font-size: 60px;
        font-weight: 600;
        border: 0px;
        border-radius: 0px;
    }}
    """

def wa_title(t) -> str:
    return f"""
    QLabel {{
            background-color: transparent;
            color: {t.accent};
            font-family: Segoe UI;
            font-size: 60px;
            font-weight: 600;
            border: 0px;
            border-radius: 0px;
        }}
        """

def w_subtitle(t) -> str:
    return f"""
    QLabel {{
        background-color: transparent;
        color: {t.sub};
        font-family: Segoe UI;
        font-size: 32px;
        font-weight: 500;
        border: 0px;
        border-radius: 0px;
    }}
    """

def w_body(t) -> str:
    return f"""
    QLabel {{
        background-color: transparent;
        color: {t.fg};
        font-family: Consolas;
        font-size: 24px;
        font-weight: 500;
        border: 0px;
        border-radius: 0px;
    }}
    """

# --- accented
def a_subtitle(t) -> str:
    return f"""
    QLabel {{
        background-color: transparent;
        color: {t.accent};
        font-family: Segoe UI;
        font-size: 24px;
        font-weight: 500;
        border: 0px;
        border-radius: 0px;
    }}
    """

def a_body(t) -> str:
    return f"""
    QLabel {{
        background-color: transparent;
        color: {t.accent};
        font-family: Consolas;
        font-size: 24px;
        font-weight: 500;
        border: 0px;
        border-radius: 0px;
    }}
    """

def w_title2(t) -> str:
    return f"""
    QLabel {{
        background-color: transparent;
        color: {t.fg};
        font-family: Segoe UI;
        font-size: 36px;
        font-weight: 600;
        border: 0px;
        border-radius: 0px;
    }}
    """

def w_subtitle2(t) -> str:
    return f"""
    QLabel {{
        background-color: transparent;
        color: {t.sub};
        font-family: Segoe UI;
        font-size: 24px;
        font-weight: 500;
        border: 0px;
        border-radius: 0px;
    }}
    """

def d_combo(t) -> str:
    return f"""
    QComboBox {{
        background-color: {t.bg};
        color: {t.fg};
        placeholder-text-color: {t.sub};
        font-family: Segoe UI;
        font-size: 18px;
        font-weight: 500;
        border: 1px solid {t.border};
        padding: 10px 36px 10px 10px;
    }}

    QComboBox:hover {{
        background-color: {t.hover};
    }}

    QComboBox:focus {{
        background-color: {t.surface};
        color: {t.fg};
        border: 1px solid {t.borderstrong};
    }}

    QComboBox::drop-down {{
        border: 0px;
        width: 32px;
    }}

    QComboBox QAbstractItemView {{
        background-color: {t.surface};
        color: {t.fg};
        border: 1px solid {t.border};
        selection-background-color: {t.selected};
        selection-color: {t.fg};
        outline: 0px;
        font-family: Segoe UI;
        font-size: 18px;
    }}
    """

def d_check(t) -> str:
    return f"""
    QCheckBox {{
        background-color: transparent;
        color: {t.fg};
        font-family: Segoe UI;
        font-size: 16px;
        font-weight: 500;
        spacing: 8px;
    }}

    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
        background-color: {t.surface};
        border: 1px solid {t.border};
        border-radius: 4px;
    }}

    QCheckBox::indicator:hover {{
        background-color: {t.hover};
        border: 1px solid {t.borderstrong};
    }}

    QCheckBox::indicator:checked {{
        background-color: {t.accent};
        border: 1px solid {t.accent};
    }}

    QCheckBox::indicator:checked:hover {{
        background-color: {t.accenthover};
        border: 1px solid {t.accenthover};
    }}

    QCheckBox::indicator:pressed {{
        background-color: {t.selected};
    }}

    QCheckBox:disabled {{
        color: {t.sub};
    }}

    QCheckBox::indicator:disabled {{
        background-color: {t.bg};
        border: 1px solid {t.border};
    }}
    """