"""
FB Manager Pro - Main Application
🐱 CUTE CAT Edition - BEAUTIFUL 🐱
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFrame, QLabel, QStackedWidget, QTableWidgetItem
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QPainter, QPen, QBrush, QLinearGradient

from config import COLORS, MENU_ITEMS, CYBERPUNK_QSS
from widgets import (
    CyberButton, CyberInput, CyberComboBox, CyberCard, CyberStatCard,
    CyberTitle, NavItem, CyberTerminal, CyberTable, CyberCheckBox,
    ScanlineOverlay, NeonRain, CyberGrid, PulsingDot, GlitchText, NeonFlash
)


class Sidebar(QWidget):
    """Sidebar COMPACT 🐱"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(200)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Logo
        logo_section = QWidget()
        logo_section.setFixedHeight(70)
        logo_layout = QHBoxLayout(logo_section)
        logo_layout.setContentsMargins(14, 12, 14, 12)
        
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
        
        divider = QFrame()
        divider.setFixedHeight(2)
        divider.setStyleSheet(f"background: qlineargradient(x1:0, x2:1, stop:0 {COLORS['neon_pink']}, stop:1 {COLORS['neon_cyan']}); margin: 0 12px;")
        layout.addWidget(divider)
        
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
    """Profiles - BEAUTIFUL TABLE 🐱"""
    
    def __init__(self, log_func, parent=None):
        super().__init__(parent)
        self.log = log_func
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(10)
        
        # Top bar
        top_bar = QHBoxLayout()
        top_bar.setSpacing(12)
        
        title = CyberTitle("Profiles", "Hidemium", "pink")
        top_bar.addWidget(title)
        
        top_bar.addStretch()
        
        self.stat_total = CyberStatCard("TOTAL", "0", "😺", "pink")
        self.stat_total.setFixedWidth(160)
        top_bar.addWidget(self.stat_total)
        
        self.stat_running = CyberStatCard("RUNNING", "0", "🟢", "mint")
        self.stat_running.setFixedWidth(160)
        top_bar.addWidget(self.stat_running)
        
        self.stat_folders = CyberStatCard("FOLDERS", "0", "📁", "purple")
        self.stat_folders.setFixedWidth(160)
        top_bar.addWidget(self.stat_folders)
        
        layout.addLayout(top_bar)
        
        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.setSpacing(8)
        
        search = CyberInput("🔍 Tìm kiếm...")
        search.setFixedWidth(200)
        toolbar.addWidget(search)
        
        folder_combo = CyberComboBox(["📁 Tất cả", "📁 Marketing", "📁 Sales", "📁 Support"])
        folder_combo.setFixedWidth(140)
        toolbar.addWidget(folder_combo)
        
        toolbar.addStretch()
        
        btn_refresh = CyberButton("⟳", "ghost")
        btn_refresh.setFixedWidth(40)
        toolbar.addWidget(btn_refresh)
        
        btn_sync = CyberButton("SYNC", "cyan", "🔄")
        btn_sync.clicked.connect(lambda: self.log("Syncing...", "info"))
        toolbar.addWidget(btn_sync)
        
        layout.addLayout(toolbar)
        
        # Table card
        table_card = CyberCard(COLORS['neon_pink'])
        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(2, 2, 2, 2)
        
        # Header với Select All
        header = QWidget()
        header.setFixedHeight(44)
        header.setStyleSheet(f"background: {COLORS['bg_darker']}; border-radius: 14px 14px 0 0;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 0, 16, 0)
        header_layout.setSpacing(12)
        
        # Select All checkbox với label
        select_all_widget = QWidget()
        select_all_layout = QHBoxLayout(select_all_widget)
        select_all_layout.setContentsMargins(0, 0, 0, 0)
        select_all_layout.setSpacing(8)
        
        self.select_all_cb = CyberCheckBox()
        self.select_all_cb.stateChanged.connect(self._toggle_select_all)
        select_all_layout.addWidget(self.select_all_cb)
        
        select_all_label = QLabel("Chọn tất cả")
        select_all_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        select_all_label.setCursor(Qt.PointingHandCursor)
        select_all_label.mousePressEvent = lambda e: self.select_all_cb.setChecked(not self.select_all_cb.isChecked())
        select_all_layout.addWidget(select_all_label)
        
        header_layout.addWidget(select_all_widget)
        
        # Separator
        sep = QFrame()
        sep.setFixedWidth(2)
        sep.setFixedHeight(24)
        sep.setStyleSheet(f"background: {COLORS['border']};")
        header_layout.addWidget(sep)
        
        header_title = QLabel("😺 PROFILES")
        header_title.setStyleSheet(f"color: {COLORS['neon_pink']}; font-size: 12px; font-weight: bold; letter-spacing: 2px;")
        header_layout.addWidget(header_title)
        
        self.count_label = QLabel("[0]")
        self.count_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px;")
        header_layout.addWidget(self.count_label)
        
        header_layout.addStretch()
        
        # Selected count
        self.selected_label = QLabel("")
        self.selected_label.setStyleSheet(f"color: {COLORS['neon_cyan']}; font-size: 11px;")
        header_layout.addWidget(self.selected_label)
        
        table_layout.addWidget(header)
        
        # Table - checkbox, ID, NAME, FOLDER, ACTION (toggle)
        self.table = CyberTable(["✓", "ID", "NAME", "FOLDER", "ACTION"])
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 350)
        self.table.setColumnWidth(3, 150)
        
        table_layout.addWidget(self.table)
        
        layout.addWidget(table_card, 1)
        
        QTimer.singleShot(300, self._load_sample_data)
    
    def _toggle_select_all(self, state):
        checked = state == Qt.Checked
        count = 0
        for row in range(self.table.rowCount()):
            widget = self.table.cellWidget(row, 0)
            if widget:
                cb = widget.findChild(CyberCheckBox)
                if cb:
                    cb.setChecked(checked)
                    if checked:
                        count += 1
        
        if checked:
            self.selected_label.setText(f"✓ {count} đã chọn")
        else:
            self.selected_label.setText("")
    
    def _load_sample_data(self):
        self.stat_total.set_value("247")
        self.stat_running.set_value("18")
        self.stat_folders.set_value("12")
        self.count_label.setText("[247 profiles]")
        
        sample_data = [
            ["PRF001", "Account_Marketing_01", "Marketing"],
            ["PRF002", "Account_Sales_02", "Sales"],
            ["PRF003", "Account_Support_03", "Support"],
            ["PRF004", "Account_Dev_04", "Dev"],
            ["PRF005", "Account_Marketing_05", "Marketing"],
            ["PRF006", "Account_HR_06", "HR"],
            ["PRF007", "Account_Finance_07", "Finance"],
            ["PRF008", "Account_Marketing_08", "Marketing"],
            ["PRF009", "Account_Sales_09", "Sales"],
            ["PRF010", "Account_Admin_10", "Admin"],
            ["PRF011", "Account_Marketing_11", "Marketing"],
            ["PRF012", "Account_Support_12", "Support"],
        ]
        
        self.table.setRowCount(len(sample_data))
        for row, data in enumerate(sample_data):
            self.table.add_row_with_widgets(data, row)
        
        self.log("Loaded 247 profiles", "success")


