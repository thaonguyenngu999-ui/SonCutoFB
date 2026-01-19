"""
FB Manager Pro - Main Application
V3 - BIGGER & BOLDER CYBERPUNK
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


class Sidebar(QFrame):
    """Sidebar CYBERPUNK"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(240)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Logo section
        logo_section = QWidget()
        logo_section.setStyleSheet(f"background: {COLORS['bg_card']};")
        logo_layout = QHBoxLayout(logo_section)
        logo_layout.setContentsMargins(16, 20, 16, 20)
        
        # Logo box
        logo_box = QFrame()
        logo_box.setFixedSize(48, 48)
        logo_box.setStyleSheet(f"""
            background: {COLORS['neon_cyan']};
            border-radius: 4px;
        """)
        logo_box_layout = QVBoxLayout(logo_box)
        logo_box_layout.setAlignment(Qt.AlignCenter)
        logo_text = QLabel("SC")
        logo_text.setStyleSheet(f"""
            color: {COLORS['bg_dark']};
            font-size: 18px;
            font-weight: bold;
        """)
        logo_text.setAlignment(Qt.AlignCenter)
        logo_box_layout.addWidget(logo_text)
        logo_layout.addWidget(logo_box)
        
        # Logo title
        title_widget = QWidget()
        title_layout = QVBoxLayout(title_widget)
        title_layout.setContentsMargins(12, 0, 0, 0)
        title_layout.setSpacing(2)
        
        main_title = QLabel("SonCuto")
        main_title.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 16px;
            font-weight: bold;
        """)
        title_layout.addWidget(main_title)
        
        sub_title = QLabel("FB MANAGER PRO")
        sub_title.setStyleSheet(f"""
            color: {COLORS['neon_cyan']};
            font-size: 10px;
            letter-spacing: 2px;
        """)
        title_layout.addWidget(sub_title)
        
        logo_layout.addWidget(title_widget)
        logo_layout.addStretch()
        layout.addWidget(logo_section)
        
        # Divider
        divider = QFrame()
        divider.setFixedHeight(3)
        divider.setStyleSheet(f"background: {COLORS['neon_cyan']};")
        layout.addWidget(divider)
        
        # Menu label
        menu_label = QLabel("◢ MAIN MENU")
        menu_label.setStyleSheet(f"""
            color: {COLORS['text_muted']};
            font-size: 11px;
            letter-spacing: 3px;
            padding: 18px 20px 10px 20px;
            background: {COLORS['bg_darker']};
        """)
        layout.addWidget(menu_label)
        
        # Navigation
        self.nav_items = {}
        nav_container = QWidget()
        nav_container.setStyleSheet(f"background: {COLORS['bg_darker']};")
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setContentsMargins(8, 0, 8, 0)
        nav_layout.setSpacing(4)
        
        for item in MENU_ITEMS:
            nav = NavItem(item["text"], item["icon"], item["id"], item["color"])
            nav_layout.addWidget(nav)
            self.nav_items[item["id"]] = nav
        
        layout.addWidget(nav_container)
        layout.addStretch()
        
        # Bottom section
        bottom = QWidget()
        bottom.setStyleSheet(f"background: {COLORS['bg_darker']};")
        bottom_layout = QVBoxLayout(bottom)
        bottom_layout.setContentsMargins(12, 10, 12, 16)
        
        # Connection status
        conn_frame = QFrame()
        conn_frame.setStyleSheet(f"""
            background: {COLORS['bg_card']};
            border: 2px solid {COLORS['border']};
            border-left: 4px solid {COLORS['text_muted']};
        """)
        conn_layout = QHBoxLayout(conn_frame)
        conn_layout.setContentsMargins(12, 10, 12, 10)
        
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
        
        bottom_layout.addWidget(conn_frame)
        
        # Version
        version = QLabel("v2.0.77 // CYBERPUNK")
        version.setStyleSheet(f"""
            color: {COLORS['text_muted']};
            font-size: 10px;
            margin-top: 10px;
        """)
        version.setAlignment(Qt.AlignCenter)
        bottom_layout.addWidget(version)
        
        layout.addWidget(bottom)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Background
        painter.fillRect(self.rect(), QColor(COLORS['bg_darker']))
        
        # Right border gradient
        gradient = QLinearGradient(self.width() - 3, 0, self.width() - 3, self.height())
        gradient.setColorAt(0, QColor(COLORS['neon_cyan']))
        gradient.setColorAt(0.5, QColor(COLORS['neon_magenta']))
        gradient.setColorAt(1, QColor(COLORS['neon_cyan']))
        
        painter.setPen(QPen(QBrush(gradient), 3))
        painter.drawLine(self.width() - 2, 0, self.width() - 2, self.height())
    
    def set_connection(self, connected: bool):
        if connected:
            self.conn_dot.color = QColor(COLORS['neon_green'])
            self.conn_text.setText("HIDEMIUM OK")
            self.conn_text.setStyleSheet(f"color: {COLORS['neon_green']}; font-size: 11px;")
        else:
            self.conn_dot.color = QColor(COLORS['neon_red'])
            self.conn_text.setText("OFFLINE")
            self.conn_text.setStyleSheet(f"color: {COLORS['neon_red']}; font-size: 11px;")


class ProfilesPage(QWidget):
    """Profiles tab - CYBERPUNK"""
    
    def __init__(self, log_func, parent=None):
        super().__init__(parent)
        self.log = log_func
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Title
        title = CyberTitle("Profiles", "Quản lý tài khoản Hidemium Browser", "cyan")
        layout.addWidget(title)
        
        # Stats row
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)
        
        self.stat_total = CyberStatCard("TỔNG PROFILES", "0", "▲ +0 tuần này", "cyan")
        self.stat_running = CyberStatCard("ĐANG CHẠY", "0", "● Active", "green")
        self.stat_folders = CyberStatCard("FOLDERS", "0", "Categories", "purple")
        self.stat_scripts = CyberStatCard("SCRIPTS", "0", "Automation", "yellow")
        
        stats_layout.addWidget(self.stat_total)
        stats_layout.addWidget(self.stat_running)
        stats_layout.addWidget(self.stat_folders)
        stats_layout.addWidget(self.stat_scripts)
        
        layout.addLayout(stats_layout)
        
        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.setSpacing(12)
        
        search = CyberInput("🔍 Tìm kiếm profile...")
        search.setFixedWidth(280)
        toolbar.addWidget(search)
        
        folder_combo = CyberComboBox(["Tất cả thư mục"])
        toolbar.addWidget(folder_combo)
        
        toolbar.addStretch()
        
        btn_refresh = CyberButton("REFRESH", "ghost", "⟳")
        toolbar.addWidget(btn_refresh)
        
        btn_sync = CyberButton("SYNC", "primary", "🔄")
        btn_sync.clicked.connect(lambda: self.log("Syncing profiles...", "info"))
        toolbar.addWidget(btn_sync)
        
        btn_create = CyberButton("CREATE", "success", "➕")
        toolbar.addWidget(btn_create)
        
        layout.addLayout(toolbar)
        
        # Table card
        card = CyberCard(COLORS['neon_cyan'])
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(2, 2, 2, 2)
        
        # Card header
        header = QFrame()
        header.setFixedHeight(52)
        header.setStyleSheet(f"background: {COLORS['bg_darker']};")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        
        header_title = QLabel("◢ PROFILE DATABASE")
        header_title.setStyleSheet(f"""
            color: {COLORS['neon_cyan']};
            font-size: 14px;
            font-weight: bold;
            letter-spacing: 3px;
        """)
        header_layout.addWidget(header_title)
        
        self.count_label = QLabel("[0 profiles]")
        self.count_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 13px;")
        header_layout.addWidget(self.count_label)
        
        header_layout.addStretch()
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
        self.log("Loaded 247 profiles", "success")


class LogPanel(QWidget):
    """Log panel CYBERPUNK"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(340)
        self.corner_size = 0
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QWidget()
        header.setFixedHeight(50)
        header.setStyleSheet(f"background: {COLORS['bg_card']};")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 0, 16, 0)
        
        title = QLabel("◢ TERMINAL")
        title.setStyleSheet(f"""
            color: {COLORS['neon_green']};
            font-size: 13px;
            font-weight: bold;
            letter-spacing: 3px;
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        btn_clear = CyberButton("CLEAR", "danger")
        btn_clear.setFixedHeight(32)
        btn_clear.clicked.connect(self._clear)
        header_layout.addWidget(btn_clear)
        
        layout.addWidget(header)
        
        # Terminal
        self.terminal = CyberTerminal()
        layout.addWidget(self.terminal)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Background
        painter.fillRect(self.rect(), QColor(COLORS['bg_darker']))
        
        # Left border
        painter.setPen(QPen(QColor(COLORS['neon_green']), 3))
        painter.drawLine(0, 0, 0, self.height())
    
    def add_line(self, message: str, level: str = "info"):
        self.terminal.add_line(message, level)
    
    def _clear(self):
        self.terminal.clear()


class StatusBar(QWidget):
    """Status bar CYBERPUNK"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(40)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        
        # Left
        left = QHBoxLayout()
        left.setSpacing(10)
        
        dot = PulsingDot(COLORS['neon_green'])
        left.addWidget(dot)
        
        status = QLabel("SYSTEM ONLINE")
        status.setStyleSheet(f"color: {COLORS['neon_green']}; font-size: 12px; font-weight: bold;")
        left.addWidget(status)
        
        layout.addLayout(left)
        layout.addStretch()
        
        # Right
        version = QLabel("FB MANAGER PRO v2.0.77 // CYBERPUNK EDITION")
        version.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px; letter-spacing: 1px;")
        layout.addWidget(version)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Background
        painter.fillRect(self.rect(), QColor(COLORS['bg_darker']))
        
        # Top border
        painter.setPen(QPen(QColor(COLORS['neon_cyan']), 2))
        painter.drawLine(0, 0, self.width(), 0)


class MainWindow(QMainWindow):
    """Main window"""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("SonCuto - FB Manager Pro // CYBERPUNK")
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
        self.log("System boot complete", "success")
        self.log("FB Manager Pro v2.0.77", "info")
        self.log("Cyberpunk Edition loaded", "info")
        
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
            "login": "green", "pages": "purple", "reels": "magenta",
            "content": "yellow", "groups": "orange", "scripts": "cyan", "posts": "green"
        }
        titles = {
            "login": "Login FB", "pages": "Pages", "reels": "Reels",
            "content": "Content", "groups": "Groups", "scripts": "Scripts", "posts": "Posts"
        }
        
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 24, 24, 24)
        
        title = CyberTitle(titles.get(tab_id, tab_id), f"Quản lý {titles.get(tab_id, tab_id)}", colors.get(tab_id, "cyan"))
        layout.addWidget(title)
        
        # Placeholder
        placeholder_card = CyberCard(COLORS.get(f"neon_{colors.get(tab_id, 'cyan')}"))
        placeholder_card_layout = QVBoxLayout(placeholder_card)
        placeholder_card_layout.setContentsMargins(50, 80, 50, 80)
        
        placeholder = QLabel(f"🚧 {titles.get(tab_id, tab_id).upper()}\n\nTính năng đang phát triển...")
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
        
        self.log(f"▸ {tab_id.upper()}", "info")
    
    def _check_connection(self):
        self.sidebar.set_connection(False)
        self.log("Hidemium not connected", "warning")
    
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
