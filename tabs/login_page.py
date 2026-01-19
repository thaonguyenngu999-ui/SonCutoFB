"""
Login Page - Dang nhap Facebook cho cac profiles
PySide6 version with Hidemium integration
"""
import threading
import os
from typing import List, Dict, Optional
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QScrollArea, QCheckBox, QFileDialog, QProgressBar, QTextEdit,
    QRadioButton, QButtonGroup, QSpinBox, QMessageBox
)
from PySide6.QtCore import Qt, QTimer, Signal, QObject

from config import COLORS
from widgets import (
    CyberButton, CyberInput, CyberComboBox, CyberCard,
    CyberTitle, CyberStatCard, CyberTable, CyberCheckBox
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
    """Login Page - Dang nhap Facebook"""

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
        self.profile_checkboxes: Dict[str, QCheckBox] = {}

        # Running state
        self._is_running = False
        self._stop_requested = False

        self._setup_ui()
        QTimer.singleShot(500, self._load_folders)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(10)

        # Top bar
        top_bar = QHBoxLayout()
        title = CyberTitle("Login FB", "Dang nhap Facebook", "mint")
        top_bar.addWidget(title)
        top_bar.addStretch()

        self.stat_total = CyberStatCard("PROFILES", "0", "📁", "mint")
        self.stat_total.setFixedWidth(140)
        top_bar.addWidget(self.stat_total)

        self.stat_selected = CyberStatCard("DA CHON", "0", "✓", "cyan")
        self.stat_selected.setFixedWidth(140)
        top_bar.addWidget(self.stat_selected)

        self.stat_accounts = CyberStatCard("TAI KHOAN", "0", "👤", "purple")
        self.stat_accounts.setFixedWidth(140)
        top_bar.addWidget(self.stat_accounts)

        layout.addLayout(top_bar)

        # Main content - 2 columns
        content = QHBoxLayout()
        content.setSpacing(12)

        # Left panel - Profile selection
        left_card = CyberCard(COLORS['neon_mint'])
        left_card.setFixedWidth(350)
        left_layout = QVBoxLayout(left_card)
        left_layout.setContentsMargins(12, 12, 12, 12)

        # Folder selection
        folder_row = QHBoxLayout()
        folder_label = QLabel("Thu muc:")
        folder_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        folder_row.addWidget(folder_label)

        self.folder_combo = CyberComboBox(["-- Chon --"])
        self.folder_combo.setFixedWidth(180)
        self.folder_combo.currentIndexChanged.connect(self._on_folder_change)
        folder_row.addWidget(self.folder_combo)

        btn_load = CyberButton("Tai", "cyan")
        btn_load.setFixedWidth(60)
        btn_load.clicked.connect(self._load_profiles)
        folder_row.addWidget(btn_load)

        left_layout.addLayout(folder_row)

        # Check FB controls
        check_row = QHBoxLayout()
        check_label = QLabel("Luong:")
        check_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        check_row.addWidget(check_label)

        self.check_threads = QSpinBox()
        self.check_threads.setRange(1, 10)
        self.check_threads.setValue(3)
        self.check_threads.setFixedWidth(60)
        self.check_threads.setStyleSheet(f"""
            QSpinBox {{
                background: {COLORS['bg_darker']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                padding: 4px;
            }}
        """)
        check_row.addWidget(self.check_threads)

        btn_check = CyberButton("Check FB", "primary", "🔍")
        btn_check.clicked.connect(self._check_fb_status)
        check_row.addWidget(btn_check)
        check_row.addStretch()

        left_layout.addLayout(check_row)

        # Filter
        filter_row = QHBoxLayout()
        self.filter_group = QButtonGroup(self)

        filters = [("Tat ca", "all"), ("Chua co FB", "no_fb"), ("Co FB", "has_fb")]
        for text, value in filters:
            radio = QRadioButton(text)
            radio.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 11px;")
            radio.setProperty("filter_value", value)
            radio.toggled.connect(self._apply_filter)
            self.filter_group.addButton(radio)
            filter_row.addWidget(radio)
            if value == "all":
                radio.setChecked(True)

        filter_row.addStretch()
        left_layout.addLayout(filter_row)

        # Select all
        select_row = QHBoxLayout()
        self.select_all_cb = CyberCheckBox()
        self.select_all_cb.stateChanged.connect(self._toggle_all)
        select_row.addWidget(self.select_all_cb)

        select_label = QLabel("Chon tat ca")
        select_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        select_row.addWidget(select_label)

        self.count_label = QLabel("(0 da chon)")
        self.count_label.setStyleSheet(f"color: {COLORS['neon_cyan']}; font-size: 11px;")
        select_row.addWidget(self.count_label)
        select_row.addStretch()

        left_layout.addLayout(select_row)

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

        content.addWidget(left_card)

        # Right panel - Login settings
        right_card = CyberCard(COLORS['neon_cyan'])
        right_layout = QVBoxLayout(right_card)
        right_layout.setContentsMargins(12, 12, 12, 12)

        # Import XLSX section
        import_title = QLabel("📥 Import tai khoan Facebook")
        import_title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 14px; font-weight: bold;")
        right_layout.addWidget(import_title)

        import_hint = QLabel("XLSX: A(Status), B(UID), C(Password), D(2FA), E(Email), F(Email Pass)")
        import_hint.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 10px;")
        import_hint.setWordWrap(True)
        right_layout.addWidget(import_hint)

        import_row = QHBoxLayout()
        self.xlsx_input = CyberInput("Chon file XLSX...")
        self.xlsx_input.setReadOnly(True)
        import_row.addWidget(self.xlsx_input, 1)

        btn_browse = CyberButton("Chon file", "secondary", "📂")
        btn_browse.clicked.connect(self._browse_xlsx)
        import_row.addWidget(btn_browse)

        right_layout.addLayout(import_row)

        self.account_info = QLabel("Chua import file")
        self.account_info.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 11px;")
        right_layout.addWidget(self.account_info)

        # Account preview
        self.account_scroll = QScrollArea()
        self.account_scroll.setWidgetResizable(True)
        self.account_scroll.setFixedHeight(120)
        self.account_scroll.setStyleSheet(f"""
            QScrollArea {{
                background: {COLORS['bg_darker']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
            }}
        """)

        self.account_list_widget = QWidget()
        self.account_list_layout = QVBoxLayout(self.account_list_widget)
        self.account_list_layout.setContentsMargins(8, 8, 8, 8)
        self.account_list_layout.setSpacing(2)

        placeholder = QLabel("Import XLSX de xem danh sach")
        placeholder.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px;")
        placeholder.setAlignment(Qt.AlignCenter)
        self.account_list_layout.addWidget(placeholder)

        self.account_scroll.setWidget(self.account_list_widget)
        right_layout.addWidget(self.account_scroll)

        # Login settings
        settings_title = QLabel("⚙️ Cai dat Login")
        settings_title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 14px; font-weight: bold;")
        right_layout.addWidget(settings_title)

        settings_row1 = QHBoxLayout()

        threads_label = QLabel("So luong:")
        threads_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        settings_row1.addWidget(threads_label)

        self.login_threads = QSpinBox()
        self.login_threads.setRange(1, 10)
        self.login_threads.setValue(3)
        self.login_threads.setFixedWidth(60)
        self.login_threads.setStyleSheet(f"""
            QSpinBox {{
                background: {COLORS['bg_darker']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                padding: 4px;
            }}
        """)
        settings_row1.addWidget(self.login_threads)

        delay_label = QLabel("Delay (s):")
        delay_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        settings_row1.addWidget(delay_label)

        self.delay_spin = QSpinBox()
        self.delay_spin.setRange(1, 60)
        self.delay_spin.setValue(5)
        self.delay_spin.setFixedWidth(60)
        self.delay_spin.setStyleSheet(f"""
            QSpinBox {{
                background: {COLORS['bg_darker']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                padding: 4px;
            }}
        """)
        settings_row1.addWidget(self.delay_spin)
        settings_row1.addStretch()

        right_layout.addLayout(settings_row1)

        # Options
        options_row = QHBoxLayout()

        self.delete_bad_cb = CyberCheckBox()
        options_row.addWidget(self.delete_bad_cb)
        delete_label = QLabel("Xoa profile neu nick DIE")
        delete_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 11px;")
        options_row.addWidget(delete_label)

        self.save_xlsx_cb = CyberCheckBox()
        self.save_xlsx_cb.setChecked(True)
        options_row.addWidget(self.save_xlsx_cb)
        save_label = QLabel("Luu trang thai vao XLSX")
        save_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 11px;")
        options_row.addWidget(save_label)
        options_row.addStretch()

        right_layout.addLayout(options_row)

        # Dest folder
        dest_row = QHBoxLayout()
        dest_label = QLabel("Folder dich (LIVE):")
        dest_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        dest_row.addWidget(dest_label)

        self.dest_folder_combo = CyberComboBox(["-- Khong chuyen --"])
        self.dest_folder_combo.setFixedWidth(200)
        dest_row.addWidget(self.dest_folder_combo)
        dest_row.addStretch()

        right_layout.addLayout(dest_row)

        # Action buttons
        btn_row = QHBoxLayout()

        self.btn_start = CyberButton("Bat dau Login", "success", "▶️")
        self.btn_start.clicked.connect(self._start_login)
        btn_row.addWidget(self.btn_start)

        self.btn_stop = CyberButton("Dung", "danger", "⏹️")
        self.btn_stop.clicked.connect(self._stop_login)
        btn_row.addWidget(self.btn_stop)
        btn_row.addStretch()

        right_layout.addLayout(btn_row)

        # Progress
        self.progress_label = QLabel("")
        self.progress_label.setStyleSheet(f"color: {COLORS['neon_cyan']}; font-size: 12px; font-weight: bold;")
        right_layout.addWidget(self.progress_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background: {COLORS['bg_darker']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                height: 16px;
            }}
            QProgressBar::chunk {{
                background: {COLORS['neon_cyan']};
                border-radius: 3px;
            }}
        """)
        right_layout.addWidget(self.progress_bar)

        # Log
        log_title = QLabel("📋 Log")
        log_title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 14px; font-weight: bold;")
        right_layout.addWidget(log_title)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet(f"""
            QTextEdit {{
                background: {COLORS['bg_darker']};
                color: {COLORS['text_secondary']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                font-family: 'Consolas', monospace;
                font-size: 11px;
            }}
        """)
        right_layout.addWidget(self.log_text, 1)

        content.addWidget(right_card, 1)
        layout.addLayout(content, 1)

    def _load_folders(self):
        """Load danh sach folders"""
        def fetch():
            try:
                return api.get_folders(limit=100)
            except Exception as e:
                return []

        def on_complete(folders):
            self.folders = folders or []

            self.folder_combo.clear()
            self.folder_combo.addItem("-- Chon --")
            for f in self.folders:
                name = f.get('name', 'Unknown')
                self.folder_combo.addItem(f"📁 {name}")

            # Update dest folder combo
            self.dest_folder_combo.clear()
            self.dest_folder_combo.addItem("-- Khong chuyen --")
            for f in self.folders:
                name = f.get('name', 'Unknown')
                self.dest_folder_combo.addItem(f"📁 {name}")

            self._add_log(f"Da tai {len(self.folders)} folders")

        def run():
            result = fetch()
            QTimer.singleShot(0, lambda: on_complete(result))

        threading.Thread(target=run, daemon=True).start()

    def _on_folder_change(self, index):
        if index > 0:
            self._load_profiles()

    def _load_profiles(self):
        """Load profiles theo folder"""
        folder_idx = self.folder_combo.currentIndex()
        if folder_idx <= 0:
            return

        folder = self.folders[folder_idx - 1]
        folder_id = folder.get('id')

        def fetch():
            try:
                return api.get_profiles(folder_id=[folder_id], limit=500)
            except:
                return []

        def on_complete(profiles):
            self.profiles = profiles or []
            self._render_profiles()
            self._update_stats()
            self._add_log(f"Da tai {len(self.profiles)} profiles")

        def run():
            result = fetch()
            QTimer.singleShot(0, lambda: on_complete(result))

        threading.Thread(target=run, daemon=True).start()

    def _render_profiles(self):
        """Render danh sach profiles"""
        # Clear old
        while self.profile_list_layout.count() > 0:
            item = self.profile_list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.profile_checkboxes.clear()

        if not self.profiles:
            label = QLabel("Khong co profile nao")
            label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px;")
            label.setAlignment(Qt.AlignCenter)
            self.profile_list_layout.addWidget(label)
            self.profile_list_layout.addStretch()
            return

        # Get filter
        filter_value = "all"
        for btn in self.filter_group.buttons():
            if btn.isChecked():
                filter_value = btn.property("filter_value")
                break

        visible_count = 0
        for profile in self.profiles:
            uuid = profile.get('uuid', '')
            name = profile.get('name', 'Unknown')

            # Check filter
            status = self.profile_status.get(uuid, {})
            has_fb = status.get('has_fb')

            if filter_value == "no_fb" and has_fb is True:
                continue
            if filter_value == "has_fb" and has_fb is not True:
                continue

            visible_count += 1

            # Create row
            row = QWidget()
            row.setStyleSheet(f"background: {COLORS['bg_card']}; border-radius: 4px;")
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(8, 4, 8, 4)
            row_layout.setSpacing(8)

            cb = CyberCheckBox()
            cb.stateChanged.connect(self._update_selection_count)
            self.profile_checkboxes[uuid] = cb
            row_layout.addWidget(cb)

            name_label = QLabel(name[:25] + "..." if len(name) > 25 else name)
            name_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 11px;")
            row_layout.addWidget(name_label, 1)

            # Status
            if has_fb is True:
                status_text = "✅"
                status_color = COLORS['neon_mint']
            elif has_fb is False:
                status_text = "❌"
                status_color = COLORS['neon_coral']
            else:
                status_text = "❓"
                status_color = COLORS['text_muted']

            status_label = QLabel(status_text)
            status_label.setStyleSheet(f"color: {status_color}; font-size: 12px;")
            row_layout.addWidget(status_label)

            self.profile_list_layout.addWidget(row)

        self.profile_list_layout.addStretch()
        self.stat_total.set_value(str(visible_count))

    def _apply_filter(self):
        self._render_profiles()

    def _toggle_all(self, state):
        checked = state == Qt.Checked
        for cb in self.profile_checkboxes.values():
            cb.setChecked(checked)
        self._update_selection_count()

    def _update_selection_count(self):
        count = sum(1 for cb in self.profile_checkboxes.values() if cb.isChecked())
        self.count_label.setText(f"({count} da chon)")
        self.stat_selected.set_value(str(count))

    def _update_stats(self):
        self.stat_total.set_value(str(len(self.profiles)))
        self._update_selection_count()
        self.stat_accounts.set_value(str(len(self.accounts)))

    def _browse_xlsx(self):
        """Chon file XLSX"""
        if not HAS_OPENPYXL:
            QMessageBox.warning(self, "Loi", "Can cai dat openpyxl: pip install openpyxl")
            return

        path, _ = QFileDialog.getOpenFileName(
            self, "Chon file XLSX", "", "Excel Files (*.xlsx)"
        )

        if path:
            self.xlsx_path = path
            self.xlsx_input.setText(os.path.basename(path))
            self._load_xlsx()

    def _load_xlsx(self):
        """Load tai khoan tu file XLSX"""
        try:
            self.workbook = openpyxl.load_workbook(self.xlsx_path)
            sheet = self.workbook.active

            self.accounts = []
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if row[1]:  # UID
                    self.accounts.append({
                        'status': row[0] or '',
                        'uid': str(row[1]),
                        'password': str(row[2]) if row[2] else '',
                        '2fa': str(row[3]) if row[3] else '',
                        'email': str(row[4]) if row[4] else '',
                        'email_pass': str(row[5]) if len(row) > 5 and row[5] else ''
                    })

            # Filter unused accounts
            unused = [a for a in self.accounts if not a['status']]
            self.account_info.setText(f"Da import {len(self.accounts)} tai khoan ({len(unused)} chua dung)")
            self.stat_accounts.set_value(str(len(unused)))

            self._render_accounts()
            self._add_log(f"Import {len(self.accounts)} tai khoan")

        except Exception as e:
            self._add_log(f"Loi doc file: {e}")

    def _render_accounts(self):
        """Render danh sach accounts"""
        while self.account_list_layout.count() > 0:
            item = self.account_list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        unused = [a for a in self.accounts if not a['status']]
        for acc in unused[:10]:  # Show max 10
            label = QLabel(f"👤 {acc['uid']} - {'✓ 2FA' if acc['2fa'] else 'No 2FA'}")
            label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 10px;")
            self.account_list_layout.addWidget(label)

        if len(unused) > 10:
            more = QLabel(f"... va {len(unused) - 10} tai khoan khac")
            more.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 10px;")
            self.account_list_layout.addWidget(more)

    def _check_fb_status(self):
        """Check trang thai FB cua profiles"""
        self._add_log("Check FB status: Tinh nang dang phat trien...")

    def _start_login(self):
        """Bat dau qua trinh login"""
        selected = [uuid for uuid, cb in self.profile_checkboxes.items() if cb.isChecked()]
        unused = [a for a in self.accounts if not a['status']]

        if not selected:
            QMessageBox.warning(self, "Loi", "Chua chon profile nao!")
            return

        if not unused:
            QMessageBox.warning(self, "Loi", "Khong co tai khoan nao chua su dung!")
            return

        self._is_running = True
        self._stop_requested = False
        self._add_log(f"Bat dau login {len(selected)} profiles voi {len(unused)} tai khoan")
        self.progress_bar.setMaximum(min(len(selected), len(unused)))

        # Start login thread
        def do_login():
            count = 0
            for i, uuid in enumerate(selected):
                if self._stop_requested or i >= len(unused):
                    break

                account = unused[i]
                name = next((p.get('name', '') for p in self.profiles if p.get('uuid') == uuid), uuid[:8])

                QTimer.singleShot(0, lambda m=f"[{i+1}] Login {name}...": self._add_log(m))
                QTimer.singleShot(0, lambda v=i+1: self.progress_bar.setValue(v))

                # Goi API open browser
                try:
                    result = api.open_browser(uuid)
                    if result.get('status') == 'successfully':
                        QTimer.singleShot(0, lambda m=f"[{i+1}] Da mo browser {name}": self._add_log(m))
                        count += 1
                    else:
                        QTimer.singleShot(0, lambda m=f"[{i+1}] Loi mo browser: {result.get('title', 'Unknown')}": self._add_log(m))
                except Exception as e:
                    QTimer.singleShot(0, lambda m=f"[{i+1}] Exception: {e}": self._add_log(m))

                import time
                time.sleep(self.delay_spin.value())

            self._is_running = False
            QTimer.singleShot(0, lambda: self._add_log(f"Hoan thanh! Da mo {count} profiles"))
            QTimer.singleShot(0, lambda: self.progress_label.setText(f"Hoan thanh: {count}/{len(selected)}"))

        threading.Thread(target=do_login, daemon=True).start()

    def _stop_login(self):
        """Dung qua trinh login"""
        self._stop_requested = True
        self._add_log("Dang dung...")

    def _add_log(self, message: str):
        """Them log"""
        from datetime import datetime
        time_str = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{time_str}] {message}")
        self.log(message, "info")
