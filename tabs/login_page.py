"""
Login Page - Dang nhap Facebook cho cac profiles
PySide6 version - BEAUTIFUL UI like ProfilesPage
"""
import threading
import os
from typing import List, Dict
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QFileDialog, QMessageBox, QTableWidgetItem, QSpinBox
)
from PySide6.QtCore import Qt, QTimer

from config import COLORS
from widgets import (
    CyberButton, CyberInput, CyberComboBox, CyberCard,
    CyberTitle, CyberStatCard, CyberTable, CyberCheckBox, ToggleButton
)
from api_service import api
from db import get_profiles, sync_profiles

# Optional openpyxl
try:
    import openpyxl
    from openpyxl import Workbook
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False


class LoginPage(QWidget):
    """Login Page - Dang nhap Facebook - BEAUTIFUL UI"""

    def __init__(self, log_func, parent=None):
        super().__init__(parent)
        self.log = log_func
        self.folders: List[Dict] = []
        self.profiles: List[Dict] = []
        self.accounts: List[Dict] = []
        self.xlsx_path = ""
        self.workbook = None

        # Profile status
        self.profile_status: Dict[str, Dict] = {}
        self.profile_checkboxes: Dict[str, CyberCheckBox] = {}

        # Running state
        self._is_running = False
        self._stop_requested = False

        self._setup_ui()
        QTimer.singleShot(500, self._load_folders)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(10)

        # ========== TOP BAR ==========
        top_bar = QHBoxLayout()
        top_bar.setSpacing(12)

        title = CyberTitle("Login FB", "Dang nhap Facebook tu dong", "mint")
        top_bar.addWidget(title)

        top_bar.addStretch()

        self.stat_profiles = CyberStatCard("PROFILES", "0", "📁", "mint")
        self.stat_profiles.setFixedWidth(160)
        top_bar.addWidget(self.stat_profiles)

        self.stat_selected = CyberStatCard("DA CHON", "0", "✓", "cyan")
        self.stat_selected.setFixedWidth(160)
        top_bar.addWidget(self.stat_selected)

        self.stat_accounts = CyberStatCard("TAI KHOAN", "0", "👤", "purple")
        self.stat_accounts.setFixedWidth(160)
        top_bar.addWidget(self.stat_accounts)

        layout.addLayout(top_bar)

        # ========== TOOLBAR ==========
        toolbar = QHBoxLayout()
        toolbar.setSpacing(8)

        # Folder selection
        self.folder_combo = CyberComboBox(["📁 Chon folder"])
        self.folder_combo.setFixedWidth(180)
        self.folder_combo.currentIndexChanged.connect(self._on_folder_change)
        toolbar.addWidget(self.folder_combo)

        btn_load = CyberButton("TAI", "cyan", "📥")
        btn_load.clicked.connect(self._load_profiles)
        toolbar.addWidget(btn_load)

        toolbar.addStretch()

        # Import XLSX
        self.xlsx_input = CyberInput("📂 Chon file XLSX...")
        self.xlsx_input.setFixedWidth(200)
        self.xlsx_input.setReadOnly(True)
        toolbar.addWidget(self.xlsx_input)

        btn_browse = CyberButton("CHON FILE", "purple", "📂")
        btn_browse.clicked.connect(self._browse_xlsx)
        toolbar.addWidget(btn_browse)

        toolbar.addStretch()

        btn_refresh = CyberButton("⟳", "ghost")
        btn_refresh.setFixedWidth(40)
        btn_refresh.clicked.connect(self._load_folders)
        toolbar.addWidget(btn_refresh)

        layout.addLayout(toolbar)

        # ========== MAIN CONTENT ==========
        content = QHBoxLayout()
        content.setSpacing(12)

        # LEFT - Profiles Table
        profiles_card = CyberCard(COLORS['neon_mint'])
        profiles_layout = QVBoxLayout(profiles_card)
        profiles_layout.setContentsMargins(2, 2, 2, 2)

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

        sep = QFrame()
        sep.setFixedWidth(2)
        sep.setFixedHeight(24)
        sep.setStyleSheet(f"background: {COLORS['border']};")
        header_layout.addWidget(sep)

        header_title = QLabel("📁 PROFILES")
        header_title.setStyleSheet(f"color: {COLORS['neon_mint']}; font-size: 12px; font-weight: bold; letter-spacing: 2px;")
        header_layout.addWidget(header_title)

        self.count_label = QLabel("[0]")
        self.count_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px;")
        header_layout.addWidget(self.count_label)

        header_layout.addStretch()

        self.selected_label = QLabel("")
        self.selected_label.setStyleSheet(f"color: {COLORS['neon_cyan']}; font-size: 11px;")
        header_layout.addWidget(self.selected_label)

        profiles_layout.addWidget(header)

        # Table
        self.table = CyberTable(["✓", "NAME", "STATUS", "FB"])
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 100)

        profiles_layout.addWidget(self.table)
        content.addWidget(profiles_card, 1)

        # RIGHT - Settings & Actions
        settings_card = CyberCard(COLORS['neon_purple'])
        settings_card.setFixedWidth(320)
        settings_layout = QVBoxLayout(settings_card)
        settings_layout.setContentsMargins(16, 16, 16, 16)
        settings_layout.setSpacing(12)

        # Title
        settings_title = QLabel("⚙️ CAI DAT LOGIN")
        settings_title.setStyleSheet(f"color: {COLORS['neon_purple']}; font-size: 14px; font-weight: bold; letter-spacing: 2px;")
        settings_layout.addWidget(settings_title)

        # Threads
        threads_row = QHBoxLayout()
        threads_label = QLabel("So luong:")
        threads_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        threads_label.setFixedWidth(80)
        threads_row.addWidget(threads_label)

        self.threads_spin = QSpinBox()
        self.threads_spin.setRange(1, 10)
        self.threads_spin.setValue(3)
        self.threads_spin.setStyleSheet(f"""
            QSpinBox {{
                background: {COLORS['bg_card']};
                color: {COLORS['text_primary']};
                border: 2px solid {COLORS['border']};
                border-radius: 8px;
                padding: 6px 12px;
                font-size: 14px;
            }}
            QSpinBox:focus {{
                border-color: {COLORS['neon_cyan']};
            }}
        """)
        threads_row.addWidget(self.threads_spin)
        threads_row.addStretch()

        settings_layout.addLayout(threads_row)

        # Delay
        delay_row = QHBoxLayout()
        delay_label = QLabel("Delay (s):")
        delay_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        delay_label.setFixedWidth(80)
        delay_row.addWidget(delay_label)

        self.delay_spin = QSpinBox()
        self.delay_spin.setRange(1, 60)
        self.delay_spin.setValue(5)
        self.delay_spin.setStyleSheet(f"""
            QSpinBox {{
                background: {COLORS['bg_card']};
                color: {COLORS['text_primary']};
                border: 2px solid {COLORS['border']};
                border-radius: 8px;
                padding: 6px 12px;
                font-size: 14px;
            }}
            QSpinBox:focus {{
                border-color: {COLORS['neon_cyan']};
            }}
        """)
        delay_row.addWidget(self.delay_spin)
        delay_row.addStretch()

        settings_layout.addLayout(delay_row)

        # Dest folder
        dest_row = QHBoxLayout()
        dest_label = QLabel("Folder dich:")
        dest_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        dest_label.setFixedWidth(80)
        dest_row.addWidget(dest_label)

        self.dest_combo = CyberComboBox(["-- Khong chuyen --"])
        dest_row.addWidget(self.dest_combo)

        settings_layout.addLayout(dest_row)

        # Options
        options_title = QLabel("📋 TUY CHON")
        options_title.setStyleSheet(f"color: {COLORS['neon_cyan']}; font-size: 12px; font-weight: bold; letter-spacing: 1px;")
        settings_layout.addWidget(options_title)

        # Delete bad
        delete_row = QHBoxLayout()
        self.delete_cb = CyberCheckBox()
        delete_row.addWidget(self.delete_cb)
        delete_label = QLabel("Xoa profile neu nick DIE")
        delete_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 11px;")
        delete_row.addWidget(delete_label)
        delete_row.addStretch()
        settings_layout.addLayout(delete_row)

        # Save XLSX
        save_row = QHBoxLayout()
        self.save_cb = CyberCheckBox()
        self.save_cb.setChecked(True)
        save_row.addWidget(self.save_cb)
        save_label = QLabel("Luu trang thai vao XLSX")
        save_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 11px;")
        save_row.addWidget(save_label)
        save_row.addStretch()
        settings_layout.addLayout(save_row)

        settings_layout.addStretch()

        # Actions
        actions_title = QLabel("🚀 HANH DONG")
        actions_title.setStyleSheet(f"color: {COLORS['neon_pink']}; font-size: 12px; font-weight: bold; letter-spacing: 1px;")
        settings_layout.addWidget(actions_title)

        btn_check = CyberButton("CHECK FB", "cyan", "🔍")
        btn_check.clicked.connect(self._check_fb_status)
        settings_layout.addWidget(btn_check)

        btn_start = CyberButton("BAT DAU LOGIN", "success", "▶️")
        btn_start.clicked.connect(self._start_login)
        settings_layout.addWidget(btn_start)

        btn_stop = CyberButton("DUNG", "danger", "⏹️")
        btn_stop.clicked.connect(self._stop_login)
        settings_layout.addWidget(btn_stop)

        # Progress
        self.progress_label = QLabel("")
        self.progress_label.setStyleSheet(f"color: {COLORS['neon_mint']}; font-size: 11px;")
        self.progress_label.setAlignment(Qt.AlignCenter)
        settings_layout.addWidget(self.progress_label)

        content.addWidget(settings_card)
        layout.addLayout(content, 1)

    def _load_folders(self):
        """Load folders tu Hidemium"""
        self.log("Loading folders...", "info")

        def fetch():
            try:
                return api.get_folders(limit=100)
            except Exception as e:
                return []

        def on_complete(folders):
            self.folders = folders or []

            self.folder_combo.clear()
            self.folder_combo.addItem("📁 Chon folder")
            for f in self.folders:
                name = f.get('name', 'Unknown')
                self.folder_combo.addItem(f"📁 {name}")

            self.dest_combo.clear()
            self.dest_combo.addItem("-- Khong chuyen --")
            for f in self.folders:
                name = f.get('name', 'Unknown')
                self.dest_combo.addItem(f"📁 {name}")

            self.log(f"Loaded {len(self.folders)} folders", "success")

        def run():
            result = fetch()
            QTimer.singleShot(0, lambda: on_complete(result))

        threading.Thread(target=run, daemon=True).start()

    def _on_folder_change(self, index):
        if index > 0:
            self._load_profiles()

    def _load_profiles(self):
        """Load profiles tu folder"""
        folder_idx = self.folder_combo.currentIndex()
        if folder_idx <= 0:
            return

        folder = self.folders[folder_idx - 1]
        folder_id = folder.get('id')

        self.log(f"Loading profiles from {folder.get('name')}...", "info")

        def fetch():
            try:
                return api.get_profiles(folder_id=[folder_id], limit=500)
            except:
                return []

        def on_complete(profiles):
            self.profiles = profiles or []
            self._update_table()
            self._update_stats()
            self.log(f"Loaded {len(self.profiles)} profiles", "success")

        def run():
            result = fetch()
            QTimer.singleShot(0, lambda: on_complete(result))

        threading.Thread(target=run, daemon=True).start()

    def _update_table(self):
        """Update table voi profiles"""
        self.table.setRowCount(len(self.profiles))
        self.profile_checkboxes.clear()

        for row, profile in enumerate(self.profiles):
            uuid = profile.get('uuid', '')
            name = profile.get('name', 'Unknown')
            status = profile.get('status', 'stopped')
            fb_status = self.profile_status.get(uuid, {})
            has_fb = fb_status.get('has_fb')

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
            self.profile_checkboxes[uuid] = checkbox

            # Name
            self.table.setItem(row, 1, QTableWidgetItem(name))

            # Status
            status_text = "🟢 Running" if status == "running" else "⚫ Stopped"
            self.table.setItem(row, 2, QTableWidgetItem(status_text))

            # FB
            if has_fb is True:
                fb_text = "✅ Co FB"
            elif has_fb is False:
                fb_text = "❌ Chua"
            else:
                fb_text = "❓ Chua check"
            self.table.setItem(row, 3, QTableWidgetItem(fb_text))

        self.count_label.setText(f"[{len(self.profiles)} profiles]")

    def _toggle_select_all(self, state):
        checked = state == Qt.Checked
        count = 0
        for uuid, cb in self.profile_checkboxes.items():
            cb.setChecked(checked)
            if checked:
                count += 1
        self.selected_label.setText(f"✓ {count} da chon" if checked else "")
        self._update_stats()

    def _update_selection_count(self):
        count = sum(1 for cb in self.profile_checkboxes.values() if cb.isChecked())
        self.selected_label.setText(f"✓ {count} da chon" if count > 0 else "")
        self.stat_selected.set_value(str(count))

    def _update_stats(self):
        self.stat_profiles.set_value(str(len(self.profiles)))
        selected = sum(1 for cb in self.profile_checkboxes.values() if cb.isChecked())
        self.stat_selected.set_value(str(selected))
        unused = len([a for a in self.accounts if not a.get('status')])
        self.stat_accounts.set_value(str(unused))

    def _browse_xlsx(self):
        """Chon file XLSX"""
        if not HAS_OPENPYXL:
            QMessageBox.warning(self, "Loi", "Can cai dat openpyxl:\npip install openpyxl")
            return

        path, _ = QFileDialog.getOpenFileName(
            self, "Chon file XLSX", "", "Excel Files (*.xlsx)"
        )

        if path:
            self.xlsx_path = path
            self.xlsx_input.setText(os.path.basename(path))
            self._load_xlsx()

    def _load_xlsx(self):
        """Load tai khoan tu XLSX"""
        try:
            self.workbook = openpyxl.load_workbook(self.xlsx_path)
            sheet = self.workbook.active

            self.accounts = []
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if row[1]:
                    self.accounts.append({
                        'status': row[0] or '',
                        'uid': str(row[1]),
                        'password': str(row[2]) if row[2] else '',
                        '2fa': str(row[3]) if row[3] else '',
                        'email': str(row[4]) if row[4] else '',
                        'email_pass': str(row[5]) if len(row) > 5 and row[5] else ''
                    })

            unused = [a for a in self.accounts if not a['status']]
            self.stat_accounts.set_value(str(len(unused)))
            self.log(f"Import {len(self.accounts)} accounts ({len(unused)} unused)", "success")

        except Exception as e:
            self.log(f"Error: {e}", "error")

    def _check_fb_status(self):
        """Check FB status"""
        self.log("Check FB: Dang phat trien...", "info")
        self.progress_label.setText("Tinh nang dang phat trien")

    def _start_login(self):
        """Bat dau login"""
        selected = [uuid for uuid, cb in self.profile_checkboxes.items() if cb.isChecked()]
        unused = [a for a in self.accounts if not a.get('status')]

        if not selected:
            QMessageBox.warning(self, "Loi", "Chua chon profile nao!")
            return

        if not unused:
            QMessageBox.warning(self, "Loi", "Khong co tai khoan chua dung!")
            return

        self._is_running = True
        self._stop_requested = False
        total = min(len(selected), len(unused))
        self.log(f"Bat dau login {total} profiles...", "info")

        def do_login():
            count = 0
            for i, uuid in enumerate(selected):
                if self._stop_requested or i >= len(unused):
                    break

                account = unused[i]
                name = next((p.get('name', '') for p in self.profiles if p.get('uuid') == uuid), uuid[:8])

                QTimer.singleShot(0, lambda m=f"[{i+1}/{total}] {name}": self.progress_label.setText(m))
                QTimer.singleShot(0, lambda m=f"Login {name}...": self.log(m, "info"))

                try:
                    result = api.open_browser(uuid)
                    if result.get('status') == 'successfully':
                        count += 1
                        QTimer.singleShot(0, lambda m=f"Opened {name}": self.log(m, "success"))
                    else:
                        QTimer.singleShot(0, lambda m=f"Failed: {result.get('title', 'Error')}": self.log(m, "error"))
                except Exception as e:
                    QTimer.singleShot(0, lambda m=f"Error: {e}": self.log(m, "error"))

                import time
                time.sleep(self.delay_spin.value())

            self._is_running = False
            QTimer.singleShot(0, lambda: self.progress_label.setText(f"Done: {count}/{total}"))
            QTimer.singleShot(0, lambda: self.log(f"Completed {count}/{total}", "success"))

        threading.Thread(target=do_login, daemon=True).start()

    def _stop_login(self):
        """Dung login"""
        self._stop_requested = True
        self.log("Stopping...", "info")
        self.progress_label.setText("Dang dung...")
