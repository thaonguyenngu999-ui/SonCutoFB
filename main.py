"""
FB Manager Pro - Main Application
🐱 CUTE CAT Edition - DATA FOCUSED 🐱
Compact controls, BIG data display
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFrame, QLabel, QStackedWidget, QScrollArea, QSizePolicy,
    QSpacerItem, QGridLayout, QTableWidgetItem
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QColor, QPainter, QPen, QBrush, QLinearGradient, QPainterPath

from config import COLORS, MENU_ITEMS, CYBERPUNK_QSS
from widgets import (
    CyberButton, CyberInput, CyberComboBox, CyberCard, CyberStatCard,
    CyberTitle, NavItem, CyberTerminal, CyberTable,
    ScanlineOverlay, NeonRain, CyberGrid, PulsingDot, GlitchText, NeonFlash
)


class Sidebar(QWidget):
    """Sidebar COMPACT 🐱"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(200)  # SMALLER
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Logo section
        logo_section = QWidget()
        logo_section.setFixedHeight(70)  # SMALLER
        logo_layout = QHBoxLayout(logo_section)
        logo_layout.setContentsMargins(14, 12, 14, 12)
        
        # Logo
        logo_box = QFrame()
        logo_box.setFixedSize(40, 40)
        logo_box.setStyleSheet(f"""
            background: qlineargradient(x1:0, x2:1, stop:0 {COLORS['neon_pink']}, stop:1 {COLORS['neon_purple']});
            border-radius: 12px;
        """)
        logo_box_layout = QVBoxLayout(logo_box)
        logo_box_layout.setAlignment(Qt.AlignCenter)
        logo_text = QLabel("🐱")
        logo_text.setStyleSheet("font-size: 20px;")
        logo_text.setAlignment(Qt.AlignCenter)
        logo_box_layout.addWidget(logo_text)
        logo_layout.addWidget(logo_box)
        
        # Title
        title_widget = QWidget()
        title_layout = QVBoxLayout(title_widget)
        title_layout.setContentsMargins(10, 0, 0, 0)
        title_layout.setSpacing(0)
        
        main_title = QLabel("SonCuto")
        main_title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 14px; font-weight: bold;")
        title_layout.addWidget(main_title)
        
        sub_title = QLabel("FB MANAGER")
        sub_title.setStyleSheet(f"color: {COLORS['neon_pink']}; font-size: 9px; letter-spacing: 1px;")
        title_layout.addWidget(sub_title)
        
        logo_layout.addWidget(title_widget)
        logo_layout.addStretch()
        layout.addWidget(logo_section)
        
        # Divider
        divider = QFrame()
        divider.setFixedHeight(2)
        divider.setStyleSheet(f"""
            background: qlineargradient(x1:0, x2:1, stop:0 {COLORS['neon_pink']}, stop:1 {COLORS['neon_cyan']});
            margin: 0 12px;
        """)
        layout.addWidget(divider)
        
        # Navigation
        self.nav_items = {}
        nav_container = QWidget()
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setContentsMargins(8, 12, 8, 0)
        nav_layout.setSpacing(4)
        
        for item in MENU_ITEMS:
            nav = NavItem(item["text"], item["icon"], item["id"], item["color"])
            nav_layout.addWidget(nav)
            self.nav_items[item["id"]] = nav
        
        layout.addWidget(nav_container)
        layout.addStretch()
        
        # Connection status
        conn_frame = QWidget()
        conn_frame.setFixedHeight(36)
        conn_layout = QHBoxLayout(conn_frame)
        conn_layout.setContentsMargins(14, 0, 14, 12)
        
        self.conn_dot = PulsingDot(COLORS['text_muted'])
        conn_layout.addWidget(self.conn_dot)
        
        self.conn_text = QLabel("OFFLINE")
        self.conn_text.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 10px;")
        conn_layout.addWidget(self.conn_text)
        conn_layout.addStretch()
        
        layout.addWidget(conn_frame)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(COLORS['bg_darker']))
        
        gradient = QLinearGradient(self.width() - 2, 0, self.width() - 2, self.height())
        gradient.setColorAt(0, QColor(COLORS['neon_pink']))
        gradient.setColorAt(1, QColor(COLORS['neon_cyan']))
        
        painter.setPen(QPen(QBrush(gradient), 2))
        painter.drawLine(self.width() - 1, 0, self.width() - 1, self.height())
    
    def set_connection(self, connected: bool):
        if connected:
            self.conn_dot.color = QColor(COLORS['neon_mint'])
            self.conn_text.setText("CONNECTED 😸")
            self.conn_text.setStyleSheet(f"color: {COLORS['neon_mint']}; font-size: 10px;")
        else:
            self.conn_dot.color = QColor(COLORS['neon_coral'])
            self.conn_text.setText("OFFLINE 😿")
            self.conn_text.setStyleSheet(f"color: {COLORS['neon_coral']}; font-size: 10px;")


