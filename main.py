"""
FB Manager Pro - Main Application
🐱 CYBERPUNK CUTE CAT Edition 🐱
Rounded, Soft, Kawaii ~nyaa
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFrame, QLabel, QStackedWidget, QScrollArea, QSizePolicy,
    QSpacerItem, QGridLayout
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QFontDatabase, QColor, QPainter, QPen, QBrush, QLinearGradient, QPainterPath

from config import COLORS, MENU_ITEMS, CYBERPUNK_QSS
from widgets import (
    CyberButton, CyberInput, CyberComboBox, CyberCard, CyberStatCard,
    CyberTitle, NavItem, CyberTerminal, CyberTable,
    ScanlineOverlay, NeonRain, CyberGrid, PulsingDot, GlitchText, NeonFlash
)


class Sidebar(QWidget):
    """Sidebar cute rounded 🐱"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(260)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Logo section
        logo_section = QWidget()
        logo_section.setFixedHeight(100)
        logo_layout = QHBoxLayout(logo_section)
        logo_layout.setContentsMargins(20, 20, 20, 20)
        
        # Logo box - rounded
        logo_box = QFrame()
        logo_box.setFixedSize(56, 56)
        logo_box.setStyleSheet(f"""
            background: qlineargradient(x1:0, x2:1, stop:0 {COLORS['neon_pink']}, stop:1 {COLORS['neon_purple']});
            border-radius: 16px;
        """)
        logo_box_layout = QVBoxLayout(logo_box)
        logo_box_layout.setAlignment(Qt.AlignCenter)
        logo_text = QLabel("🐱")
        logo_text.setStyleSheet("font-size: 28px;")
        logo_text.setAlignment(Qt.AlignCenter)
        logo_box_layout.addWidget(logo_text)
        logo_layout.addWidget(logo_box)
        
        # Logo title
        title_widget = QWidget()
        title_layout = QVBoxLayout(title_widget)
        title_layout.setContentsMargins(14, 0, 0, 0)
        title_layout.setSpacing(2)
        
        main_title = QLabel("SonCuto")
        main_title.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 18px;
            font-weight: bold;
        """)
        title_layout.addWidget(main_title)
        
        sub_title = QLabel("✦ FB MANAGER ✦")
        sub_title.setStyleSheet(f"""
            color: {COLORS['neon_pink']};
            font-size: 10px;
            letter-spacing: 2px;
        """)
        title_layout.addWidget(sub_title)
        
        logo_layout.addWidget(title_widget)
        logo_layout.addStretch()
        layout.addWidget(logo_section)
        
        # Divider - cute gradient
        divider = QFrame()
        divider.setFixedHeight(3)
        divider.setStyleSheet(f"""
            background: qlineargradient(x1:0, x2:1, stop:0 {COLORS['neon_pink']}, stop:0.5 {COLORS['neon_purple']}, stop:1 {COLORS['neon_cyan']});
            margin: 0 16px;
            border-radius: 2px;
        """)
        layout.addWidget(divider)
        
        # Menu label
        menu_label = QLabel("✦ MENU")
        menu_label.setStyleSheet(f"""
            color: {COLORS['text_muted']};
            font-size: 11px;
            letter-spacing: 3px;
            padding: 18px 24px 10px 24px;
        """)
        layout.addWidget(menu_label)
        
        # Navigation
        self.nav_items = {}
        nav_container = QWidget()
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setContentsMargins(12, 0, 12, 0)
        nav_layout.setSpacing(6)
        
        for item in MENU_ITEMS:
            nav = NavItem(item["text"], item["icon"], item["id"], item["color"])
            nav_layout.addWidget(nav)
            self.nav_items[item["id"]] = nav
        
        layout.addWidget(nav_container)
        layout.addStretch()
        
        # Bottom section
        bottom = QWidget()
        bottom_layout = QVBoxLayout(bottom)
        bottom_layout.setContentsMargins(16, 10, 16, 20)
        
        # Connection status - cute rounded
        conn_frame = QFrame()
        conn_frame.setStyleSheet(f"""
            background: {COLORS['bg_card']};
            border: 2px solid {COLORS['border']};
            border-radius: 14px;
        """)
        conn_layout = QHBoxLayout(conn_frame)
        conn_layout.setContentsMargins(14, 12, 14, 12)
        
        self.conn_dot = PulsingDot(COLORS['text_muted'])
        conn_layout.addWidget(self.conn_dot)
        
        self.conn_text = QLabel("CHECKING...")
        self.conn_text.setStyleSheet(f"""
            color: {COLORS['text_muted']};
            font-size: 11px;
            letter-spacing: 1px;
        """)
        conn_layout.addWidget(self.conn_text)
        conn_layout.addStretch()
        
        conn_cat = QLabel("🐱")
        conn_layout.addWidget(conn_cat)
        
        bottom_layout.addWidget(conn_frame)
        
        # Version
        version = QLabel("v2.0.77 ✦ CUTE CAT")
        version.setStyleSheet(f"""
            color: {COLORS['text_muted']};
            font-size: 10px;
            margin-top: 12px;
        """)
        version.setAlignment(Qt.AlignCenter)
        bottom_layout.addWidget(version)
        
        layout.addWidget(bottom)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Background
        painter.fillRect(self.rect(), QColor(COLORS['bg_darker']))
        
        # Right border - gradient
        gradient = QLinearGradient(self.width() - 2, 0, self.width() - 2, self.height())
        gradient.setColorAt(0, QColor(COLORS['neon_pink']))
        gradient.setColorAt(0.5, QColor(COLORS['neon_purple']))
        gradient.setColorAt(1, QColor(COLORS['neon_cyan']))
        
        painter.setPen(QPen(QBrush(gradient), 3))
        painter.drawLine(self.width() - 2, 0, self.width() - 2, self.height())
    
    def set_connection(self, connected: bool):
        if connected:
            self.conn_dot.color = QColor(COLORS['neon_mint'])
            self.conn_text.setText("CONNECTED 😸")
            self.conn_text.setStyleSheet(f"color: {COLORS['neon_mint']}; font-size: 11px;")
        else:
            self.conn_dot.color = QColor(COLORS['neon_coral'])
            self.conn_text.setText("OFFLINE 😿")
            self.conn_text.setStyleSheet(f"color: {COLORS['neon_coral']}; font-size: 11px;")


class ProfilesPage(QWidget):
    """Profiles tab cute 🐱"""
    
    def __init__(self, log_func, parent=None):
        super().__init__(parent)
        self.log = log_func
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(24)
        
        # Title
        title = CyberTitle("Profiles", "Quản lý tài khoản Hidemium Browser", "pink")
        layout.addWidget(title)
        
        # Stats row
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(18)
        
        self.stat_total = CyberStatCard("TỔNG PROFILES", "0", "▲ +0 tuần này", "pink")
        self.stat_running = CyberStatCard("ĐANG CHẠY", "0", "● Active", "mint")
        self.stat_folders = CyberStatCard("FOLDERS", "0", "Categories", "purple")
        self.stat_scripts = CyberStatCard("SCRIPTS", "0", "Automation", "yellow")
        
        stats_layout.addWidget(self.stat_total)
        stats_layout.addWidget(self.stat_running)
        stats_layout.addWidget(self.stat_folders)
        stats_layout.addWidget(self.stat_scripts)
        
        layout.addLayout(stats_layout)
        
        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.setSpacing(14)
        
        search = CyberInput("🔍 Tìm kiếm profile...")
        search.setFixedWidth(300)
        toolbar.addWidget(search)
        
        folder_combo = CyberComboBox(["📁 Tất cả thư mục"])
        toolbar.addWidget(folder_combo)
        
        toolbar.addStretch()
        
        btn_refresh = CyberButton("REFRESH", "ghost", "⟳")
        toolbar.addWidget(btn_refresh)
        
        btn_sync = CyberButton("SYNC", "cyan", "🔄")
        btn_sync.clicked.connect(lambda: self.log("Syncing profiles ~nyaa", "info"))
        toolbar.addWidget(btn_sync)
        
        btn_create = CyberButton("CREATE", "success", "➕")
        toolbar.addWidget(btn_create)
        
        layout.addLayout(toolbar)
        
        # Table card
        card = CyberCard(COLORS['neon_pink'])
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(4, 4, 4, 4)
        
        # Card header
        header = QFrame()
        header.setFixedHeight(56)
        header.setStyleSheet(f"""
            background: {COLORS['bg_darker']};
            border-radius: 16px 16px 0 0;
        """)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(22, 0, 22, 0)
        
        header_title = QLabel("😺 PROFILE DATABASE")
        header_title.setStyleSheet(f"""
            color: {COLORS['neon_pink']};
            font-size: 14px;
            font-weight: bold;
            letter-spacing: 2px;
        """)
        header_layout.addWidget(header_title)
        
        self.count_label = QLabel("[0 profiles]")
        self.count_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 13px;")
        header_layout.addWidget(self.count_label)
        
        header_layout.addStretch()
        
        header_cat = QLabel("🐱✦🐱✦🐱")
        header_cat.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px;")
        header_layout.addWidget(header_cat)
        
        card_layout.addWidget(header)
        
        # Table
        self.table = CyberTable(["", "PROFILE", "STATUS", "PLATFORM", "FOLDER", "LAST", "ACTION"])
        card_layout.addWidget(self.table)
        
        layout.addWidget(card)
        
        # Load data
        QTimer.singleShot(500, self._load_sample_data)
    
    def _load_sample_data(self):
        self.stat_total.set_value("247")
        self.stat_running.set_value("18")
        self.stat_folders.set_value("12")
        self.stat_scripts.set_value("34")
        self.count_label.setText("[247 profiles]")
        self.log("Loaded 247 profiles ~nyaa", "success")


class LogPanel(QWidget):
    """Log panel cute rounded 🐱"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(360)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QWidget()
        header.setFixedHeight(56)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        
        title = QLabel("😸 TERMINAL")
        title.setStyleSheet(f"""
            color: {COLORS['neon_mint']};
            font-size: 14px;
            font-weight: bold;
            letter-spacing: 2px;
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        btn_clear = CyberButton("CLEAR", "danger")
        btn_clear.setFixedHeight(34)
        btn_clear.clicked.connect(self._clear)
        header_layout.addWidget(btn_clear)
        
        layout.addWidget(header)
        
        # Terminal
        self.terminal = CyberTerminal()
        layout.addWidget(self.terminal)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Background
        painter.fillRect(self.rect(), QColor(COLORS['bg_darker']))
        
        # Left border gradient
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(COLORS['neon_mint']))
        gradient.setColorAt(0.5, QColor(COLORS['neon_cyan']))
        gradient.setColorAt(1, QColor(COLORS['neon_purple']))
        
        painter.setPen(QPen(QBrush(gradient), 3))
        painter.drawLine(0, 0, 0, self.height())
    
    def add_line(self, message: str, level: str = "info"):
        self.terminal.add_line(message, level)
    
    def _clear(self):
        self.terminal.clear()


class StatusBar(QWidget):
    """Status bar cute 🐱"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(44)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        
        # Left
        left = QHBoxLayout()
        left.setSpacing(12)
        
        cat = QLabel("😺")
        left.addWidget(cat)
        
        dot = PulsingDot(COLORS['neon_mint'])
        left.addWidget(dot)
        
        status = QLabel("SYSTEM ONLINE")
        status.setStyleSheet(f"color: {COLORS['neon_mint']}; font-size: 12px; font-weight: bold;")
        left.addWidget(status)
        
        layout.addLayout(left)
        layout.addStretch()
        
        # Right
        version = QLabel("FB MANAGER PRO v2.0.77 ✦ CUTE CAT EDITION 🐱")
        version.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px;")
        layout.addWidget(version)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Background
        painter.fillRect(self.rect(), QColor(COLORS['bg_darker']))
        
        # Top border - gradient
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor(COLORS['neon_pink']))
        gradient.setColorAt(0.5, QColor(COLORS['neon_purple']))
        gradient.setColorAt(1, QColor(COLORS['neon_cyan']))
        
        painter.setPen(QPen(QBrush(gradient), 2))
        painter.drawLine(0, 0, self.width(), 0)


