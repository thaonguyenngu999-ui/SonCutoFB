"""
Groups Page - Quan ly Groups Facebook
PySide6 version - BEAUTIFUL UI like ProfilesPage
"""
import threading
from typing import List, Dict
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QMessageBox, QProgressBar, QTableWidgetItem, QSpinBox
)
from PySide6.QtCore import Qt, QTimer

from config import COLORS
from widgets import (
    CyberButton, CyberInput, CyberComboBox, CyberCard,
    CyberTitle, CyberStatCard, CyberTable, CyberCheckBox
)
from api_service import api
from db import (
    get_profiles, get_groups, get_groups_for_profiles, save_group,
    delete_group, sync_groups, clear_groups
)


class GroupsPage(QWidget):
    """Groups Page - Quan ly Groups - BEAUTIFUL UI"""

    def __init__(self, log_func, parent=None):
        super().__init__(parent)
        self.log = log_func
        self.profiles: List[Dict] = []
        self.groups: List[Dict] = []
        self.folders: List[Dict] = []

        # Selection
        self.selected_profile_uuids: List[str] = []
        self.profile_checkboxes: Dict[str, CyberCheckBox] = {}
        self.group_checkboxes: Dict[int, CyberCheckBox] = {}

        # State
        self._is_scanning = False
        self._stop_requested = False

        self._setup_ui()
        QTimer.singleShot(500, self._load_data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(10)

        # ========== TOP BAR ==========
        top_bar = QHBoxLayout()
        top_bar.setSpacing(12)

        title = CyberTitle("Groups", "Quan ly Groups Facebook", "coral")
        top_bar.addWidget(title)

        top_bar.addStretch()

        self.stat_profiles = CyberStatCard("PROFILES", "0", "📁", "coral")
        self.stat_profiles.setFixedWidth(160)
        top_bar.addWidget(self.stat_profiles)

        self.stat_groups = CyberStatCard("GROUPS", "0", "👥", "purple")
        self.stat_groups.setFixedWidth(160)
        top_bar.addWidget(self.stat_groups)

        self.stat_selected = CyberStatCard("DA CHON", "0", "✓", "mint")
        self.stat_selected.setFixedWidth(160)
        top_bar.addWidget(self.stat_selected)

        layout.addLayout(top_bar)

        # ========== TOOLBAR ==========
        toolbar = QHBoxLayout()
        toolbar.setSpacing(8)

        # Folder selection
        self.folder_combo = CyberComboBox(["📁 Tat ca folder"])
        self.folder_combo.setFixedWidth(180)
        self.folder_combo.currentIndexChanged.connect(self._on_folder_change)
        toolbar.addWidget(self.folder_combo)

        btn_load = CyberButton("TAI", "cyan", "📥")
        btn_load.clicked.connect(self._load_profiles_from_folder)
        toolbar.addWidget(btn_load)

        toolbar.addStretch()

        # Search
        self.search_input = CyberInput("🔍 Tim kiem Group...")
        self.search_input.setFixedWidth(220)
        self.search_input.textChanged.connect(self._filter_groups)
        toolbar.addWidget(self.search_input)

        toolbar.addStretch()

        # Threads
        threads_label = QLabel("So luong:")
        threads_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        toolbar.addWidget(threads_label)

        self.threads_spin = QSpinBox()
        self.threads_spin.setRange(1, 10)
        self.threads_spin.setValue(3)
        self.threads_spin.setFixedWidth(60)
        self.threads_spin.setStyleSheet(f"""
            QSpinBox {{
                background: {COLORS['bg_card']};
                color: {COLORS['text_primary']};
                border: 2px solid {COLORS['border']};
                border-radius: 8px;
                padding: 4px 8px;
                font-size: 12px;
            }}
            QSpinBox:focus {{
                border-color: {COLORS['neon_cyan']};
            }}
        """)
        toolbar.addWidget(self.threads_spin)

        btn_refresh = CyberButton("⟳", "ghost")
        btn_refresh.setFixedWidth(40)
        btn_refresh.clicked.connect(self._load_data)
        toolbar.addWidget(btn_refresh)

        layout.addLayout(toolbar)

        # ========== MAIN CONTENT ==========
        content = QHBoxLayout()
        content.setSpacing(12)

        # LEFT - Profiles Table
        profiles_card = CyberCard(COLORS['neon_coral'])
        profiles_card.setFixedWidth(340)
        profiles_layout = QVBoxLayout(profiles_card)
        profiles_layout.setContentsMargins(2, 2, 2, 2)

        # Header
        header = QWidget()
        header.setFixedHeight(44)
        header.setStyleSheet(f"background: {COLORS['bg_darker']}; border-radius: 14px 14px 0 0;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 0, 16, 0)
        header_layout.setSpacing(12)

        # Select All Profiles
        select_widget = QWidget()
        select_layout = QHBoxLayout(select_widget)
        select_layout.setContentsMargins(0, 0, 0, 0)
        select_layout.setSpacing(8)

        self.select_all_profiles_cb = CyberCheckBox()
        self.select_all_profiles_cb.stateChanged.connect(self._toggle_select_all_profiles)
        select_layout.addWidget(self.select_all_profiles_cb)

        select_label = QLabel("Chon tat ca")
        select_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        select_label.setCursor(Qt.PointingHandCursor)
        select_label.mousePressEvent = lambda e: self.select_all_profiles_cb.setChecked(
            not self.select_all_profiles_cb.isChecked())
        select_layout.addWidget(select_label)

        header_layout.addWidget(select_widget)

        sep = QFrame()
        sep.setFixedWidth(2)
        sep.setFixedHeight(24)
        sep.setStyleSheet(f"background: {COLORS['border']};")
        header_layout.addWidget(sep)

        header_title = QLabel("📁 PROFILES")
        header_title.setStyleSheet(
            f"color: {COLORS['neon_coral']}; font-size: 12px; font-weight: bold; letter-spacing: 2px;")
        header_layout.addWidget(header_title)

        self.profiles_count_label = QLabel("[0]")
        self.profiles_count_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px;")
        header_layout.addWidget(self.profiles_count_label)

        header_layout.addStretch()

        profiles_layout.addWidget(header)

        # Profiles Table
        self.profiles_table = CyberTable(["✓", "NAME", "STATUS"])
        self.profiles_table.setColumnWidth(0, 50)
        self.profiles_table.setColumnWidth(1, 180)
        self.profiles_table.setColumnWidth(2, 80)

        profiles_layout.addWidget(self.profiles_table)

        # Profile stats
        profile_stats_row = QHBoxLayout()
        profile_stats_row.setContentsMargins(12, 8, 12, 8)

        self.profile_selected_label = QLabel("")
        self.profile_selected_label.setStyleSheet(f"color: {COLORS['neon_cyan']}; font-size: 11px;")
        profile_stats_row.addWidget(self.profile_selected_label)

        profile_stats_row.addStretch()

        profiles_layout.addLayout(profile_stats_row)
        content.addWidget(profiles_card)

        # RIGHT - Groups Table
        groups_card = CyberCard(COLORS['neon_purple'])
        groups_layout = QVBoxLayout(groups_card)
        groups_layout.setContentsMargins(2, 2, 2, 2)

        # Header
        header2 = QWidget()
        header2.setFixedHeight(44)
        header2.setStyleSheet(f"background: {COLORS['bg_darker']}; border-radius: 14px 14px 0 0;")
        header2_layout = QHBoxLayout(header2)
        header2_layout.setContentsMargins(16, 0, 16, 0)
        header2_layout.setSpacing(12)

        # Select All Groups
        select_widget2 = QWidget()
        select_layout2 = QHBoxLayout(select_widget2)
        select_layout2.setContentsMargins(0, 0, 0, 0)
        select_layout2.setSpacing(8)

        self.select_all_groups_cb = CyberCheckBox()
        self.select_all_groups_cb.stateChanged.connect(self._toggle_select_all_groups)
        select_layout2.addWidget(self.select_all_groups_cb)

        select_label2 = QLabel("Chon tat ca")
        select_label2.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        select_label2.setCursor(Qt.PointingHandCursor)
        select_label2.mousePressEvent = lambda e: self.select_all_groups_cb.setChecked(
            not self.select_all_groups_cb.isChecked())
        select_layout2.addWidget(select_label2)

        header2_layout.addWidget(select_widget2)

        sep2 = QFrame()
        sep2.setFixedWidth(2)
        sep2.setFixedHeight(24)
        sep2.setStyleSheet(f"background: {COLORS['border']};")
        header2_layout.addWidget(sep2)

        header2_title = QLabel("👥 GROUPS")
        header2_title.setStyleSheet(
            f"color: {COLORS['neon_purple']}; font-size: 12px; font-weight: bold; letter-spacing: 2px;")
        header2_layout.addWidget(header2_title)

        self.groups_count_label = QLabel("[0]")
        self.groups_count_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px;")
        header2_layout.addWidget(self.groups_count_label)

        header2_layout.addStretch()

        self.groups_selected_label = QLabel("")
        self.groups_selected_label.setStyleSheet(f"color: {COLORS['neon_cyan']}; font-size: 11px;")
        header2_layout.addWidget(self.groups_selected_label)

        groups_layout.addWidget(header2)

        # Groups Table
        self.groups_table = CyberTable(["✓", "TEN GROUP", "THANH VIEN", "PROFILE"])
        self.groups_table.setColumnWidth(0, 50)
        self.groups_table.setColumnWidth(1, 280)
        self.groups_table.setColumnWidth(2, 100)
        self.groups_table.setColumnWidth(3, 150)

        groups_layout.addWidget(self.groups_table)

        # Progress bar
        progress_row = QHBoxLayout()
        progress_row.setContentsMargins(12, 4, 12, 4)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(16)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background: {COLORS['bg_darker']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, x2:1, stop:0 {COLORS['neon_coral']}, stop:1 {COLORS['neon_purple']});
                border-radius: 7px;
            }}
        """)
        self.progress_bar.setValue(0)
        progress_row.addWidget(self.progress_bar)

        groups_layout.addLayout(progress_row)

        # Action buttons
        actions_row = QHBoxLayout()
        actions_row.setContentsMargins(12, 8, 12, 12)
        actions_row.setSpacing(8)

        btn_scan = CyberButton("SCAN GROUPS", "success", "🔍")
        btn_scan.clicked.connect(self._scan_groups)
        actions_row.addWidget(btn_scan)

        btn_stop = CyberButton("DUNG", "warning", "⏹️")
        btn_stop.clicked.connect(self._stop_scan)
        actions_row.addWidget(btn_stop)

        actions_row.addStretch()

        btn_delete = CyberButton("XOA", "danger", "🗑️")
        btn_delete.clicked.connect(self._delete_selected_groups)
        actions_row.addWidget(btn_delete)

        btn_clear = CyberButton("XOA HET", "danger", "💥")
        btn_clear.clicked.connect(self._clear_all_groups)
        actions_row.addWidget(btn_clear)

        groups_layout.addLayout(actions_row)

        # Progress label
        self.progress_label = QLabel("")
        self.progress_label.setStyleSheet(f"color: {COLORS['neon_mint']}; font-size: 11px;")
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.progress_label.setContentsMargins(12, 0, 12, 8)
        groups_layout.addWidget(self.progress_label)

        content.addWidget(groups_card, 1)
        layout.addLayout(content, 1)

    def _load_data(self):
        """Load profiles va folders tu Hidemium"""
        self.log("Loading data...", "info")

        def fetch():
            try:
                folders = api.get_folders(limit=100)
                profiles = api.get_profiles(limit=500)
                return {"folders": folders or [], "profiles": profiles or []}
            except Exception as e:
                return {"folders": [], "profiles": get_profiles(), "error": str(e)}

        def on_complete(data):
            if data.get("error"):
                self.log(f"API Error: {data['error']}", "warning")

            self.folders = data.get("folders", [])
            self.profiles = data.get("profiles", [])

            # Update folder combo
            self.folder_combo.clear()
            self.folder_combo.addItem("📁 Tat ca folder")
            for f in self.folders:
                self.folder_combo.addItem(f"📁 {f.get('name', 'Unknown')}")

            self._update_profiles_table()
            self._update_stats()
            self.log(f"Loaded {len(self.profiles)} profiles, {len(self.folders)} folders", "success")

        def run():
            result = fetch()
            QTimer.singleShot(0, lambda: on_complete(result))

        threading.Thread(target=run, daemon=True).start()

    def _on_folder_change(self, index):
        """Khi thay doi folder"""
        if index > 0:
            self._load_profiles_from_folder()

    def _load_profiles_from_folder(self):
        """Load profiles tu folder da chon"""
        folder_idx = self.folder_combo.currentIndex()

        if folder_idx <= 0:
            # Load all
            self.log("Loading all profiles...", "info")

            def fetch():
                try:
                    return api.get_profiles(limit=500) or []
                except:
                    return get_profiles()

            def on_complete(profiles):
                self.profiles = profiles
                self._update_profiles_table()
                self._update_stats()
                self.log(f"Loaded {len(self.profiles)} profiles", "success")

            def run():
                result = fetch()
                QTimer.singleShot(0, lambda: on_complete(result))

            threading.Thread(target=run, daemon=True).start()
            return

        folder = self.folders[folder_idx - 1]
        folder_id = folder.get('id')
        folder_name = folder.get('name', 'Unknown')

        self.log(f"Loading profiles from {folder_name}...", "info")

        def fetch():
            try:
                return api.get_profiles(folder_id=[folder_id], limit=500) or []
            except:
                return []

        def on_complete(profiles):
            self.profiles = profiles
            self._update_profiles_table()
            self._update_stats()
            self.log(f"Loaded {len(self.profiles)} profiles from {folder_name}", "success")

        def run():
            result = fetch()
            QTimer.singleShot(0, lambda: on_complete(result))

        threading.Thread(target=run, daemon=True).start()

    def _update_profiles_table(self):
        """Update profiles table"""
        self.profiles_table.setRowCount(len(self.profiles))
        self.profile_checkboxes.clear()

        for row, profile in enumerate(self.profiles):
            uuid = profile.get('uuid', '')
            name = profile.get('name', 'Unknown')
            status = profile.get('status', 'stopped')

            # Checkbox
            cb_widget = QWidget()
            cb_widget.setStyleSheet("background: transparent;")
            cb_layout = QHBoxLayout(cb_widget)
            cb_layout.setContentsMargins(0, 0, 0, 0)
            cb_layout.setAlignment(Qt.AlignCenter)
            checkbox = CyberCheckBox()
            checkbox.setChecked(uuid in self.selected_profile_uuids)
            checkbox.stateChanged.connect(lambda state, u=uuid: self._on_profile_select(u, state))
            cb_layout.addWidget(checkbox)
            self.profiles_table.setCellWidget(row, 0, cb_widget)
            self.profile_checkboxes[uuid] = checkbox

            # Name
            name_display = name[:25] + "..." if len(name) > 25 else name
            self.profiles_table.setItem(row, 1, QTableWidgetItem(name_display))

            # Status
            status_text = "🟢 ON" if status == "running" else "⚫ OFF"
            self.profiles_table.setItem(row, 2, QTableWidgetItem(status_text))

        self.profiles_count_label.setText(f"[{len(self.profiles)} profiles]")

    def _on_profile_select(self, uuid: str, state):
        """Khi chon/bo chon profile"""
        if state == Qt.Checked:
            if uuid not in self.selected_profile_uuids:
                self.selected_profile_uuids.append(uuid)
        else:
            if uuid in self.selected_profile_uuids:
                self.selected_profile_uuids.remove(uuid)

        self._update_profile_selection_label()
        self._load_groups_for_selected()

    def _toggle_select_all_profiles(self, state):
        """Toggle chon tat ca profiles"""
        checked = state == Qt.Checked
        for uuid, cb in self.profile_checkboxes.items():
            cb.blockSignals(True)
            cb.setChecked(checked)
            cb.blockSignals(False)

            if checked:
                if uuid not in self.selected_profile_uuids:
                    self.selected_profile_uuids.append(uuid)
            else:
                if uuid in self.selected_profile_uuids:
                    self.selected_profile_uuids.remove(uuid)

        self._update_profile_selection_label()
        self._load_groups_for_selected()

    def _update_profile_selection_label(self):
        """Update label so profile da chon"""
        count = len(self.selected_profile_uuids)
        self.profile_selected_label.setText(f"✓ {count} da chon" if count > 0 else "")
        self.stat_selected.set_value(str(count))

    def _load_groups_for_selected(self):
        """Load groups cho cac profiles da chon"""
        if not self.selected_profile_uuids:
            self.groups = []
            self._update_groups_table()
            return

        self.groups = get_groups_for_profiles(self.selected_profile_uuids)
        self._update_groups_table()

    def _update_groups_table(self, search_text=None):
        """Update groups table"""
        # Filter by search
        groups_to_show = self.groups
        if search_text:
            search_lower = search_text.lower()
            groups_to_show = [g for g in self.groups if search_lower in g.get('group_name', '').lower()]

        self.groups_table.setRowCount(len(groups_to_show))
        self.group_checkboxes.clear()

        # Profile name map
        profile_map = {p.get('uuid'): p.get('name', 'Unknown') for p in self.profiles}

        for row, group in enumerate(groups_to_show):
            group_id = group.get('id')
            group_name = group.get('group_name', 'Unknown')
            member_count = group.get('member_count', 0)
            profile_uuid = group.get('profile_uuid', '')
            profile_name = profile_map.get(profile_uuid, 'Unknown')

            # Checkbox
            cb_widget = QWidget()
            cb_widget.setStyleSheet("background: transparent;")
            cb_layout = QHBoxLayout(cb_widget)
            cb_layout.setContentsMargins(0, 0, 0, 0)
            cb_layout.setAlignment(Qt.AlignCenter)
            checkbox = CyberCheckBox()
            checkbox.stateChanged.connect(self._update_groups_selection_count)
            cb_layout.addWidget(checkbox)
            self.groups_table.setCellWidget(row, 0, cb_widget)
            self.group_checkboxes[group_id] = checkbox

            # Group name
            name_display = group_name[:35] + "..." if len(group_name) > 35 else group_name
            self.groups_table.setItem(row, 1, QTableWidgetItem(name_display))

            # Member count
            member_item = QTableWidgetItem(f"{member_count:,}")
            member_item.setForeground(Qt.cyan)
            self.groups_table.setItem(row, 2, member_item)

            # Profile name
            profile_display = profile_name[:18] + "..." if len(profile_name) > 18 else profile_name
            self.groups_table.setItem(row, 3, QTableWidgetItem(profile_display))

        self.groups_count_label.setText(f"[{len(groups_to_show)} groups]")
        self.stat_groups.set_value(str(len(groups_to_show)))

    def _toggle_select_all_groups(self, state):
        """Toggle chon tat ca groups"""
        checked = state == Qt.Checked
        for gid, cb in self.group_checkboxes.items():
            cb.blockSignals(True)
            cb.setChecked(checked)
            cb.blockSignals(False)

        self._update_groups_selection_count()

    def _update_groups_selection_count(self):
        """Update so groups da chon"""
        count = sum(1 for cb in self.group_checkboxes.values() if cb.isChecked())
        self.groups_selected_label.setText(f"✓ {count} da chon" if count > 0 else "")

    def _filter_groups(self, text):
        """Filter groups theo search text"""
        self._update_groups_table(text)

    def _update_stats(self):
        """Update all stats"""
        self.stat_profiles.set_value(str(len(self.profiles)))
        self.stat_groups.set_value(str(len(self.groups)))
        self.stat_selected.set_value(str(len(self.selected_profile_uuids)))

    def _scan_groups(self):
        """Scan groups tu profiles da chon"""
        if not self.selected_profile_uuids:
            QMessageBox.warning(self, "Loi", "Chua chon profile nao!")
            return

        if self._is_scanning:
            QMessageBox.warning(self, "Loi", "Dang scan, vui long doi!")
            return

        self._is_scanning = True
        self._stop_requested = False
        total = len(self.selected_profile_uuids)
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(0)
        self.log(f"Bat dau scan groups cho {total} profiles...", "info")

        def do_scan():
            import time

            for i, uuid in enumerate(self.selected_profile_uuids):
                if self._stop_requested:
                    QTimer.singleShot(0, lambda: self.log("Scan da dung!", "warning"))
                    break

                QTimer.singleShot(0, lambda v=i + 1: self.progress_bar.setValue(v))

                name = next((p.get('name', '') for p in self.profiles if p.get('uuid') == uuid), uuid[:8])
                QTimer.singleShot(0, lambda m=f"[{i + 1}/{total}] Scanning {name}...": self.progress_label.setText(m))
                QTimer.singleShot(0, lambda m=f"Scanning {name}...": self.log(m, "info"))

                # TODO: Implement real group scanning via Hidemium script
                # For now, just simulate with delay
                time.sleep(1)

            self._is_scanning = False
            QTimer.singleShot(0, lambda: self.progress_label.setText("Scan hoan thanh!"))
            QTimer.singleShot(0, lambda: self.log("Scan groups hoan thanh!", "success"))
            QTimer.singleShot(0, self._load_groups_for_selected)

        threading.Thread(target=do_scan, daemon=True).start()

    def _stop_scan(self):
        """Dung scan"""
        if self._is_scanning:
            self._stop_requested = True
            self.log("Dang dung scan...", "info")
            self.progress_label.setText("Dang dung...")

    def _delete_selected_groups(self):
        """Xoa cac groups da chon"""
        selected_ids = [gid for gid, cb in self.group_checkboxes.items() if cb.isChecked()]

        if not selected_ids:
            QMessageBox.warning(self, "Loi", "Chua chon group nao!")
            return

        reply = QMessageBox.question(
            self, "Xac nhan",
            f"Ban co chac muon xoa {len(selected_ids)} groups?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            for gid in selected_ids:
                delete_group(gid)
            self.log(f"Da xoa {len(selected_ids)} groups", "success")
            self._load_groups_for_selected()

    def _clear_all_groups(self):
        """Xoa tat ca groups cua cac profiles da chon"""
        if not self.selected_profile_uuids:
            QMessageBox.warning(self, "Loi", "Chua chon profile nao!")
            return

        reply = QMessageBox.question(
            self, "Xac nhan",
            f"Ban co chac muon xoa TAT CA groups cua {len(self.selected_profile_uuids)} profiles?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            count = 0
            for uuid in self.selected_profile_uuids:
                if clear_groups(uuid):
                    count += 1
            self.log(f"Da xoa groups cua {count} profiles", "success")
            self._load_groups_for_selected()