class ProfilesPage(QWidget):
    """Profiles tab - DATA FOCUSED 🐱"""
    
    def __init__(self, log_func, parent=None):
        super().__init__(parent)
        self.log = log_func
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)  # SMALLER margins
        layout.setSpacing(10)  # SMALLER spacing
        
        # Top bar: Title + Stats inline
        top_bar = QHBoxLayout()
        top_bar.setSpacing(16)
        
        # Title compact
        title = CyberTitle("Profiles", "Hidemium Browser", "pink")
        top_bar.addWidget(title)
        
        top_bar.addStretch()
        
        # Stats inline - COMPACT
        self.stat_total = CyberStatCard("TOTAL", "0", "😺", "pink")
        self.stat_total.setFixedWidth(140)
        top_bar.addWidget(self.stat_total)
        
        self.stat_running = CyberStatCard("RUNNING", "0", "🟢", "mint")
        self.stat_running.setFixedWidth(140)
        top_bar.addWidget(self.stat_running)
        
        self.stat_folders = CyberStatCard("FOLDERS", "0", "📁", "purple")
        self.stat_folders.setFixedWidth(140)
        top_bar.addWidget(self.stat_folders)
        
        layout.addLayout(top_bar)
        
        # Toolbar - COMPACT
        toolbar = QHBoxLayout()
        toolbar.setSpacing(8)
        
        search = CyberInput("🔍 Tìm kiếm...")
        search.setFixedWidth(220)
        toolbar.addWidget(search)
        
        folder_combo = CyberComboBox(["📁 Tất cả"])
        folder_combo.setFixedWidth(130)
        toolbar.addWidget(folder_combo)
        
        status_combo = CyberComboBox(["🔵 Tất cả", "🟢 Running", "⚪ Stopped"])
        status_combo.setFixedWidth(130)
        toolbar.addWidget(status_combo)
        
        toolbar.addStretch()
        
        btn_refresh = CyberButton("⟳", "ghost")
        btn_refresh.setFixedWidth(40)
        toolbar.addWidget(btn_refresh)
        
        btn_sync = CyberButton("SYNC", "cyan", "🔄")
        btn_sync.clicked.connect(lambda: self.log("Syncing...", "info"))
        toolbar.addWidget(btn_sync)
        
        btn_start = CyberButton("START ALL", "success", "▶")
        toolbar.addWidget(btn_start)
        
        btn_stop = CyberButton("STOP", "danger", "⏹")
        toolbar.addWidget(btn_stop)
        
        layout.addLayout(toolbar)
        
        # TABLE - BIG, takes most space
        table_card = CyberCard(COLORS['neon_pink'])
        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(2, 2, 2, 2)
        
        # Table header
        header = QWidget()
        header.setFixedHeight(36)
        header.setStyleSheet(f"background: {COLORS['bg_darker']}; border-radius: 14px 14px 0 0;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 0, 16, 0)
        
        header_title = QLabel("😺 PROFILES")
        header_title.setStyleSheet(f"color: {COLORS['neon_pink']}; font-size: 11px; font-weight: bold; letter-spacing: 2px;")
        header_layout.addWidget(header_title)
        
        self.count_label = QLabel("[0]")
        self.count_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px;")
        header_layout.addWidget(self.count_label)
        
        header_layout.addStretch()
        
        # Quick actions
        btn_select_all = CyberButton("Select All", "ghost")
        btn_select_all.setFixedHeight(26)
        header_layout.addWidget(btn_select_all)
        
        table_layout.addWidget(header)
        
        # Table
        self.table = CyberTable(["✓", "ID", "NAME", "STATUS", "PROXY", "FOLDER", "NOTES", "ACTIONS"])
        self.table.setColumnWidth(0, 40)   # Checkbox
        self.table.setColumnWidth(1, 80)   # ID
        self.table.setColumnWidth(2, 180)  # Name
        self.table.setColumnWidth(3, 100)  # Status
        self.table.setColumnWidth(4, 150)  # Proxy
        self.table.setColumnWidth(5, 100)  # Folder
        self.table.setColumnWidth(6, 150)  # Notes
        
        table_layout.addWidget(self.table)
        
        layout.addWidget(table_card, 1)  # Stretch factor 1 = take remaining space
        
        # Load data
        QTimer.singleShot(300, self._load_sample_data)
    
    def _load_sample_data(self):
        self.stat_total.set_value("247")
        self.stat_running.set_value("18")
        self.stat_folders.set_value("12")
        self.count_label.setText("[247 profiles]")
        
        # Sample data
        sample_data = [
            ["", "PRF001", "Account_Marketing_01", "🟢 Running", "103.152.x.x:8080", "Marketing", "Main account"],
            ["", "PRF002", "Account_Sales_02", "⚪ Stopped", "None", "Sales", ""],
            ["", "PRF003", "Account_Support_03", "🟢 Running", "103.152.x.x:8081", "Support", "Customer care"],
            ["", "PRF004", "Account_Dev_04", "🟡 Starting", "Auto", "Dev", "Testing"],
            ["", "PRF005", "Account_Marketing_05", "🟢 Running", "103.152.x.x:8082", "Marketing", ""],
            ["", "PRF006", "Account_HR_06", "⚪ Stopped", "None", "HR", "Recruitment"],
            ["", "PRF007", "Account_Finance_07", "🟢 Running", "103.152.x.x:8083", "Finance", "Reports"],
            ["", "PRF008", "Account_Marketing_08", "🟢 Running", "103.152.x.x:8084", "Marketing", "Ads"],
        ]
        
        self.table.setRowCount(len(sample_data))
        for row, data in enumerate(sample_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                if col == 3:  # Status column
                    if "Running" in value:
                        item.setForeground(QColor(COLORS['neon_mint']))
                    elif "Starting" in value:
                        item.setForeground(QColor(COLORS['neon_yellow']))
                self.table.setItem(row, col, item)
        
        self.log("Loaded 247 profiles", "success")


class LogPanel(QWidget):
    """Log panel COMPACT 🐱"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(280)  # SMALLER
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QWidget()
        header.setFixedHeight(40)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(12, 0, 12, 0)
        
        title = QLabel("😸 LOG")
        title.setStyleSheet(f"color: {COLORS['neon_mint']}; font-size: 11px; font-weight: bold; letter-spacing: 2px;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        btn_clear = CyberButton("✕", "danger")
        btn_clear.setFixedSize(28, 28)
        btn_clear.clicked.connect(self._clear)
        header_layout.addWidget(btn_clear)
        
        layout.addWidget(header)
        
        # Terminal
        self.terminal = CyberTerminal()
        layout.addWidget(self.terminal)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(COLORS['bg_darker']))
        
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(COLORS['neon_mint']))
        gradient.setColorAt(1, QColor(COLORS['neon_purple']))
        
        painter.setPen(QPen(QBrush(gradient), 2))
        painter.drawLine(0, 0, 0, self.height())
    
    def add_line(self, message: str, level: str = "info"):
        self.terminal.add_line(message, level)
    
    def _clear(self):
        self.terminal.clear()


class StatusBar(QWidget):
    """Status bar COMPACT 🐱"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(32)  # SMALLER
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        
        # Left
        dot = PulsingDot(COLORS['neon_mint'])
        layout.addWidget(dot)
        
        status = QLabel("ONLINE")
        status.setStyleSheet(f"color: {COLORS['neon_mint']}; font-size: 10px; font-weight: bold;")
        layout.addWidget(status)
        
        layout.addStretch()
        
        # Right
        version = QLabel("🐱 CUTE CAT v2.0.77")
        version.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 10px;")
        layout.addWidget(version)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(COLORS['bg_darker']))
        
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor(COLORS['neon_pink']))
        gradient.setColorAt(0.5, QColor(COLORS['neon_purple']))
        gradient.setColorAt(1, QColor(COLORS['neon_cyan']))
        
        painter.setPen(QPen(QBrush(gradient), 2))
        painter.drawLine(0, 0, self.width(), 0)


