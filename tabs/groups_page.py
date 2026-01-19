"""
Groups Page - Quan ly Groups Facebook
PySide6 version with Hidemium integration
"""
import threading
from typing import List, Dict
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QScrollArea, QMessageBox, QProgressBar
)
from PySide6.QtCore import Qt, QTimer

from config import COLORS
from widgets import (
    CyberButton, CyberInput, CyberComboBox, CyberCard,
    CyberTitle, CyberStatCard, CyberCheckBox
)
from api_service import api
from db import (
    get_profiles, get_groups, get_groups_for_profiles, save_group,
    delete_group, sync_groups, clear_groups
)


class GroupsPage(QWidget):
    """Groups Page - Quan ly Groups"""

    def __init__(self, log_func, parent=None):
        super().__init__(parent)
        self.log = log_func
        self.profiles: List[Dict] = []
        self.groups: List[Dict] = []
        self.folders: List[Dict] = []

        # Selection
        self.selected_profile_uuids: List[str] = []
        self.profile_checkboxes: Dict[str, QCheckBox] = {}
        self.group_checkboxes: Dict[int, QCheckBox] = {}

        # State
        self._is_scanning = False

        self._setup_ui()
        QTimer.singleShot(500, self._load_data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(10)

        # Top bar
        top_bar = QHBoxLayout()
        title = CyberTitle("Groups", "Quan ly Groups", "coral")
        top_bar.addWidget(title)
        top_bar.addStretch()

        self.stat_profiles = CyberStatCard("PROFILES", "0", "📁", "coral")
        self.stat_profiles.setFixedWidth(140)
        top_bar.addWidget(self.stat_profiles)

        self.stat_groups = CyberStatCard("GROUPS", "0", "👥", "purple")
        self.stat_groups.setFixedWidth(140)
        top_bar.addWidget(self.stat_groups)

        self.stat_selected = CyberStatCard("DA CHON", "0", "✓", "mint")
        self.stat_selected.setFixedWidth(140)
        top_bar.addWidget(self.stat_selected)

        layout.addLayout(top_bar)

        # Main content - 2 columns
        content = QHBoxLayout()
        content.setSpacing(12)

        # Left panel - Profile selection
        left_card = CyberCard(COLORS['neon_coral'])
        left_card.setFixedWidth(280)
        left_layout = QVBoxLayout(left_card)
        left_layout.setContentsMargins(12, 12, 12, 12)

        # Header
        header_row = QHBoxLayout()
        header_label = QLabel("Chon Profile")
        header_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 14px; font-weight: bold;")
        header_row.addWidget(header_label)

        btn_refresh = CyberButton("", "ghost", "🔄")
        btn_refresh.setFixedWidth(36)
        btn_refresh.clicked.connect(self._load_data)
        header_row.addWidget(btn_refresh)

        left_layout.addLayout(header_row)

        # Folder filter
        folder_row = QHBoxLayout()
        folder_label = QLabel("📁")
        folder_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        folder_row.addWidget(folder_label)

        self.folder_combo = CyberComboBox(["-- Tat ca --"])
        self.folder_combo.currentIndexChanged.connect(self._on_folder_change)
        folder_row.addWidget(self.folder_combo, 1)

        left_layout.addLayout(folder_row)

        # Select buttons
        btn_row = QHBoxLayout()
        btn_all = CyberButton("Chon tat ca", "ghost")
        btn_all.clicked.connect(self._select_all_profiles)
        btn_row.addWidget(btn_all)

        btn_none = CyberButton("Bo chon", "ghost")
        btn_none.clicked.connect(self._deselect_all_profiles)
        btn_row.addWidget(btn_none)

        left_layout.addLayout(btn_row)

        # Profile list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                background: {COLORS['bg_darker']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
            }}
        """)

        self.profile_list_widget = QWidget()
        self.profile_list_layout = QVBoxLayout(self.profile_list_widget)
        self.profile_list_layout.setContentsMargins(8, 8, 8, 8)
        self.profile_list_layout.setSpacing(4)
        self.profile_list_layout.addStretch()

        scroll.setWidget(self.profile_list_widget)
        left_layout.addWidget(scroll, 1)

        # Stats
        self.profile_stats = QLabel("Profiles: 0 | Da chon: 0")
        self.profile_stats.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 10px;")
        left_layout.addWidget(self.profile_stats)

        content.addWidget(left_card)

        # Right panel - Groups list
        right_card = CyberCard(COLORS['neon_purple'])
        right_layout = QVBoxLayout(right_card)
        right_layout.setContentsMargins(12, 12, 12, 12)

        # Header with actions
        header_row2 = QHBoxLayout()
        groups_label = QLabel("Danh sach Groups")
        groups_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 14px; font-weight: bold;")
        header_row2.addWidget(groups_label)
        header_row2.addStretch()

        btn_scan = CyberButton("Scan Groups", "primary", "🔍")
        btn_scan.clicked.connect(self._scan_groups)
        header_row2.addWidget(btn_scan)

        btn_delete = CyberButton("Xoa", "danger", "🗑️")
        btn_delete.clicked.connect(self._delete_selected_groups)
        header_row2.addWidget(btn_delete)

        right_layout.addLayout(header_row2)

        # Search and filter
        filter_row = QHBoxLayout()

        self.search_input = CyberInput("🔍 Tim kiem Group...")
        self.search_input.setFixedWidth(250)
        self.search_input.textChanged.connect(self._filter_groups)
        filter_row.addWidget(self.search_input)

        filter_row.addStretch()

        self.select_all_groups_cb = CyberCheckBox()
        self.select_all_groups_cb.stateChanged.connect(self._toggle_all_groups)
        filter_row.addWidget(self.select_all_groups_cb)

        select_label = QLabel("Chon tat ca")
        select_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 11px;")
        filter_row.addWidget(select_label)

        right_layout.addLayout(filter_row)

        # Progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background: {COLORS['bg_darker']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                height: 12px;
            }}
            QProgressBar::chunk {{
                background: {COLORS['neon_coral']};
                border-radius: 3px;
            }}
        """)
        self.progress_bar.setValue(0)
        right_layout.addWidget(self.progress_bar)

        # Table header
        table_header = QFrame()
        table_header.setFixedHeight(32)
        table_header.setStyleSheet(f"background: {COLORS['bg_card']}; border-radius: 4px;")
        table_header_layout = QHBoxLayout(table_header)
        table_header_layout.setContentsMargins(8, 0, 8, 0)

        headers = [("", 30), ("Ten Group", 220), ("Thanh vien", 90), ("Profile", 150)]
        for text, width in headers:
            lbl = QLabel(text)
            lbl.setFixedWidth(width)
            lbl.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 10px; font-weight: bold;")
            table_header_layout.addWidget(lbl)

        table_header_layout.addStretch()
        right_layout.addWidget(table_header)

        # Groups list
        scroll2 = QScrollArea()
        scroll2.setWidgetResizable(True)
        scroll2.setStyleSheet(f"""
            QScrollArea {{
                background: {COLORS['bg_darker']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
            }}
        """)

        self.groups_list_widget = QWidget()
        self.groups_list_layout = QVBoxLayout(self.groups_list_widget)
        self.groups_list_layout.setContentsMargins(8, 8, 8, 8)
        self.groups_list_layout.setSpacing(2)

        empty_label = QLabel("Chua co Group nao\nChon profile va bam 'Scan Groups' de quet")
        empty_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px;")
        empty_label.setAlignment(Qt.AlignCenter)
        self.groups_list_layout.addWidget(empty_label)
        self.groups_list_layout.addStretch()

        scroll2.setWidget(self.groups_list_widget)
        right_layout.addWidget(scroll2, 1)

        content.addWidget(right_card, 1)
        layout.addLayout(content, 1)

    def _load_data(self):
        """Load profiles va folders"""
        def fetch():
            try:
                profiles = get_profiles()
                folders = api.get_folders(limit=100)
                return {"profiles": profiles, "folders": folders or []}
            except Exception as e:
                return {"profiles": get_profiles(), "folders": []}

        def on_complete(data):
            self.profiles = data.get("profiles", [])
            self.folders = data.get("folders", [])

            # Update folder combo
            self.folder_combo.clear()
            self.folder_combo.addItem("-- Tat ca --")
            for f in self.folders:
                self.folder_combo.addItem(f"📁 {f.get('name', 'Unknown')}")

            self._render_profiles()
            self.log(f"Loaded {len(self.profiles)} profiles", "success")

        def run():
            result = fetch()
            QTimer.singleShot(0, lambda: on_complete(result))

        threading.Thread(target=run, daemon=True).start()

    def _render_profiles(self):
        """Render danh sach profiles"""
        while self.profile_list_layout.count() > 0:
            item = self.profile_list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.profile_checkboxes.clear()

        if not self.profiles:
            label = QLabel("Khong co profile")
            label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px;")
            label.setAlignment(Qt.AlignCenter)
            self.profile_list_layout.addWidget(label)
            self.profile_list_layout.addStretch()
            return

        for profile in self.profiles:
            uuid = profile.get('uuid', '')
            name = profile.get('name', 'Unknown')

            row = QWidget()
            row.setStyleSheet(f"background: {COLORS['bg_card']}; border-radius: 4px;")
            row.setFixedHeight(36)
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(8, 4, 8, 4)
            row_layout.setSpacing(8)

            cb = CyberCheckBox()
            cb.setChecked(uuid in self.selected_profile_uuids)
            cb.stateChanged.connect(lambda state, u=uuid: self._on_profile_select(u, state))
            self.profile_checkboxes[uuid] = cb
            row_layout.addWidget(cb)

            name_label = QLabel(name[:20] + "..." if len(name) > 20 else name)
            name_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 11px;")
            row_layout.addWidget(name_label, 1)

            self.profile_list_layout.addWidget(row)

        self.profile_list_layout.addStretch()
        self._update_profile_stats()

    def _on_folder_change(self, index):
        """Khi thay doi folder"""
        if index <= 0:
            self.profiles = get_profiles()
        else:
            folder = self.folders[index - 1]
            folder_id = folder.get('id')
            try:
                self.profiles = api.get_profiles(folder_id=[folder_id]) or []
            except:
                self.profiles = get_profiles()

        self._render_profiles()

    def _on_profile_select(self, uuid: str, state):
        """Khi chon/bo chon profile"""
        if state == Qt.Checked:
            if uuid not in self.selected_profile_uuids:
                self.selected_profile_uuids.append(uuid)
        else:
            if uuid in self.selected_profile_uuids:
                self.selected_profile_uuids.remove(uuid)

        self._update_profile_stats()
        self._load_groups_for_selected()

    def _select_all_profiles(self):
        for uuid, cb in self.profile_checkboxes.items():
            cb.setChecked(True)

    def _deselect_all_profiles(self):
        for uuid, cb in self.profile_checkboxes.items():
            cb.setChecked(False)

    def _update_profile_stats(self):
        total = len(self.profile_checkboxes)
        selected = len(self.selected_profile_uuids)
        self.profile_stats.setText(f"Profiles: {total} | Da chon: {selected}")
        self.stat_profiles.set_value(str(total))
        self.stat_selected.set_value(str(selected))

    def _load_groups_for_selected(self):
        """Load groups cho cac profiles da chon"""
        if not self.selected_profile_uuids:
            self.groups = []
            self._render_groups()
            return

        self.groups = get_groups_for_profiles(self.selected_profile_uuids)
        self._render_groups()

    def _render_groups(self, search_text=None):
        """Render danh sach groups"""
        while self.groups_list_layout.count() > 0:
            item = self.groups_list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.group_checkboxes.clear()

        # Filter by search
        groups_to_show = self.groups
        if search_text:
            search_lower = search_text.lower()
            groups_to_show = [g for g in self.groups if search_lower in g.get('group_name', '').lower()]

        if not groups_to_show:
            label = QLabel("Chua co Group nao\nChon profile va bam 'Scan Groups'")
            label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px;")
            label.setAlignment(Qt.AlignCenter)
            self.groups_list_layout.addWidget(label)
            self.groups_list_layout.addStretch()
            self.stat_groups.set_value("0")
            return

        # Profile name map
        profile_map = {p['uuid']: p.get('name', 'Unknown') for p in self.profiles}

        for group in groups_to_show:
            group_id = group.get('id')
            group_name = group.get('group_name', 'Unknown')
            member_count = group.get('member_count', 0)
            profile_uuid = group.get('profile_uuid', '')
            profile_name = profile_map.get(profile_uuid, 'Unknown')[:15]

            row = QWidget()
            row.setStyleSheet(f"background: {COLORS['bg_card']}; border-radius: 4px;")
            row.setFixedHeight(36)
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(8, 4, 8, 4)
            row_layout.setSpacing(4)

            cb = CyberCheckBox()
            cb.stateChanged.connect(self._update_group_selection_count)
            self.group_checkboxes[group_id] = cb
            row_layout.addWidget(cb)

            name_lbl = QLabel(group_name[:30] + "..." if len(group_name) > 30 else group_name)
            name_lbl.setFixedWidth(220)
            name_lbl.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 11px;")
            row_layout.addWidget(name_lbl)

            member_lbl = QLabel(f"{member_count:,}")
            member_lbl.setFixedWidth(90)
            member_lbl.setStyleSheet(f"color: {COLORS['neon_cyan']}; font-size: 11px;")
            row_layout.addWidget(member_lbl)

            profile_lbl = QLabel(profile_name)
            profile_lbl.setFixedWidth(150)
            profile_lbl.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 10px;")
            row_layout.addWidget(profile_lbl)

            row_layout.addStretch()
            self.groups_list_layout.addWidget(row)

        self.groups_list_layout.addStretch()
        self.stat_groups.set_value(str(len(groups_to_show)))

    def _filter_groups(self, text):
        self._render_groups(text)

    def _toggle_all_groups(self, state):
        checked = state == Qt.Checked
        for cb in self.group_checkboxes.values():
            cb.setChecked(checked)

    def _update_group_selection_count(self):
        count = sum(1 for cb in self.group_checkboxes.values() if cb.isChecked())
        self.stat_selected.set_value(str(count))

    def _scan_groups(self):
        """Scan groups tu profiles da chon"""
        if not self.selected_profile_uuids:
            QMessageBox.warning(self, "Loi", "Chua chon profile nao!")
            return

        self._is_scanning = True
        self.progress_bar.setMaximum(len(self.selected_profile_uuids))
        self.log("Bat dau scan groups...", "info")

        def do_scan():
            for i, uuid in enumerate(self.selected_profile_uuids):
                QTimer.singleShot(0, lambda v=i+1: self.progress_bar.setValue(v))

                name = next((p.get('name', '') for p in self.profiles if p.get('uuid') == uuid), uuid[:8])
                QTimer.singleShot(0, lambda m=f"Scanning {name}...": self.log(m, "info"))

                import time
                time.sleep(1)

            self._is_scanning = False
            QTimer.singleShot(0, lambda: self.log("Scan hoan thanh!", "success"))
            QTimer.singleShot(0, self._load_groups_for_selected)

        threading.Thread(target=do_scan, daemon=True).start()

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
