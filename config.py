"""
FB Manager Pro - Configuration
Cyberpunk 2077 Theme - V3 BIGGER & BOLDER
"""

# ========== COLORS ==========
COLORS = {
    # Background
    "bg_dark": "#0a0a18",
    "bg_darker": "#06060f",
    "bg_card": "#0f0f22",
    "bg_hover": "#1a1a35",
    
    # Neon colors
    "neon_cyan": "#00f0ff",
    "neon_magenta": "#ff00a8",
    "neon_yellow": "#fcee0a",
    "neon_green": "#00ff66",
    "neon_purple": "#bf00ff",
    "neon_orange": "#ff6b00",
    "neon_red": "#ff003c",
    
    # Text - BIGGER
    "text_primary": "#ffffff",
    "text_secondary": "#c0c0d8",
    "text_muted": "#7878a0",
    "border": "#2a2a50",
    "border_bright": "#4040a0",
}

# ========== MENU ==========
MENU_ITEMS = [
    {"id": "profiles", "icon": "👤", "text": "Profiles", "color": "cyan"},
    {"id": "login", "icon": "🔐", "text": "Login FB", "color": "green"},
    {"id": "pages", "icon": "📄", "text": "Pages", "color": "purple"},
    {"id": "reels", "icon": "🎬", "text": "Reels", "color": "magenta"},
    {"id": "content", "icon": "✏️", "text": "Soạn tin", "color": "yellow"},
    {"id": "groups", "icon": "👥", "text": "Đăng nhóm", "color": "orange"},
    {"id": "scripts", "icon": "📜", "text": "Kịch bản", "color": "cyan"},
    {"id": "posts", "icon": "📊", "text": "Bài đăng", "color": "green"},
]

# ========== API ==========
API_CONFIG = {
    "hidemium_base_url": "http://127.0.0.1:52000",
    "timeout": 30,
}

# ========== QSS STYLESHEET ==========
CYBERPUNK_QSS = """
/* ========== GLOBAL - BIGGER FONTS ========== */
* {
    font-family: 'Segoe UI', 'Arial', sans-serif;
}

QMainWindow, QWidget {
    background-color: #06060f;
    color: #ffffff;
    font-size: 14px;
}

QLabel {
    font-size: 14px;
}

/* ========== SCROLLBAR ========== */
QScrollBar:vertical {
    background: #0a0a18;
    width: 10px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background: #2a2a50;
    border-radius: 5px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: #00f0ff;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background: #0a0a18;
    height: 10px;
    border-radius: 5px;
}

QScrollBar::handle:horizontal {
    background: #2a2a50;
    border-radius: 5px;
    min-width: 30px;
}

QScrollBar::handle:horizontal:hover {
    background: #00f0ff;
}

/* ========== BUTTONS ========== */
QPushButton {
    background: transparent;
    border: 2px solid #00f0ff;
    color: #00f0ff;
    padding: 12px 24px;
    font-weight: bold;
    font-size: 13px;
    letter-spacing: 1px;
}

QPushButton:hover {
    background: #00f0ff;
    color: #06060f;
}

/* ========== INPUT ========== */
QLineEdit, QTextEdit {
    background: #0a0a18;
    border: 2px solid #2a2a50;
    padding: 12px 16px;
    color: #ffffff;
    font-size: 14px;
    selection-background-color: #00f0ff;
}

QLineEdit:focus, QTextEdit:focus {
    border-color: #00f0ff;
}

/* ========== COMBOBOX ========== */
QComboBox {
    background: #0a0a18;
    border: 2px solid #2a2a50;
    padding: 12px 16px;
    color: #ffffff;
    font-size: 14px;
    min-width: 160px;
}

QComboBox:hover {
    border-color: #00f0ff;
}

QComboBox::drop-down {
    border: none;
    width: 35px;
}

QComboBox::down-arrow {
    border-left: 6px solid transparent;
    border-right: 6px solid transparent;
    border-top: 8px solid #00f0ff;
}

QComboBox QAbstractItemView {
    background: #0f0f22;
    border: 2px solid #2a2a50;
    selection-background-color: #1a1a35;
    font-size: 14px;
}

/* ========== TABLE ========== */
QTableWidget {
    background: transparent;
    border: none;
    gridline-color: #2a2a50;
    font-size: 14px;
}

QTableWidget::item {
    padding: 14px;
    border-bottom: 1px solid #2a2a50;
    color: #ffffff;
}

QTableWidget::item:selected {
    background: rgba(0, 240, 255, 0.2);
}

QTableWidget::item:hover {
    background: #1a1a35;
}

QHeaderView::section {
    background: #0a0a18;
    color: #00f0ff;
    padding: 14px;
    border: none;
    border-bottom: 3px solid #00f0ff;
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
    border: 2px solid #2a2a50;
    background: #0a0a18;
}

QCheckBox::indicator:checked {
    background: #00f0ff;
    border-color: #00f0ff;
}

QCheckBox::indicator:hover {
    border-color: #00f0ff;
}
"""
