"""
FB Manager Pro - Main Application
PySide6 with Cyberpunk 2077 Theme
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFrame, QLabel, QStackedWidget, QScrollArea, QSizePolicy,
    QSpacerItem, QGridLayout
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QFontDatabase, QColor

from config import COLORS, MENU_ITEMS, CYBERPUNK_QSS
from widgets import (
    CyberButton, CyberInput, CyberComboBox, CyberCard, CyberStatCard,
    CyberTitle, NavItem, CyberTerminal, CyberTable,
    ScanlineOverlay, NeonRain, CyberGrid, PulsingDot, GlitchText, NeonFlash
)


class Sidebar(QFrame):
    """Sidebar với navigation"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(240)
        
        self.setStyleSheet(f"""
            QFrame#sidebar {{
                background: qlineargradient(y1:0, y2:1, stop:0 #05050a, stop:1 #020204);
                border-right: 2px solid qlineargradient(y1:0, y2:1, 
                    stop:0 {COLORS['neon_cyan']}, 
                    stop:0.5 {COLORS['neon_magenta']}, 
                    stop:1 {COLORS['neon_cyan']});
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Logo section
        logo_section = QWidget()
        logo_layout = QHBoxLayout(logo_section)
        logo_layout.setContentsMargins(16, 20, 16, 20)
        
        # Logo box
        logo_box = QFrame()
        logo_box.setFixedSize(50, 50)
        logo_box.setStyleSheet(f"""
            background: {COLORS['neon_cyan']};
            border-radius: 12px;
        """)
        logo_box_layout = QVBoxLayout(logo_box)
        logo_box_layout.setAlignment(Qt.AlignCenter)
        logo_text = QLabel("SC")
        logo_text.setStyleSheet(f"""
            color: {COLORS['bg_dark']};
            font-size: 18px;
            font-weight: bold;
            font-family: 'Orbitron', sans-serif;
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
            font-size: 14px;
            font-weight: bold;
            letter-spacing: 1px;
        """)
        title_layout.addWidget(main_title)
        
        sub_title = QLabel("FB MANAGER PRO")
        sub_title.setStyleSheet(f"""
            color: {COLORS['neon_cyan']};
            font-size: 9px;
            letter-spacing: 2px;
        """)
        title_layout.addWidget(sub_title)
        
        logo_layout.addWidget(title_widget)
        logo_layout.addStretch()
        layout.addWidget(logo_section)
        
        # Divider
        divider = QFrame()
        divider.setFixedHeight(1)
        divider.setStyleSheet(f"""
            background: qlineargradient(x1:0, x2:1, 
                stop:0 transparent, stop:0.5 {COLORS['neon_cyan']}, stop:1 transparent);
            margin: 0 16px;
        """)
        layout.addWidget(divider)
        
        # Menu label
        menu_label = QLabel("◢ MAIN MENU")
        menu_label.setStyleSheet(f"""
            color: {COLORS['neon_cyan']};
            font-size: 9px;
            letter-spacing: 3px;
            padding: 16px 20px 8px 20px;
        """)
        layout.addWidget(menu_label)
        
        # Navigation
        self.nav_items = {}
        nav_container = QWidget()
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setContentsMargins(8, 0, 8, 0)
        nav_layout.setSpacing(2)
        
        for item in MENU_ITEMS:
            nav = NavItem(item["text"], item["icon"], item["id"], item["color"])
            nav_layout.addWidget(nav)
            self.nav_items[item["id"]] = nav
        
        layout.addWidget(nav_container)
        layout.addStretch()
        
        # Bottom section
        bottom = QWidget()
        bottom_layout = QVBoxLayout(bottom)
        bottom_layout.setContentsMargins(12, 0, 12, 16)
        
        # Connection status
        conn_frame = QFrame()
        conn_frame.setStyleSheet(f"""
            background: {COLORS['bg_hover']};
            border-radius: 8px;
            padding: 10px;
        """)
        conn_layout = QHBoxLayout(conn_frame)
        conn_layout.setContentsMargins(12, 10, 12, 10)
        
        self.conn_dot = PulsingDot(COLORS['text_muted'])
        conn_layout.addWidget(self.conn_dot)
        
        self.conn_text = QLabel("CHECKING...")
        self.conn_text.setStyleSheet(f"""
            color: {COLORS['text_muted']};
            font-size: 10px;
            letter-spacing: 1px;
        """)
        conn_layout.addWidget(self.conn_text)
        conn_layout.addStretch()
        
        bottom_layout.addWidget(conn_frame)
        
        # Settings
        settings_btn = NavItem("Settings", "⚙️", "settings", "cyan")
        bottom_layout.addWidget(settings_btn)
        
        # Version
        version = QLabel("v2.0.77 // CYBERPUNK")
        version.setStyleSheet(f"""
            color: {COLORS['text_muted']};
            font-size: 9px;
            letter-spacing: 1px;
        """)
        version.setAlignment(Qt.AlignCenter)
        bottom_layout.addWidget(version)
        
        layout.addWidget(bottom)
    
    def set_connection(self, connected: bool):
        if connected:
            self.conn_dot.color = QColor(COLORS['neon_green'])
            self.conn_text.setText("HIDEMIUM ONLINE")
            self.conn_text.setStyleSheet(f"color: {COLORS['neon_green']}; font-size: 10px;")
        else:
            self.conn_dot.color = QColor(COLORS['neon_red'])
            self.conn_text.setText("HIDEMIUM OFFLINE")
            self.conn_text.setStyleSheet(f"color: {COLORS['neon_red']}; font-size: 10px;")


class ProfilesPage(QWidget):
    """Profiles tab content"""
    
    def __init__(self, log_func, parent=None):
        super().__init__(parent)
        self.log = log_func
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
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
        
        search = CyberInput("🔍 SEARCH...")
        search.setFixedWidth(280)
        toolbar.addWidget(search)
        
        folder_combo = CyberComboBox(["ALL FOLDERS"])
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
        card = CyberCard()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        
        # Card header
        header = QFrame()
        header.setStyleSheet(f"""
            background: rgba(0, 240, 255, 0.03);
            border-bottom: 1px solid {COLORS['border']};
            border-radius: 12px 12px 0 0;
        """)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 16, 20, 16)
        
        bar = QFrame()
        bar.setFixedSize(4, 24)
        bar.setStyleSheet(f"background: {COLORS['neon_cyan']}; border-radius: 2px;")
        header_layout.addWidget(bar)
        
        header_title = QLabel("PROFILE DATABASE")
        header_title.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 12px;
            font-weight: bold;
            letter-spacing: 2px;
        """)
        header_layout.addWidget(header_title)
        
        self.count_label = QLabel("[0]")
        self.count_label.setStyleSheet(f"color: {COLORS['neon_cyan']}; font-size: 12px; font-weight: bold;")
        header_layout.addWidget(self.count_label)
        
        header_layout.addStretch()
        card_layout.addWidget(header)
        
        # Table
        self.table = CyberTable(["", "PROFILE", "STATUS", "PLATFORM", "FOLDER", "LAST", "ACTION"])
        card_layout.addWidget(self.table)
        
        layout.addWidget(card)
        
        # Load sample data
        QTimer.singleShot(500, self._load_sample_data)
    
    def _load_sample_data(self):
        self.stat_total.set_value("247")
        self.stat_running.set_value("18")
        self.stat_folders.set_value("12")
        self.stat_scripts.set_value("34")
        self.count_label.setText("[247]")
        self.log("Loaded 247 profiles", "success")


