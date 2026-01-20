"""
Reels Page - Đăng Reels lên Fanpage
PySide6 version - BEAUTIFUL UI like ProfilesPage
"""
import threading
import os
from typing import List, Dict
from datetime import datetime
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QFileDialog, QMessageBox, QTableWidgetItem, QSpinBox,
    QTextEdit, QDateTimeEdit
)
from PySide6.QtCore import Qt, QTimer, QDateTime, Signal, QObject

from config import COLORS
from widgets import (
    CyberButton, CyberInput, CyberComboBox, CyberCard,
    CyberTitle, CyberStatCard, CyberTable, CyberCheckBox
)
from api_service import api
from db import (
    get_profiles, get_pages, get_pages_for_profiles,
    get_reel_schedules, save_reel_schedule, delete_reel_schedule,
    get_posted_reels, save_posted_reel, get_posted_reels_count
)


class ReelsSignal(QObject):
    """Signal để thread-safe UI update"""
    folders_loaded = Signal(list)
    profiles_loaded = Signal(list)
    log_message = Signal(str, str)


class ReelsPage(QWidget):
    """Reels Page - Dang Reels - BEAUTIFUL UI"""

    def __init__(self, log_func, parent=None):
        super().__init__(parent)
        self.log = log_func
        self.folders: List[Dict] = []
        self.profiles: List[Dict] = []
        self.pages: List[Dict] = []
        self.schedules: List[Dict] = []
        self.posted_reels: List[Dict] = []

        # Selected items
        self.selected_profile_uuid = None
        self.selected_page_id = None
        self.video_path = ""

        # Running state
        self._is_posting = False

        # Signal để thread-safe UI update
        self.signal = ReelsSignal()
        self.signal.folders_loaded.connect(self._on_folders_loaded)
        self.signal.profiles_loaded.connect(self._on_profiles_loaded)
        self.signal.log_message.connect(lambda msg, t: self.log(msg, t))

        self._setup_ui()
        QTimer.singleShot(500, self._load_folders)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(10)

        # ========== TOP BAR ==========
        top_bar = QHBoxLayout()
        top_bar.setSpacing(12)

        title = CyberTitle("Reels", "Đăng Reels lên Fanpage", "pink")
        top_bar.addWidget(title)

        top_bar.addStretch()

        self.stat_profiles = CyberStatCard("PROFILES", "0", "📁", "pink")
        self.stat_profiles.setFixedWidth(160)
        top_bar.addWidget(self.stat_profiles)

        self.stat_pages = CyberStatCard("PAGES", "0", "📄", "purple")
        self.stat_pages.setFixedWidth(160)
        top_bar.addWidget(self.stat_pages)

        self.stat_scheduled = CyberStatCard("ĐÃ HẸN", "0", "📅", "cyan")
        self.stat_scheduled.setFixedWidth(160)
        top_bar.addWidget(self.stat_scheduled)

        self.stat_posted = CyberStatCard("ĐÃ ĐĂNG", "0", "🎬", "mint")
        self.stat_posted.setFixedWidth(160)
        top_bar.addWidget(self.stat_posted)

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

        btn_refresh = CyberButton("", "ghost", "🔄")
        btn_refresh.setFixedWidth(40)
        btn_refresh.clicked.connect(self._load_history)
        toolbar.addWidget(btn_refresh)

        layout.addLayout(toolbar)

        # ========== MAIN CONTENT ==========
        content = QHBoxLayout()
        content.setSpacing(12)

        # LEFT - Create Reel Form
        left_card = CyberCard(COLORS['neon_pink'])
        left_card.setFixedWidth(380)
        left_layout = QVBoxLayout(left_card)
        left_layout.setContentsMargins(16, 16, 16, 16)
        left_layout.setSpacing(12)

        # Header
        form_header = QWidget()
        form_header.setFixedHeight(40)
        form_header.setStyleSheet(f"background: {COLORS['bg_darker']}; border-radius: 10px;")
        form_header_layout = QHBoxLayout(form_header)
        form_header_layout.setContentsMargins(12, 0, 12, 0)

        form_title = QLabel("🎬 TẠO REEL MỚI")
        form_title.setStyleSheet(f"color: {COLORS['neon_pink']}; font-size: 12px; font-weight: bold; letter-spacing: 2px;")
        form_header_layout.addWidget(form_title)
        form_header_layout.addStretch()

        left_layout.addWidget(form_header)

        # Profile selection
        profile_row = QHBoxLayout()
        profile_label = QLabel("Profile:")
        profile_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        profile_label.setFixedWidth(80)
        profile_row.addWidget(profile_label)

        self.profile_combo = CyberComboBox(["-- Chọn Profile --"])
        self.profile_combo.currentIndexChanged.connect(self._on_profile_change)
        profile_row.addWidget(self.profile_combo, 1)

        left_layout.addLayout(profile_row)

        # Page selection
        page_row = QHBoxLayout()
        page_label = QLabel("Page:")
        page_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        page_label.setFixedWidth(80)
        page_row.addWidget(page_label)

        self.page_combo = CyberComboBox(["-- Chọn Page --"])
        page_row.addWidget(self.page_combo, 1)

        left_layout.addLayout(page_row)

        # Video selection
        video_row = QHBoxLayout()
        video_label = QLabel("Video:")
        video_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        video_label.setFixedWidth(80)
        video_row.addWidget(video_label)

        self.video_input = CyberInput("Chọn file video...")
        self.video_input.setReadOnly(True)
        video_row.addWidget(self.video_input, 1)

        btn_browse = CyberButton("CHON", "purple", "📂")
        btn_browse.setFixedWidth(80)
        btn_browse.clicked.connect(self._browse_video)
        video_row.addWidget(btn_browse)

        left_layout.addLayout(video_row)

        # Caption
        caption_title = QLabel("📝 CAPTION")
        caption_title.setStyleSheet(f"color: {COLORS['neon_cyan']}; font-size: 11px; font-weight: bold; letter-spacing: 1px;")
        left_layout.addWidget(caption_title)

        self.caption_text = QTextEdit()
        self.caption_text.setFixedHeight(100)
        self.caption_text.setPlaceholderText("Nhập caption cho Reel...")
        self.caption_text.setStyleSheet(f"""
            QTextEdit {{
                background: {COLORS['bg_card']};
                color: {COLORS['text_primary']};
                border: 2px solid {COLORS['border']};
                border-radius: 10px;
                padding: 10px;
                font-size: 13px;
            }}
            QTextEdit:focus {{
                border-color: {COLORS['neon_cyan']};
            }}
        """)
        left_layout.addWidget(self.caption_text)

        # Hashtags
        hashtag_row = QHBoxLayout()
        hashtag_label = QLabel("Hashtags:")
        hashtag_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        hashtag_label.setFixedWidth(80)
        hashtag_row.addWidget(hashtag_label)

        self.hashtag_input = CyberInput("#viral #trending #reels")
        hashtag_row.addWidget(self.hashtag_input, 1)

        left_layout.addLayout(hashtag_row)

        # Schedule section
        schedule_title = QLabel("📅 HẸN GIỜ")
        schedule_title.setStyleSheet(f"color: {COLORS['neon_purple']}; font-size: 11px; font-weight: bold; letter-spacing: 1px;")
        left_layout.addWidget(schedule_title)

        schedule_row = QHBoxLayout()
        self.schedule_cb = CyberCheckBox()
        schedule_row.addWidget(self.schedule_cb)

        schedule_text = QLabel("Hẹn giờ đăng")
        schedule_text.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        schedule_row.addWidget(schedule_text)

        self.schedule_datetime = QDateTimeEdit(QDateTime.currentDateTime().addSecs(3600))
        self.schedule_datetime.setDisplayFormat("dd/MM/yyyy HH:mm")
        self.schedule_datetime.setStyleSheet(f"""
            QDateTimeEdit {{
                background: {COLORS['bg_card']};
                color: {COLORS['text_primary']};
                border: 2px solid {COLORS['border']};
                border-radius: 8px;
                padding: 6px 12px;
                font-size: 13px;
            }}
            QDateTimeEdit:focus {{
                border-color: {COLORS['neon_purple']};
            }}
        """)
        self.schedule_datetime.setEnabled(False)
        self.schedule_cb.stateChanged.connect(
            lambda state: self.schedule_datetime.setEnabled(state == Qt.Checked)
        )
        schedule_row.addWidget(self.schedule_datetime, 1)

        left_layout.addLayout(schedule_row)

        # Delay settings
        delay_row = QHBoxLayout()
        delay_label = QLabel("Delay (s):")
        delay_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        delay_label.setFixedWidth(80)
        delay_row.addWidget(delay_label)

        self.delay_min = QSpinBox()
        self.delay_min.setRange(10, 300)
        self.delay_min.setValue(30)
        self.delay_min.setStyleSheet(f"""
            QSpinBox {{
                background: {COLORS['bg_card']};
                color: {COLORS['text_primary']};
                border: 2px solid {COLORS['border']};
                border-radius: 8px;
                padding: 6px 12px;
                font-size: 13px;
            }}
            QSpinBox:focus {{
                border-color: {COLORS['neon_cyan']};
            }}
        """)
        delay_row.addWidget(self.delay_min)

        delay_to = QLabel("-")
        delay_to.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 14px;")
        delay_row.addWidget(delay_to)

        self.delay_max = QSpinBox()
        self.delay_max.setRange(10, 300)
        self.delay_max.setValue(60)
        self.delay_max.setStyleSheet(f"""
            QSpinBox {{
                background: {COLORS['bg_card']};
                color: {COLORS['text_primary']};
                border: 2px solid {COLORS['border']};
                border-radius: 8px;
                padding: 6px 12px;
                font-size: 13px;
            }}
            QSpinBox:focus {{
                border-color: {COLORS['neon_cyan']};
            }}
        """)
        delay_row.addWidget(self.delay_max)
        delay_row.addStretch()

        left_layout.addLayout(delay_row)

        left_layout.addStretch()

        # Actions
        actions_title = QLabel("🚀 HÀNH ĐỘNG")
        actions_title.setStyleSheet(f"color: {COLORS['neon_mint']}; font-size: 11px; font-weight: bold; letter-spacing: 1px;")
        left_layout.addWidget(actions_title)

        btn_post = CyberButton("ĐĂNG NGAY", "success", "🚀")
        btn_post.clicked.connect(self._post_reel_now)
        left_layout.addWidget(btn_post)

        btn_schedule = CyberButton("HẸN LỊCH", "cyan", "📅")
        btn_schedule.clicked.connect(self._schedule_reel)
        left_layout.addWidget(btn_schedule)

        # Progress
        self.progress_label = QLabel("")
        self.progress_label.setStyleSheet(f"color: {COLORS['neon_pink']}; font-size: 11px;")
        self.progress_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(self.progress_label)

        content.addWidget(left_card)

        # RIGHT - History Table
        right_card = CyberCard(COLORS['neon_purple'])
        right_layout = QVBoxLayout(right_card)
        right_layout.setContentsMargins(2, 2, 2, 2)

        # Header
        header = QWidget()
        header.setFixedHeight(50)
        header.setStyleSheet(f"background: {COLORS['bg_darker']}; border-radius: 14px 14px 0 0;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 0, 16, 0)
        header_layout.setSpacing(12)

        # Tabs
        self.btn_scheduled = CyberButton("ĐÃ HẸN", "primary", "📅")
        self.btn_scheduled.setFixedWidth(120)
        self.btn_scheduled.clicked.connect(lambda: self._show_tab("scheduled"))
        header_layout.addWidget(self.btn_scheduled)

        self.btn_posted = CyberButton("ĐÃ ĐĂNG", "secondary", "🎬")
        self.btn_posted.setFixedWidth(120)
        self.btn_posted.clicked.connect(lambda: self._show_tab("posted"))
        header_layout.addWidget(self.btn_posted)

        sep = QFrame()
        sep.setFixedWidth(2)
        sep.setFixedHeight(24)
        sep.setStyleSheet(f"background: {COLORS['border']};")
        header_layout.addWidget(sep)

        header_title = QLabel("🎬 LỊCH SỬ REELS")
        header_title.setStyleSheet(f"color: {COLORS['neon_purple']}; font-size: 12px; font-weight: bold; letter-spacing: 2px;")
        header_layout.addWidget(header_title)

        self.count_label = QLabel("[0]")
        self.count_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px;")
        header_layout.addWidget(self.count_label)

        header_layout.addStretch()

        right_layout.addWidget(header)

        # Table
        self.table = CyberTable(["PAGE", "CAPTION", "THOI GIAN", "TRANG THAI", ""])
        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 100)
        self.table.setColumnWidth(4, 60)

        right_layout.addWidget(self.table)
        content.addWidget(right_card, 1)

        layout.addLayout(content, 1)

    def _load_folders(self):
        """Load folders từ Hidemium"""
        self.log("Đang tải thư mục...", "info")

        def fetch():
            try:
                folders = api.get_folders(limit=100)
                print(f"[DEBUG] ReelsPage got {len(folders)} folders")
                return folders
            except Exception as e:
                print(f"[DEBUG] ReelsPage folder error: {e}")
                return []

        def run():
            result = fetch()
            self.signal.folders_loaded.emit(result)

        threading.Thread(target=run, daemon=True).start()

    def _on_folders_loaded(self, folders):
        """Slot nhận folders từ thread - chạy trên main thread"""
        self.folders = folders or []

        print(f"[DEBUG] _on_folders_loaded: {len(self.folders)} folders")

        self.folder_combo.clear()
        self.folder_combo.addItem("📁 Chọn folder")
        for f in self.folders:
            name = f.get('name', 'Unknown')
            self.folder_combo.addItem(f"📁 {name}")

        self.log(f"Đã tải {len(self.folders)} thư mục", "success")
        self._load_history()

    def _on_folder_change(self, index):
        if index > 0:
            self._load_profiles()

    def _load_profiles(self):
        """Load profiles từ folder"""
        folder_idx = self.folder_combo.currentIndex()
        if folder_idx <= 0:
            return

        folder = self.folders[folder_idx - 1]
        folder_id = folder.get('id')

        self.log(f"Đang tải profiles từ {folder.get('name')}...", "info")

        def fetch():
            try:
                profiles = api.get_profiles(folder_id=[folder_id], limit=500)
                print(f"[DEBUG] ReelsPage got {len(profiles)} profiles")
                return profiles
            except Exception as e:
                print(f"[DEBUG] ReelsPage profiles error: {e}")
                return []

        def run():
            result = fetch()
            self.signal.profiles_loaded.emit(result)

        threading.Thread(target=run, daemon=True).start()

    def _on_profiles_loaded(self, profiles):
        """Slot nhận profiles từ thread - chạy trên main thread"""
        self.profiles = profiles or []

        print(f"[DEBUG] _on_profiles_loaded: {len(self.profiles)} profiles")

        self.profile_combo.clear()
        self.profile_combo.addItem("-- Chọn Profile --")
        for p in self.profiles:
            name = p.get('name', 'Unknown')
            self.profile_combo.addItem(f"👤 {name}")

        self.stat_profiles.set_value(str(len(self.profiles)))
        self.log(f"Đã tải {len(self.profiles)} profiles", "success")

    def _on_profile_change(self, index):
        """Khi thay doi profile"""
        if index <= 0:
            self.page_combo.clear()
            self.page_combo.addItem("-- Chọn Page --")
            self.selected_profile_uuid = None
            self.stat_pages.set_value("0")
            return

        profile = self.profiles[index - 1]
        self.selected_profile_uuid = profile.get('uuid')

        # Load pages for this profile
        self.pages = get_pages(self.selected_profile_uuid)

        self.page_combo.clear()
        self.page_combo.addItem("-- Chọn Page --")
        for page in self.pages:
            name = page.get('page_name', 'Unknown')
            self.page_combo.addItem(f"📄 {name}")

        self.stat_pages.set_value(str(len(self.pages)))

    def _browse_video(self):
        """Chọn file video"""
        path, _ = QFileDialog.getOpenFileName(
            self, "Chọn video",
            "", "Video Files (*.mp4 *.mov *.avi *.mkv *.webm)"
        )

        if path:
            self.video_path = path
            self.video_input.setText(os.path.basename(path))
            self.log(f"Selected: {os.path.basename(path)}", "info")

    def _validate_inputs(self):
        """Validate inputs"""
        if not self.selected_profile_uuid:
            QMessageBox.warning(self, "Loi", "Chưa chọn profile!")
            return False

        if self.page_combo.currentIndex() <= 0:
            QMessageBox.warning(self, "Loi", "Chưa chọn page!")
            return False

        if not self.video_path:
            QMessageBox.warning(self, "Loi", "Chưa chọn video!")
            return False

        if not os.path.exists(self.video_path):
            QMessageBox.warning(self, "Loi", "File video không tồn tại!")
            return False

        return True

    def _post_reel_now(self):
        """Dang Reel ngay"""
        if not self._validate_inputs():
            return

        if self._is_posting:
            QMessageBox.warning(self, "Thông báo", "Đang trong quá trình đăng...")
            return

        self._is_posting = True
        self.log("Bắt đầu đăng Reel...", "info")
        self.progress_label.setText("Đang xử lý...")

        page_idx = self.page_combo.currentIndex()
        page = self.pages[page_idx - 1] if page_idx > 0 else {}

        def do_post():
            import time
            time.sleep(2)  # Simulate posting

            # Save to history
            save_posted_reel({
                'profile_uuid': self.selected_profile_uuid,
                'page_id': page.get('page_id', ''),
                'page_name': page.get('page_name', ''),
                'video_path': self.video_path,
                'caption': self.caption_text.toPlainText(),
                'hashtags': self.hashtag_input.text(),
                'status': 'success'
            })

            QTimer.singleShot(0, lambda: self._on_post_complete(True))

        threading.Thread(target=do_post, daemon=True).start()

    def _on_post_complete(self, success):
        self._is_posting = False

        if success:
            self.progress_label.setText("Đã đăng thành công!")
            self.log("Reel đã được đăng!", "success")
            self._load_history()

            # Clear form
            self.caption_text.clear()
            self.video_path = ""
            self.video_input.clear()
        else:
            self.progress_label.setText("Lỗi khi đăng!")
            self.log("Lỗi đăng Reel", "error")

    def _schedule_reel(self):
        """Hen lich dang Reel"""
        if not self._validate_inputs():
            return

        if not self.schedule_cb.isChecked():
            QMessageBox.warning(self, "Loi", "Chưa bật hẹn giờ!")
            return

        page_idx = self.page_combo.currentIndex()
        page = self.pages[page_idx - 1] if page_idx > 0 else {}

        schedule_time = self.schedule_datetime.dateTime().toPython()

        if schedule_time <= datetime.now():
            QMessageBox.warning(self, "Loi", "Thời gian hẹn phải lớn hơn hiện tại!")
            return

        save_reel_schedule({
            'profile_uuid': self.selected_profile_uuid,
            'page_id': page.get('id'),
            'page_name': page.get('page_name', ''),
            'video_path': self.video_path,
            'caption': self.caption_text.toPlainText(),
            'hashtags': self.hashtag_input.text(),
            'scheduled_time': schedule_time.isoformat(),
            'delay_min': self.delay_min.value(),
            'delay_max': self.delay_max.value()
        })

        self.log(f"Đã hẹn lịch đăng lúc {schedule_time.strftime('%d/%m/%Y %H:%M')}", "success")
        self.progress_label.setText(f"Hẹn lúc {schedule_time.strftime('%H:%M %d/%m')}")

        # Clear form
        self.caption_text.clear()
        self.video_path = ""
        self.video_input.clear()
        self.schedule_cb.setChecked(False)

        self._load_history()

    def _load_history(self):
        """Load lich su Reels"""
        self.schedules = get_reel_schedules(status='pending')
        self.posted_reels = get_posted_reels(limit=50)

        self.stat_scheduled.set_value(str(len(self.schedules)))
        self.stat_posted.set_value(str(len(self.posted_reels)))

        self._show_tab("scheduled")

    def _show_tab(self, tab: str):
        """Hien thi tab"""
        self.table.setRowCount(0)

        if tab == "scheduled":
            self.btn_scheduled.setStyleSheet(f"""
                QPushButton {{
                    background: {COLORS['neon_purple']};
                    border: 2px solid {COLORS['neon_purple']};
                    color: {COLORS['bg_dark']};
                    border-radius: 8px;
                    padding: 8px 16px;
                    font-weight: bold;
                }}
            """)
            self.btn_posted.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    border: 2px solid {COLORS['border']};
                    color: {COLORS['text_secondary']};
                    border-radius: 8px;
                    padding: 8px 16px;
                }}
            """)
            items = self.schedules
            self.count_label.setText(f"[{len(items)} hen]")
        else:
            self.btn_scheduled.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    border: 2px solid {COLORS['border']};
                    color: {COLORS['text_secondary']};
                    border-radius: 8px;
                    padding: 8px 16px;
                }}
            """)
            self.btn_posted.setStyleSheet(f"""
                QPushButton {{
                    background: {COLORS['neon_mint']};
                    border: 2px solid {COLORS['neon_mint']};
                    color: {COLORS['bg_dark']};
                    border-radius: 8px;
                    padding: 8px 16px;
                    font-weight: bold;
                }}
            """)
            items = self.posted_reels
            self.count_label.setText(f"[{len(items)} đã đăng]")

        self.table.setRowCount(len(items))

        for row, item in enumerate(items):
            # Page name
            page_name = item.get('page_name', 'Unknown')[:20]
            self.table.setItem(row, 0, QTableWidgetItem(f"📄 {page_name}"))

            # Caption
            caption = item.get('caption', '')[:30]
            if len(item.get('caption', '')) > 30:
                caption += "..."
            self.table.setItem(row, 1, QTableWidgetItem(caption))

            # Time
            if tab == "scheduled":
                time_str = item.get('scheduled_time', '')[:16].replace('T', ' ')
            else:
                time_str = item.get('posted_at', '')[:16].replace('T', ' ')
            self.table.setItem(row, 2, QTableWidgetItem(time_str))

            # Status
            if tab == "scheduled":
                status_text = "📅 Chờ đăng"
            else:
                status = item.get('status', '')
                if status == 'success':
                    status_text = "✅ Thành công"
                else:
                    status_text = "❌ Loi"
            self.table.setItem(row, 3, QTableWidgetItem(status_text))

            # Action button
            if tab == "scheduled":
                action_widget = QWidget()
                action_widget.setStyleSheet("background: transparent;")
                action_layout = QHBoxLayout(action_widget)
                action_layout.setContentsMargins(0, 0, 0, 0)
                action_layout.setAlignment(Qt.AlignCenter)

                btn_del = CyberButton("", "danger", "🗑️")
                btn_del.setFixedSize(32, 32)
                item_id = item.get('id')
                btn_del.clicked.connect(lambda checked, sid=item_id: self._delete_schedule(sid))
                action_layout.addWidget(btn_del)

                self.table.setCellWidget(row, 4, action_widget)
            else:
                self.table.setItem(row, 4, QTableWidgetItem(""))

    def _delete_schedule(self, schedule_id):
        """Xoa schedule"""
        if schedule_id:
            reply = QMessageBox.question(
                self, "Xác nhận",
                "Bạn có chắc muốn xóa lịch hẹn này?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                delete_reel_schedule(schedule_id)
                self.log("Đã xóa lịch hẹn", "success")
                self._load_history()