class MainWindow(QMainWindow):
    """Main window cute cat 🐱"""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("🐱 SonCuto - FB Manager Pro ✦ Cute Cat Edition")
        self.setMinimumSize(1400, 800)
        self.resize(1600, 900)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Content
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = Sidebar()
        content_layout.addWidget(self.sidebar)
        
        # Main area
        self.main_container = QWidget()
        self.main_container.setStyleSheet(f"background: {COLORS['bg_dark']};")
        main_container_layout = QVBoxLayout(self.main_container)
        main_container_layout.setContentsMargins(0, 0, 0, 0)
        main_container_layout.setSpacing(0)
        
        # Pages
        self.pages = QStackedWidget()
        
        # Log panel
        self.log_panel = LogPanel()
        
        # Create pages
        self.profiles_page = ProfilesPage(self.log)
        self.pages.addWidget(self.profiles_page)
        
        for tab_id in ["login", "pages", "reels", "content", "groups", "scripts", "posts"]:
            page = self._create_placeholder_page(tab_id)
            self.pages.addWidget(page)
        
        main_container_layout.addWidget(self.pages)
        
        content_layout.addWidget(self.main_container, 1)
        content_layout.addWidget(self.log_panel)
        
        main_layout.addWidget(content, 1)
        
        # Status bar
        self.status_bar = StatusBar()
        main_layout.addWidget(self.status_bar)
        
        # Effects
        self._setup_effects()
        
        # Navigation
        for tab_id, nav_item in self.sidebar.nav_items.items():
            nav_item.clicked_nav.connect(self._switch_tab)
        
        self._switch_tab("profiles")
        
        # Logs
        self.log("System boot complete ~nyaa", "success")
        self.log("FB Manager Pro v2.0.77", "info")
        self.log("Cute Cat Edition loaded 🐱", "info")
        
        QTimer.singleShot(1000, self._check_connection)
    
    def _setup_effects(self):
        self.grid = CyberGrid(self.main_container)
        self.grid.lower()
        
        self.rain = NeonRain(self.main_container)
        self.rain.lower()
        
        self.scanlines = ScanlineOverlay(self.main_container)
        self.scanlines.raise_()
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        w = self.main_container.width()
        h = self.main_container.height()
        self.grid.setGeometry(0, 0, w, h)
        self.rain.setGeometry(0, 0, w, h)
        self.scanlines.setGeometry(0, 0, w, h)
    
    def _create_placeholder_page(self, tab_id: str) -> QWidget:
        colors = {
            "login": "mint", "pages": "purple", "reels": "pink",
            "content": "yellow", "groups": "coral", "scripts": "cyan", "posts": "mint"
        }
        titles = {
            "login": "Login FB", "pages": "Pages", "reels": "Reels",
            "content": "Content", "groups": "Groups", "scripts": "Scripts", "posts": "Posts"
        }
        cats = {
            "login": "😺", "pages": "😸", "reels": "🐱",
            "content": "😻", "groups": "😽", "scripts": "🙀", "posts": "😹"
        }
        
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 28, 28, 28)
        
        title = CyberTitle(titles.get(tab_id, tab_id), f"Quản lý {titles.get(tab_id, tab_id)}", colors.get(tab_id, "pink"))
        layout.addWidget(title)
        
        # Placeholder
        placeholder_card = CyberCard(COLORS.get(f"neon_{colors.get(tab_id, 'pink')}", COLORS['neon_pink']))
        placeholder_card_layout = QVBoxLayout(placeholder_card)
        placeholder_card_layout.setContentsMargins(60, 100, 60, 100)
        
        cat_emoji = cats.get(tab_id, "🐱")
        placeholder = QLabel(f"{cat_emoji}\n\n{titles.get(tab_id, tab_id).upper()}\n\nTính năng đang phát triển ~nyaa")
        placeholder.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 18px;")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder_card_layout.addWidget(placeholder)
        
        layout.addWidget(placeholder_card)
        layout.addStretch()
        
        return page
    
    def _switch_tab(self, tab_id: str):
        for tid, nav in self.sidebar.nav_items.items():
            nav.set_active(tid == tab_id)
        
        tab_indices = {
            "profiles": 0, "login": 1, "pages": 2, "reels": 3,
            "content": 4, "groups": 5, "scripts": 6, "posts": 7
        }
        self.pages.setCurrentIndex(tab_indices.get(tab_id, 0))
        
        self.log(f"▸ {tab_id.upper()} 😺", "info")
    
    def _check_connection(self):
        self.sidebar.set_connection(False)
        self.log("Hidemium not connected 😿", "warning")
    
    def log(self, message: str, level: str = "info"):
        self.log_panel.add_line(message, level)


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(CYBERPUNK_QSS)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