class LogPanel(QWidget):
    """Log panel 🐱"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(280)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
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
    """Status bar 🐱"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(32)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        
        dot = PulsingDot(COLORS['neon_mint'])
        layout.addWidget(dot)
        
        status = QLabel("ONLINE")
        status.setStyleSheet(f"color: {COLORS['neon_mint']}; font-size: 10px; font-weight: bold;")
        layout.addWidget(status)
        
        layout.addStretch()
        
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
    """Main window 🐱"""
    
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
        
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        self.sidebar = Sidebar()
        content_layout.addWidget(self.sidebar)
        
        self.main_container = QWidget()
        self.main_container.setStyleSheet(f"background: {COLORS['bg_dark']};")
        main_container_layout = QVBoxLayout(self.main_container)
        main_container_layout.setContentsMargins(0, 0, 0, 0)
        main_container_layout.setSpacing(0)
        
        self.pages = QStackedWidget()
        self.log_panel = LogPanel()
        
        self.profiles_page = ProfilesPage(self.log)
        self.pages.addWidget(self.profiles_page)
        
        for tab_id in ["login", "pages", "reels", "content", "groups", "scripts", "posts"]:
            page = self._create_placeholder_page(tab_id)
            self.pages.addWidget(page)
        
        main_container_layout.addWidget(self.pages)
        
        content_layout.addWidget(self.main_container, 1)
        content_layout.addWidget(self.log_panel)
        
        main_layout.addWidget(content, 1)
        
        self.status_bar = StatusBar()
        main_layout.addWidget(self.status_bar)
        
        self._setup_effects()
        
        for tab_id, nav_item in self.sidebar.nav_items.items():
            nav_item.clicked_nav.connect(self._switch_tab)
        
        self._switch_tab("profiles")
        
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
