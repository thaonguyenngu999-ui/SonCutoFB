"""
FB Manager Pro - Configuration
🐱 CYBERPUNK CUTE CAT Edition 🐱
"""

# ========== HIDEMIUM API CONFIG ==========
HIDEMIUM_BASE_URL = "http://127.0.0.1:2222"
HIDEMIUM_TOKEN = "Cu6tDTR2N1HhTxlMyrQubY2ad56eQzWOjVrrb"

# ========== APP INFO ==========
APP_NAME = "SonCuto FB Manager Pro"
APP_VERSION = "2.0.77"

# ========== COLORS - PASTEL NEON ==========
COLORS = {
    # Background - softer dark
    "bg_dark": "#12121f",
    "bg_darker": "#0c0c18",
    "bg_card": "#1a1a2e",
    "bg_hover": "#252545",
    
    # Pastel Neon - cute colors
    "neon_pink": "#ff6b9d",
    "neon_cyan": "#6bfff2",
    "neon_purple": "#b88fff",
    "neon_mint": "#6bffb8",
    "neon_yellow": "#fff06b",
    "neon_coral": "#ff8f6b",
    "neon_blue": "#6bb8ff",
    "neon_rose": "#ff6bda",
    
    # Legacy names
    "neon_magenta": "#ff6bda",
    "neon_green": "#6bffb8",
    "neon_orange": "#ff8f6b",
    "neon_red": "#ff6b6b",
    
    # Text
    "text_primary": "#ffffff",
    "text_secondary": "#c8c8e0",
    "text_muted": "#8888b0",
    "border": "#3a3a60",
    "border_bright": "#5050a0",
}

# ========== MENU - với cat emoji ==========
MENU_ITEMS = [
    {"id": "profiles", "icon": "😺", "text": "Profiles", "color": "cyan"},
    {"id": "login", "icon": "🔐", "text": "Login FB", "color": "mint"},
    {"id": "pages", "icon": "📄", "text": "Pages", "color": "purple"},
    {"id": "reels", "icon": "🎬", "text": "Reels", "color": "pink"},
    {"id": "content", "icon": "✏️", "text": "Soạn tin", "color": "yellow"},
    {"id": "groups", "icon": "😸", "text": "Đăng nhóm", "color": "coral"},
    {"id": "scripts", "icon": "🐱", "text": "Kịch bản", "color": "blue"},
    {"id": "posts", "icon": "📊", "text": "Bài đăng", "color": "mint"},
]

# ========== API ==========
API_CONFIG = {
    "hidemium_base_url": "http://127.0.0.1:52000",
    "timeout": 30,
}

# ========== QSS STYLESHEET - CUTE ==========
CYBERPUNK_QSS = """
/* ========== GLOBAL - ROUNDED & CUTE ========== */
* {
    font-family: 'Segoe UI', 'Arial', sans-serif;
}

QMainWindow, QWidget {
    background-color: #0c0c18;
    color: #ffffff;
    font-size: 14px;
}

QLabel {
    font-size: 14px;
}

/* ========== SCROLLBAR - CUTE ROUNDED ========== */
QScrollBar:vertical {
    background: #1a1a2e;
    width: 12px;
    border-radius: 6px;
    margin: 4px;
}

QScrollBar::handle:vertical {
    background: qlineargradient(x1:0, x2:1, stop:0 #ff6b9d, stop:1 #b88fff);
    border-radius: 5px;
    min-height: 40px;
    margin: 2px;
}

QScrollBar::handle:vertical:hover {
    background: qlineargradient(x1:0, x2:1, stop:0 #ff8fb8, stop:1 #c8a8ff);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background: #1a1a2e;
    height: 12px;
    border-radius: 6px;
    margin: 4px;
}

QScrollBar::handle:horizontal {
    background: qlineargradient(y1:0, y2:1, stop:0 #6bfff2, stop:1 #6bb8ff);
    border-radius: 5px;
    min-width: 40px;
    margin: 2px;
}

/* ========== BUTTONS - ROUNDED ========== */
QPushButton {
    background: transparent;
    border: 2px solid #ff6b9d;
    border-radius: 12px;
    color: #ff6b9d;
    padding: 12px 24px;
    font-weight: bold;
    font-size: 13px;
}

QPushButton:hover {
    background: #ff6b9d;
    color: #0c0c18;
}

/* ========== INPUT - ROUNDED ========== */
QLineEdit, QTextEdit {
    background: #1a1a2e;
    border: 2px solid #3a3a60;
    border-radius: 12px;
    padding: 12px 18px;
    color: #ffffff;
    font-size: 14px;
    selection-background-color: #ff6b9d;
}

QLineEdit:focus, QTextEdit:focus {
    border-color: #6bfff2;
}

/* ========== COMBOBOX ========== */
QComboBox {
    background: #1a1a2e;
    border: 2px solid #3a3a60;
    border-radius: 12px;
    padding: 12px 18px;
    color: #ffffff;
    font-size: 14px;
    min-width: 160px;
}

QComboBox:hover {
    border-color: #b88fff;
}

QComboBox::drop-down {
    border: none;
    width: 35px;
}

QComboBox::down-arrow {
    border-left: 6px solid transparent;
    border-right: 6px solid transparent;
    border-top: 8px solid #b88fff;
}

QComboBox QAbstractItemView {
    background: #1a1a2e;
    border: 2px solid #3a3a60;
    border-radius: 8px;
    selection-background-color: #252545;
    font-size: 14px;
}

/* ========== TABLE ========== */
QTableWidget {
    background: transparent;
    border: none;
    gridline-color: #3a3a60;
    font-size: 14px;
    border-radius: 12px;
}

QTableWidget::item {
    padding: 14px;
    border-bottom: 1px solid #3a3a60;
    color: #ffffff;
}

QTableWidget::item:selected {
    background: rgba(255, 107, 157, 0.2);
}

QTableWidget::item:hover {
    background: #252545;
}

QHeaderView::section {
    background: #1a1a2e;
    color: #6bfff2;
    padding: 14px;
    border: none;
    border-bottom: 3px solid #6bfff2;
    border-radius: 0;
    font-weight: bold;
    font-size: 12px;
    letter-spacing: 2px;
}

/* ========== CHECKBOX ========== */
QCheckBox {
    spacing: 10px;
    color: #ffffff;
    font-size: 14px;
}

QCheckBox::indicator {
    width: 22px;
    height: 22px;
    border: 2px solid #3a3a60;
    border-radius: 6px;
    background: #1a1a2e;
}

QCheckBox::indicator:checked {
    background: qlineargradient(x1:0, x2:1, stop:0 #ff6b9d, stop:1 #b88fff);
    border-color: #ff6b9d;
}

QCheckBox::indicator:hover {
    border-color: #ff6b9d;
}
"""
