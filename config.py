"""
FB Manager Pro - Configuration
Cyberpunk 2077 Theme - BRIGHT EDITION
"""

# ========== COLORS - CYBERPUNK BRIGHT ==========
COLORS = {
    # Background - sáng hơn, cyber hơn
    "bg_dark": "#12142a",
    "bg_darker": "#0d0f20",
    "bg_card": "#1a1c38",
    "bg_hover": "#252850",
    
    # Neon colors
    "neon_cyan": "#00f0ff",
    "neon_magenta": "#ff00a8",
    "neon_yellow": "#fcee0a",
    "neon_green": "#00ff66",
    "neon_purple": "#bf00ff",
    "neon_orange": "#ff6b00",
    "neon_red": "#ff003c",
    
    # Text
    "text_primary": "#ffffff",
    "text_secondary": "#d0d0e0",
    "text_muted": "#9090b0",
    "border": "#4a4a80",  # Sáng hơn, cyber hơn
    "border_glow": "#6060a0",
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

# ========== QSS STYLESHEET ==========
CYBERPUNK_QSS = """
/* ========== GLOBAL ========== */
* {
    font-family: 'Segoe UI', 'Rajdhani', sans-serif;
}

QMainWindow, QWidget {
    background-color: #0d0f20;
    color: #e4e4e7;
}

/* ========== SCROLLBAR ========== */
QScrollBar:vertical {
    background: #0d0f20;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background: #3a3a60;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: #00f0ff;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

/* ========== BUTTONS ========== */
QPushButton {
    background: transparent;
    border: 2px solid #00f0ff;
    border-radius: 6px;
    color: #00f0ff;
    padding: 10px 20px;
    font-weight: bold;
    font-size: 11px;
    letter-spacing: 1px;
}

QPushButton:hover {
    background: #00f0ff;
    color: #0d0f20;
}

QPushButton:pressed {
    background: #00c4cc;
}

QPushButton.success {
    border-color: #00ff66;
    color: #00ff66;
}

QPushButton.success:hover {
    background: #00ff66;
    color: #0d0f20;
}

QPushButton.danger {
    border-color: #ff003c;
    color: #ff003c;
}

QPushButton.danger:hover {
    background: #ff003c;
    color: #0d0f20;
}

QPushButton.ghost {
    border-color: #5a5a80;
    color: #b0b0c0;
}

QPushButton.ghost:hover {
    border-color: #00f0ff;
    color: #00f0ff;
    background: transparent;
}

/* ========== INPUT ========== */
QLineEdit, QTextEdit {
    background: #0d0f20;
    border: 2px solid #4a4a80;
    border-radius: 6px;
    padding: 10px 14px;
    color: #e4e4e7;
    font-size: 13px;
    selection-background-color: #00f0ff;
}

QLineEdit:focus, QTextEdit:focus {
    border-color: #00f0ff;
}

QLineEdit::placeholder {
    color: #6a6a90;
}

/* ========== COMBOBOX ========== */
QComboBox {
    background: #0d0f20;
    border: 2px solid #4a4a80;
    border-radius: 6px;
    padding: 10px 14px;
    color: #e4e4e7;
    min-width: 150px;
}

QComboBox:hover {
    border-color: #00f0ff;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #00f0ff;
    margin-right: 10px;
}

QComboBox QAbstractItemView {
    background: #12142a;
    border: 2px solid #4a4a80;
    selection-background-color: #252850;
    outline: none;
}

/* ========== CHECKBOX ========== */
QCheckBox {
    spacing: 8px;
    color: #e4e4e7;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #4a4a80;
    border-radius: 4px;
    background: #0d0f20;
}

QCheckBox::indicator:checked {
    background: #00f0ff;
    border-color: #00f0ff;
}

QCheckBox::indicator:hover {
    border-color: #00f0ff;
}

/* ========== TABLE ========== */
QTableWidget {
    background: transparent;
    border: none;
    gridline-color: #4a4a80;
}

QTableWidget::item {
    padding: 12px;
    border-bottom: 1px solid #4a4a80;
}

QTableWidget::item:selected {
    background: rgba(0, 240, 255, 0.15);
}

QTableWidget::item:hover {
    background: #252850;
}

QHeaderView::section {
    background: rgba(0, 240, 255, 0.08);
    color: #00f0ff;
    padding: 12px;
    border: none;
    border-bottom: 2px solid #4a4a80;
    font-weight: bold;
    font-size: 10px;
    letter-spacing: 2px;
}

/* ========== LABELS ========== */
QLabel.title {
    font-size: 32px;
    font-weight: bold;
    letter-spacing: 4px;
}

QLabel.subtitle {
    color: #6a6a90;
    font-size: 11px;
    letter-spacing: 2px;
}

QLabel.neon-cyan { color: #00f0ff; }
QLabel.neon-green { color: #00ff66; }
QLabel.neon-magenta { color: #ff00a8; }
QLabel.neon-purple { color: #bf00ff; }
QLabel.neon-yellow { color: #fcee0a; }
QLabel.neon-orange { color: #ff6b00; }

/* ========== FRAMES ========== */
QFrame.card {
    background: #1a1c38;
    border: 2px solid #4a4a80;
    border-radius: 12px;
}

QFrame.card-header {
    background: rgba(0, 240, 255, 0.05);
    border-bottom: 2px solid #4a4a80;
}

/* ========== SIDEBAR ========== */
QFrame#sidebar {
    background: qlineargradient(y1:0, y2:1, stop:0 #12142a, stop:1 #0d0f20);
    border-right: 2px solid qlineargradient(y1:0, y2:1, 
        stop:0 #00f0ff, stop:0.5 #ff00a8, stop:1 #00f0ff);
}

/* ========== NAV ITEM ========== */
QPushButton.nav-item {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 8px;
    text-align: left;
    padding: 12px 16px;
    color: #b0b0c0;
    font-weight: 600;
}

QPushButton.nav-item:hover {
    background: rgba(0, 240, 255, 0.08);
    color: #e4e4e7;
    border-color: rgba(0, 240, 255, 0.3);
}

QPushButton.nav-item.active {
    background: qlineargradient(x1:0, x2:1, stop:0 rgba(0,240,255,0.2), stop:1 transparent);
    border-left: 3px solid #00f0ff;
    color: #00f0ff;
}

/* ========== STAT CARD ========== */
QFrame.stat-card {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
        stop:0 rgba(26,28,56,0.9), stop:1 rgba(18,20,42,0.95));
    border: 2px solid #4a4a80;
    border-radius: 12px;
}

QFrame.stat-card:hover {
    border-color: rgba(0, 240, 255, 0.5);
}

/* ========== TERMINAL ========== */
QFrame#terminal {
    background: rgba(10, 12, 25, 0.8);
    border: 2px solid #4a4a80;
    border-radius: 8px;
}

QTextEdit#terminal-text {
    background: transparent;
    border: none;
    color: #e4e4e7;
    font-family: 'Consolas', 'Share Tech Mono', monospace;
    font-size: 11px;
}
"""