class MainWindow(QMainWindow):
    """Main window DATA FOCUSED 🐱"""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("🐱 SonCuto FB Manager - Cute Cat Edition")
        self.setMinimumSize(1200, 700)
        self.resize(1500, 850)
        
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
        self.log("System ready", "success")
        self.log("Cute Cat Edition 🐱", "info")
        
        QTimer.singleShot(500, self._check_connection)
    
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
        colors = {"login": "mint", "pages": "purple", "reels": "pink", "content": "yellow", "groups": "coral", "scripts": "cyan", "posts": "mint"}
        titles = {"login": "Login FB", "pages": "Pages", "reels": "Reels", "content": "Content", "groups": "Groups", "scripts": "Scripts", "posts": "Posts"}
        
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(16, 12, 16, 12)
        
        title = CyberTitle(titles.get(tab_id, tab_id), "", colors.get(tab_id, "pink"))
        layout.addWidget(title)
        
        placeholder_card = CyberCard(COLORS.get(f"neon_{colors.get(tab_id, 'pink')}", COLORS['neon_pink']))
        placeholder_layout = QVBoxLayout(placeholder_card)
        placeholder_layout.setContentsMargins(40, 60, 40, 60)
        
        placeholder = QLabel(f"🐱 {titles.get(tab_id, tab_id).upper()}\n\nĐang phát triển...")
        placeholder.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 16px;")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder_layout.addWidget(placeholder)
        
        layout.addWidget(placeholder_card, 1)
        
        return page
    
    def _switch_tab(self, tab_id: str):
        for tid, nav in self.sidebar.nav_items.items():
            nav.set_active(tid == tab_id)
        
        tab_indices = {"profiles": 0, "login": 1, "pages": 2, "reels": 3, "content": 4, "groups": 5, "scripts": 6, "posts": 7}
        self.pages.setCurrentIndex(tab_indices.get(tab_id, 0))
        
        self.log(f"→ {tab_id.upper()}", "info")
    
    def _check_connection(self):
        self.sidebar.set_connection(False)
        self.log("Hidemium offline", "warning")
    
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