class LogPanel(QFrame):
    """Log panel bên phải"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(360)
        self.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(y1:0, y2:1, stop:0 #05050a, stop:1 #020204);
                border-left: 2px solid {COLORS['neon_green']};
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 16, 16, 16)
        
        title = QLabel("◢ TERMINAL LOG")
        title.setStyleSheet(f"""
            color: {COLORS['neon_green']};
            font-size: 11px;
            font-weight: bold;
            letter-spacing: 2px;
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        btn_clear = CyberButton("CLEAR", "danger")
        btn_clear.setFixedSize(60, 28)
        btn_clear.clicked.connect(self._clear)
        header_layout.addWidget(btn_clear)
        
        layout.addWidget(header)
        
        # Terminal
        self.terminal = CyberTerminal()
        layout.addWidget(self.terminal)
    
    def add_line(self, message: str, level: str = "info"):
        self.terminal.add_line(message, level)
    
    def _clear(self):
        self.terminal.clear()


class StatusBar(QFrame):
    """Status bar dưới cùng"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(36)
        self.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['bg_darker']};
                border-top: 1px solid {COLORS['neon_cyan']};
            }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        
        # Left
        left = QHBoxLayout()
        
        dot = PulsingDot(COLORS['neon_green'])
        left.addWidget(dot)
        
        status = QLabel("ONLINE")
        status.setStyleSheet(f"color: {COLORS['neon_green']}; font-size: 10px;")
        left.addWidget(status)
        
        layout.addLayout(left)
        layout.addStretch()
        
        # Right
        right = QHBoxLayout()
        right.setSpacing(20)
        
        hidemium = QLabel("HIDEMIUM: <span style='color:#00ff66'>OK</span>")
        hidemium.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 10px;")
        right.addWidget(hidemium)
        
        version = QLabel("v2.0.77")
        version.setStyleSheet(f"color: {COLORS['neon_cyan']}; font-size: 10px;")
        right.addWidget(version)
        
        layout.addLayout(right)


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("SonCuto - FB Manager Pro")
        self.setMinimumSize(1400, 800)
        self.resize(1600, 900)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        # Main layout
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Content area
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = Sidebar()
        content_layout.addWidget(self.sidebar)
        
        # Main area with effects
        main_area = QWidget()
        main_area.setStyleSheet(f"background: {COLORS['bg_dark']};")
        main_area_layout = QVBoxLayout(main_area)
        main_area_layout.setContentsMargins(0, 0, 0, 0)
        main_area_layout.setSpacing(0)
        
        # Pages stack
        self.pages = QStackedWidget()
        
        # Log panel reference for pages
        self.log_panel = LogPanel()
        
        # Create pages
        self.profiles_page = ProfilesPage(self.log)
        self.pages.addWidget(self.profiles_page)
        
        # Placeholder pages
        for tab_id in ["login", "pages", "reels", "content", "groups", "scripts", "posts"]:
            page = self._create_placeholder_page(tab_id)
            self.pages.addWidget(page)
        
        main_area_layout.addWidget(self.pages)
        
        content_layout.addWidget(main_area, 1)
        content_layout.addWidget(self.log_panel)
        
        main_layout.addWidget(content, 1)
        
        # Status bar
        self.status_bar = StatusBar()
        main_layout.addWidget(self.status_bar)
        
        # Effects overlays
        self._setup_effects()
        
        # Connect navigation
        for tab_id, nav_item in self.sidebar.nav_items.items():
            nav_item.clicked_nav.connect(self._switch_tab)
        
        # Set initial tab
        self._switch_tab("profiles")
        
        # Startup logs
        self.log("System boot complete", "success")
        self.log("FB Manager Pro v2.0.77", "info")
        
        # Check connection
        QTimer.singleShot(1000, self._check_connection)
    
    def _setup_effects(self):
        """Setup Cyberpunk effects - ENHANCED"""
        # Grid background
        self.grid = CyberGrid(self)
        self.grid.lower()
        
        # Neon rain - more particles
        self.rain = NeonRain(self)
        self.rain.lower()
        
        # Neon flash effect
        self.flash = NeonFlash(self)
        
        # Scanlines (on top)
        self.scanlines = ScanlineOverlay(self)
        self.scanlines.raise_()
    
    def resizeEvent(self, event):
        """Resize effects with window"""
        super().resizeEvent(event)
        self.grid.setGeometry(0, 0, self.width(), self.height())
        self.rain.setGeometry(0, 0, self.width(), self.height())
        self.flash.setGeometry(0, 0, self.width(), self.height())
        self.scanlines.setGeometry(0, 0, self.width(), self.height())
    
    def _create_placeholder_page(self, tab_id: str) -> QWidget:
        """Create placeholder page"""
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
        layout.setContentsMargins(28, 28, 28, 28)
        
        title = CyberTitle(titles.get(tab_id, tab_id), f"Quản lý {titles.get(tab_id, tab_id)}", colors.get(tab_id, "cyan"))
        layout.addWidget(title)
        
        placeholder = QLabel(f"🚧 {titles.get(tab_id, tab_id).upper()} - Coming soon...")
        placeholder.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 16px;")
        placeholder.setAlignment(Qt.AlignCenter)
        layout.addWidget(placeholder, 1)
        
        return page
    
    def _switch_tab(self, tab_id: str):
        """Switch to tab"""
        # Update nav items
        for tid, nav in self.sidebar.nav_items.items():
            nav.set_active(tid == tab_id)
        
        # Switch page
        tab_indices = {
            "profiles": 0, "login": 1, "pages": 2, "reels": 3,
            "content": 4, "groups": 5, "scripts": 6, "posts": 7
        }
        self.pages.setCurrentIndex(tab_indices.get(tab_id, 0))
        
        self.log(f"→ {tab_id.upper()}", "info")
    
    def _check_connection(self):
        """Check Hidemium connection"""
        # Simulate - in real app, call API
        self.sidebar.set_connection(False)
        self.log("Hidemium not connected", "warning")
    
    def log(self, message: str, level: str = "info"):
        """Log to terminal"""
        self.log_panel.add_line(message, level)


def main():
    app = QApplication(sys.argv)
    
    # Apply stylesheet
    app.setStyleSheet(CYBERPUNK_QSS)
    
    # Create window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
