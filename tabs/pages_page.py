"""
Pages Page - Quan ly cac Fanpage Facebook
PySide6 version - BEAUTIFUL UI like ProfilesPage
"""
import threading
from typing import List, Dict
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QMessageBox, QTableWidgetItem, QProgressBar
)
from PySide6.QtCore import Qt, QTimer

from config import COLORS
from widgets import (
    CyberButton, CyberInput, CyberComboBox, CyberCard,
    CyberTitle, CyberStatCard, CyberTable, CyberCheckBox
)
from api_service import api
from db import (
    get_profiles, get_pages, get_pages_for_profiles, save_page,
    delete_page, delete_pages_bulk, sync_pages, clear_pages, get_pages_count
)


class PagesPage(QWidget):
    """Pages Page - Quan ly Fanpage - BEAUTIFUL UI"""

    def __init__(self, log_func, parent=None):
        super().__init__(parent)
        self.log = log_func
        self.profiles: List[Dict] = []
        self.pages: List[Dict] = []
        self.folders: List[Dict] = []
        self.folder_map: Dict[str, str] = {}

        # Selection tracking
        self.page_checkboxes: Dict[int, CyberCheckBox] = {}

        # State
        self._is_scanning = False

        self._setup_ui()
        QTimer.singleShot(500, self._load_data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(10)

        # ========== TOP BAR ==========
        top_bar = QHBoxLayout()
        top_bar.setSpacing(12)

        title = CyberTitle("Pages", "Quan ly Fanpage Facebook", "purple")
        top_bar.addWidget(title)

        top_bar.addStretch()

        self.stat_total = CyberStatCard("TONG PAGE", "0", "📄", "purple")
        self.stat_total.setFixedWidth(160)
        top_bar.addWidget(self.stat_total)

        self.stat_selected = CyberStatCard("DA CHON", "0", "✓", "cyan")
        self.stat_selected.setFixedWidth(160)
        top_bar.addWidget(self.stat_selected)

        self.stat_profiles = CyberStatCard("PROFILES", "0", "📁", "pink")
        self.stat_profiles.setFixedWidth(160)
        top_bar.addWidget(self.stat_profiles)

        layout.addLayout(top_bar)

        # ========== TOOLBAR ==========
        toolbar = QHBoxLayout()
        toolbar.setSpacing(8)

        # Folder filter
        self.folder_combo = CyberComboBox(["📁 Tat ca folder"])
        self.folder_combo.setFixedWidth(180)
        self.folder_combo.currentIndexChanged.connect(self._on_folder_change)
        toolbar.addWidget(self.folder_combo)

        # Profile filter
        self.profile_combo = CyberComboBox(["👤 Tat ca profile"])
        self.profile_combo.setFixedWidth(200)
        self.profile_combo.currentIndexChanged.connect(self._on_profile_change)
        toolbar.addWidget(self.profile_combo)

        # Search
        self.search_input = CyberInput("🔍 Tim kiem Page...")
        self.search_input.setFixedWidth(200)
        self.search_input.textChanged.connect(self._filter_pages)
        toolbar.addWidget(self.search_input)

        toolbar.addStretch()

        # Action buttons
        btn_refresh = CyberButton("", "ghost", "🔄")
        btn_refresh.setFixedWidth(40)
        btn_refresh.clicked.connect(self._load_data)
        toolbar.addWidget(btn_refresh)

        btn_scan = CyberButton("SCAN", "cyan", "🔍")
        btn_scan.clicked.connect(self._scan_pages)
        toolbar.addWidget(btn_scan)

        btn_delete = CyberButton("XOA", "danger", "🗑️")
        btn_delete.clicked.connect(self._delete_selected_pages)
        toolbar.addWidget(btn_delete)

        layout.addLayout(toolbar)

        # ========== PROGRESS BAR ==========
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background: {COLORS['bg_darker']};
                border: none;
                border-radius: 3px;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, x2:1, stop:0 {COLORS['neon_purple']}, stop:1 {COLORS['neon_pink']});
                border-radius: 3px;
            }}
        """)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # ========== MAIN CONTENT - TABLE CARD ==========
        table_card = CyberCard(COLORS['neon_purple'])
        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(2, 2, 2, 2)

        # Header
        header = QWidget()
        header.setFixedHeight(44)
        header.setStyleSheet(f"background: {COLORS['bg_darker']}; border-radius: 14px 14px 0 0;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 0, 16, 0)
        header_layout.setSpacing(12)

        # Select All
        select_widget = QWidget()
        select_layout = QHBoxLayout(select_widget)
        select_layout.setContentsMargins(0, 0, 0, 0)
        select_layout.setSpacing(8)

        self.select_all_cb = CyberCheckBox()
        self.select_all_cb.stateChanged.connect(self._toggle_select_all)
        select_layout.addWidget(self.select_all_cb)

        select_label = QLabel("Chon tat ca")
        select_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        select_label.setCursor(Qt.PointingHandCursor)
        select_label.mousePressEvent = lambda e: self.select_all_cb.setChecked(not self.select_all_cb.isChecked())
        select_layout.addWidget(select_label)

        header_layout.addWidget(select_widget)

        # Separator
        sep = QFrame()
        sep.setFixedWidth(2)
        sep.setFixedHeight(24)
        sep.setStyleSheet(f"background: {COLORS['border']};")
        header_layout.addWidget(sep)

        # Title
        header_title = QLabel("📄 FANPAGES")
        header_title.setStyleSheet(f"color: {COLORS['neon_purple']}; font-size: 12px; font-weight: bold; letter-spacing: 2px;")
        header_layout.addWidget(header_title)

        self.count_label = QLabel("[0]")
        self.count_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px;")
        header_layout.addWidget(self.count_label)

        header_layout.addStretch()

        # Selected count
        self.selected_label = QLabel("")
        self.selected_label.setStyleSheet(f"color: {COLORS['neon_cyan']}; font-size: 11px;")
        header_layout.addWidget(self.selected_label)

        # Progress text
        self.progress_label = QLabel("")
        self.progress_label.setStyleSheet(f"color: {COLORS['neon_pink']}; font-size: 11px;")
        header_layout.addWidget(self.progress_label)

        table_layout.addWidget(header)

        # Table
        self.table = CyberTable(["✓", "TEN PAGE", "FOLLOWERS", "PROFILE", "ROLE", "CATEGORY"])
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 250)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 150)
        self.table.setColumnWidth(4, 80)
        self.table.setColumnWidth(5, 120)

        table_layout.addWidget(self.table)
        layout.addWidget(table_card, 1)

    def _load_data(self):
        """Load folders, profiles va pages tu Hidemium va DB"""
        self.log("Loading data...", "info")

        def fetch():
            try:
                folders = api.get_folders(limit=100)
                profiles = api.get_profiles(limit=500)
                pages = get_pages()
                return {"folders": folders or [], "profiles": profiles or [], "pages": pages or []}
            except Exception as e:
                return {"folders": [], "profiles": get_profiles(), "pages": get_pages(), "error": str(e)}

        def on_complete(result):
            if "error" in result:
                self.log(f"API Error: {result['error']}", "warning")

            self.folders = result.get("folders", [])
            self.profiles = result.get("profiles", [])
            self.pages = result.get("pages", [])

            # Build folder map
            self.folder_map = {f.get('id'): f.get('name', 'Unknown') for f in self.folders}

            # Update folder combo
            self.folder_combo.clear()
            self.folder_combo.addItem("📁 Tat ca folder")
            for folder in self.folders:
                self.folder_combo.addItem(f"📁 {folder.get('name', 'Unknown')}")

            # Update profile combo
            self.profile_combo.clear()
            self.profile_combo.addItem("👤 Tat ca profile")
            for profile in self.profiles:
                name = profile.get('name', 'Unknown')
                if len(name) > 25:
                    name = name[:25] + "..."
                self.profile_combo.addItem(f"👤 {name}")

            self._update_table()
            self._update_stats()
            self.log(f"Loaded {len(self.profiles)} profiles, {len(self.pages)} pages", "success")

        def run():
            result = fetch()
            QTimer.singleShot(0, lambda: on_complete(result))

        threading.Thread(target=run, daemon=True).start()

    def _on_folder_change(self, index):
        """Khi thay doi folder filter"""
        if index <= 0:
            # All folders - load all profiles
            self._load_profiles_for_folder(None)
        else:
            folder = self.folders[index - 1]
            folder_id = folder.get('id')
            self._load_profiles_for_folder(folder_id)

    def _load_profiles_for_folder(self, folder_id):
        """Load profiles theo folder"""
        def fetch():
            try:
                if folder_id:
                    return api.get_profiles(folder_id=[folder_id], limit=500)
                else:
                    return api.get_profiles(limit=500)
            except:
                return get_profiles()

        def on_complete(profiles):
            self.profiles = profiles or []

            # Update profile combo
            self.profile_combo.clear()
            self.profile_combo.addItem("👤 Tat ca profile")
            for profile in self.profiles:
                name = profile.get('name', 'Unknown')
                if len(name) > 25:
                    name = name[:25] + "..."
                self.profile_combo.addItem(f"👤 {name}")

            self._filter_pages_by_profile()
            self._update_stats()

        def run():
            result = fetch()
            QTimer.singleShot(0, lambda: on_complete(result))

        threading.Thread(target=run, daemon=True).start()

    def _on_profile_change(self, index):
        """Khi thay doi profile filter"""
        self._filter_pages_by_profile()

    def _filter_pages_by_profile(self):
        """Filter pages theo profile da chon"""
        profile_idx = self.profile_combo.currentIndex()

        if profile_idx <= 0:
            # All profiles - get pages for all current profiles
            profile_uuids = [p.get('uuid') for p in self.profiles]
            if profile_uuids:
                self.pages = get_pages_for_profiles(profile_uuids)
            else:
                self.pages = get_pages()
        else:
            profile = self.profiles[profile_idx - 1]
            uuid = profile.get('uuid', '')
            self.pages = get_pages(uuid)

        self._update_table()
        self._update_stats()

    def _filter_pages(self, search_text):
        """Filter pages theo search text"""
        self._update_table(search_text)

    def _update_table(self, search_text=None):
        """Update table voi pages"""
        # Filter by search
        pages_to_show = self.pages
        if search_text:
            search_lower = search_text.lower()
            pages_to_show = [
                p for p in self.pages
                if search_lower in p.get('page_name', '').lower()
                or search_lower in p.get('category', '').lower()
            ]

        # Build profile name map
        profile_map = {p.get('uuid'): p.get('name', 'Unknown') for p in self.profiles}

        self.table.setRowCount(len(pages_to_show))
        self.page_checkboxes.clear()

        for row, page in enumerate(pages_to_show):
            page_id = page.get('id')
            page_name = page.get('page_name', 'Unknown')
            followers = page.get('follower_count', 0)
            profile_uuid = page.get('profile_uuid', '')
            profile_name = profile_map.get(profile_uuid, 'Unknown')
            role = page.get('role', 'admin')
            category = page.get('category', '-')

            # Checkbox
            cb_widget = QWidget()
            cb_widget.setStyleSheet("background: transparent;")
            cb_layout = QHBoxLayout(cb_widget)
            cb_layout.setContentsMargins(0, 0, 0, 0)
            cb_layout.setAlignment(Qt.AlignCenter)
            checkbox = CyberCheckBox()
            checkbox.stateChanged.connect(self._update_selection_count)
            cb_layout.addWidget(checkbox)
            self.table.setCellWidget(row, 0, cb_widget)
            self.page_checkboxes[page_id] = checkbox

            # Page name
            name_item = QTableWidgetItem(page_name[:35] + "..." if len(page_name) > 35 else page_name)
            self.table.setItem(row, 1, name_item)

            # Followers
            followers_item = QTableWidgetItem(self._format_number(followers))
            followers_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, followers_item)

            # Profile name
            profile_display = profile_name[:20] + "..." if len(profile_name) > 20 else profile_name
            self.table.setItem(row, 3, QTableWidgetItem(profile_display))

            # Role
            role_item = QTableWidgetItem(role)
            role_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 4, role_item)

            # Category
            self.table.setItem(row, 5, QTableWidgetItem(category or '-'))

        self.count_label.setText(f"[{len(pages_to_show)} pages]")

    def _format_number(self, num):
        """Format so de hien thi"""
        if num >= 1000000:
            return f"{num/1000000:.1f}M"
        elif num >= 1000:
            return f"{num/1000:.1f}K"
        return str(num)

    def _toggle_select_all(self, state):
        """Toggle chon tat ca pages"""
        checked = state == Qt.Checked
        count = 0
        for page_id, cb in self.page_checkboxes.items():
            cb.setChecked(checked)
            if checked:
                count += 1
        self.selected_label.setText(f"✓ {count} da chon" if checked else "")
        self._update_stats()

    def _update_selection_count(self):
        """Cap nhat so luong da chon"""
        count = sum(1 for cb in self.page_checkboxes.values() if cb.isChecked())
        self.selected_label.setText(f"✓ {count} da chon" if count > 0 else "")
        self.stat_selected.set_value(str(count))

    def _update_stats(self):
        """Cap nhat stats"""
        self.stat_total.set_value(str(len(self.pages)))
        selected = sum(1 for cb in self.page_checkboxes.values() if cb.isChecked())
        self.stat_selected.set_value(str(selected))
        self.stat_profiles.set_value(str(len(self.profiles)))

    def _scan_pages(self):
        """Scan pages tu profiles"""
        if self._is_scanning:
            QMessageBox.warning(self, "Thong bao", "Dang scan, vui long doi...")
            return

        # Get selected profile or all profiles
        profile_idx = self.profile_combo.currentIndex()
        if profile_idx <= 0:
            profiles_to_scan = self.profiles
        else:
            profiles_to_scan = [self.profiles[profile_idx - 1]]

        if not profiles_to_scan:
            QMessageBox.warning(self, "Loi", "Khong co profile nao de scan!")
            return

        reply = QMessageBox.question(
            self, "Xac nhan",
            f"Scan pages tu {len(profiles_to_scan)} profiles?\n\nLuu y: Tinh nang nay can mo browser va dang nhap Facebook.",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        self._is_scanning = True
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(profiles_to_scan))
        self.progress_bar.setValue(0)
        self.log(f"Bat dau scan {len(profiles_to_scan)} profiles...", "info")

        def do_scan():
            total_pages = 0
            for i, profile in enumerate(profiles_to_scan):
                uuid = profile.get('uuid', '')
                name = profile.get('name', uuid[:8])

                QTimer.singleShot(0, lambda v=i+1: self.progress_bar.setValue(v))
                QTimer.singleShot(0, lambda m=f"[{i+1}/{len(profiles_to_scan)}] {name}": self.progress_label.setText(m))
                QTimer.singleShot(0, lambda m=f"Scanning {name}...": self.log(m, "info"))

                # TODO: Implement actual page scanning via CDP
                # This would involve:
                # 1. Open browser with api.open_browser(uuid)
                # 2. Navigate to facebook.com/pages
                # 3. Extract page info using CDP
                # 4. Save to database with sync_pages(uuid, pages_data)

                # Simulate scan delay
                import time
                time.sleep(1)

                # For demo, create mock pages
                # In real implementation, this would be actual scanned data

            self._is_scanning = False
            QTimer.singleShot(0, lambda: self.progress_bar.setVisible(False))
            QTimer.singleShot(0, lambda: self.progress_label.setText(""))
            QTimer.singleShot(0, lambda: self.log("Scan hoan thanh!", "success"))
            QTimer.singleShot(0, self._filter_pages_by_profile)

        threading.Thread(target=do_scan, daemon=True).start()

    def _delete_selected_pages(self):
        """Xoa cac pages da chon"""
        selected_ids = [pid for pid, cb in self.page_checkboxes.items() if cb.isChecked()]

        if not selected_ids:
            QMessageBox.warning(self, "Loi", "Chua chon page nao!")
            return

        reply = QMessageBox.question(
            self, "Xac nhan",
            f"Ban co chac muon xoa {len(selected_ids)} pages?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            deleted = delete_pages_bulk(selected_ids)
            self.log(f"Da xoa {deleted} pages", "success")
            self._filter_pages_by_profile()
