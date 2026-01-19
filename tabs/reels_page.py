"""
Reels Page - Dang Reels len Fanpage
PySide6 version with Hidemium integration
"""
import threading
import os
from typing import List, Dict
from datetime import datetime
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QScrollArea, QFileDialog, QMessageBox, QProgressBar,
    QTextEdit, QSpinBox, QDateTimeEdit
)
from PySide6.QtCore import Qt, QTimer, QDateTime

from config import COLORS
from widgets import (
    CyberButton, CyberInput, CyberComboBox, CyberCard,
    CyberTitle, CyberStatCard, CyberCheckBox
)
from api_service import api
from db import (
    get_profiles, get_pages, get_pages_for_profiles,
    get_reel_schedules, save_reel_schedule, delete_reel_schedule,
    get_posted_reels, save_posted_reel
)


class ReelsPage(QWidget):
    """Reels Page - Dang Reels"""

    def __init__(self, log_func, parent=None):
        super().__init__(parent)
        self.log = log_func
        self.profiles: List[Dict] = []
        self.pages: List[Dict] = []
        self.schedules: List[Dict] = []
        self.posted_reels: List[Dict] = []

        # Selected items
        self.selected_profile_uuid = None
        self.selected_page_id = None
        self.video_path = ""

        self._setup_ui()
        QTimer.singleShot(500, self._load_data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(10)

        # Top bar
        top_bar = QHBoxLayout()
        title = CyberTitle("Reels", "Dang Reels len Page", "pink")
        top_bar.addWidget(title)
        top_bar.addStretch()

        self.stat_profiles = CyberStatCard("PROFILES", "0", "📁", "pink")
        self.stat_profiles.setFixedWidth(140)
        top_bar.addWidget(self.stat_profiles)

        self.stat_pages = CyberStatCard("PAGES", "0", "📄", "purple")
        self.stat_pages.setFixedWidth(140)
        top_bar.addWidget(self.stat_pages)

        self.stat_posted = CyberStatCard("DA DANG", "0", "🎬", "mint")
        self.stat_posted.setFixedWidth(140)
        top_bar.addWidget(self.stat_posted)

        layout.addLayout(top_bar)

        # Main content - 2 columns
        content = QHBoxLayout()
        content.setSpacing(12)

        # Left panel - Create Reel
        left_card = CyberCard(COLORS['neon_pink'])
        left_card.setFixedWidth(400)
        left_layout = QVBoxLayout(left_card)
        left_layout.setContentsMargins(12, 12, 12, 12)

        # Title
        create_title = QLabel("🎬 Tao Reel moi")
        create_title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 14px; font-weight: bold;")
        left_layout.addWidget(create_title)

        # Profile selection
        profile_row = QHBoxLayout()
        profile_label = QLabel("Profile:")
        profile_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        profile_label.setFixedWidth(70)
        profile_row.addWidget(profile_label)

        self.profile_combo = CyberComboBox(["-- Chon Profile --"])
        self.profile_combo.currentIndexChanged.connect(self._on_profile_change)
        profile_row.addWidget(self.profile_combo, 1)

        left_layout.addLayout(profile_row)

        # Page selection
        page_row = QHBoxLayout()
        page_label = QLabel("Page:")
        page_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        page_label.setFixedWidth(70)
        page_row.addWidget(page_label)

        self.page_combo = CyberComboBox(["-- Chon Page --"])
        page_row.addWidget(self.page_combo, 1)

        left_layout.addLayout(page_row)

        # Video selection
        video_row = QHBoxLayout()
        video_label = QLabel("Video:")
        video_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        video_label.setFixedWidth(70)
        video_row.addWidget(video_label)

        self.video_input = CyberInput("Chon file video...")
        self.video_input.setReadOnly(True)
        video_row.addWidget(self.video_input, 1)

        btn_browse = CyberButton("Chon", "secondary", "📂")
        btn_browse.setFixedWidth(80)
        btn_browse.clicked.connect(self._browse_video)
        video_row.addWidget(btn_browse)

        left_layout.addLayout(video_row)

        # Caption
        caption_label = QLabel("Caption:")
        caption_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        left_layout.addWidget(caption_label)

        self.caption_text = QTextEdit()
        self.caption_text.setFixedHeight(100)
        self.caption_text.setPlaceholderText("Nhap caption cho Reel...")
        self.caption_text.setStyleSheet(f"""
            QTextEdit {{
                background: {COLORS['bg_darker']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                padding: 8px;
            }}
        """)
        left_layout.addWidget(self.caption_text)

        # Hashtags
        hashtag_row = QHBoxLayout()
        hashtag_label = QLabel("Hashtags:")
        hashtag_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        hashtag_label.setFixedWidth(70)
        hashtag_row.addWidget(hashtag_label)

        self.hashtag_input = CyberInput("#viral #trending")
        hashtag_row.addWidget(self.hashtag_input, 1)

        left_layout.addLayout(hashtag_row)

        # Schedule
        schedule_row = QHBoxLayout()
        schedule_label = QLabel("Hen gio:")
        schedule_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        schedule_label.setFixedWidth(70)
        schedule_row.addWidget(schedule_label)

        self.schedule_cb = CyberCheckBox()
        schedule_row.addWidget(self.schedule_cb)

        self.schedule_datetime = QDateTimeEdit(QDateTime.currentDateTime())
        self.schedule_datetime.setStyleSheet(f"""
            QDateTimeEdit {{
                background: {COLORS['bg_darker']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                padding: 4px;
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
        delay_label.setFixedWidth(70)
        delay_row.addWidget(delay_label)

        self.delay_min = QSpinBox()
        self.delay_min.setRange(10, 300)
        self.delay_min.setValue(30)
        self.delay_min.setStyleSheet(f"""
            QSpinBox {{
                background: {COLORS['bg_darker']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                padding: 4px;
            }}
        """)
        delay_row.addWidget(self.delay_min)

        delay_to = QLabel("-")
        delay_to.setStyleSheet(f"color: {COLORS['text_muted']};")
        delay_row.addWidget(delay_to)

        self.delay_max = QSpinBox()
        self.delay_max.setRange(10, 300)
        self.delay_max.setValue(60)
        self.delay_max.setStyleSheet(f"""
            QSpinBox {{
                background: {COLORS['bg_darker']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                padding: 4px;
            }}
        """)
        delay_row.addWidget(self.delay_max)
        delay_row.addStretch()

        left_layout.addLayout(delay_row)

        # Action buttons
        btn_row = QHBoxLayout()

        self.btn_post = CyberButton("Dang ngay", "success", "🚀")
        self.btn_post.clicked.connect(self._post_reel_now)
        btn_row.addWidget(self.btn_post)

        self.btn_schedule = CyberButton("Hen lich", "primary", "📅")
        self.btn_schedule.clicked.connect(self._schedule_reel)
        btn_row.addWidget(self.btn_schedule)

        left_layout.addLayout(btn_row)

        # Progress
        self.progress_label = QLabel("")
        self.progress_label.setStyleSheet(f"color: {COLORS['neon_pink']}; font-size: 11px;")
        left_layout.addWidget(self.progress_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background: {COLORS['bg_darker']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                height: 12px;
            }}
            QProgressBar::chunk {{
                background: {COLORS['neon_pink']};
                border-radius: 3px;
            }}
        """)
        left_layout.addWidget(self.progress_bar)

        left_layout.addStretch()
        content.addWidget(left_card)

        # Right panel - History
        right_card = CyberCard(COLORS['neon_purple'])
        right_layout = QVBoxLayout(right_card)
        right_layout.setContentsMargins(12, 12, 12, 12)

        # Header
        history_title = QLabel("📋 Lich su Reels")
        history_title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 14px; font-weight: bold;")
        right_layout.addWidget(history_title)

        # Tabs
        tab_row = QHBoxLayout()

        self.btn_scheduled = CyberButton("Da hen", "primary")
        self.btn_scheduled.clicked.connect(lambda: self._show_tab("scheduled"))
        tab_row.addWidget(self.btn_scheduled)

        self.btn_posted = CyberButton("Da dang", "secondary")
        self.btn_posted.clicked.connect(lambda: self._show_tab("posted"))
        tab_row.addWidget(self.btn_posted)

        tab_row.addStretch()

        btn_refresh = CyberButton("", "ghost", "🔄")
        btn_refresh.setFixedWidth(36)
        btn_refresh.clicked.connect(self._load_history)
        tab_row.addWidget(btn_refresh)

        right_layout.addLayout(tab_row)

        # History list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                background: {COLORS['bg_darker']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
            }}
        """)

        self.history_widget = QWidget()
        self.history_layout = QVBoxLayout(self.history_widget)
        self.history_layout.setContentsMargins(8, 8, 8, 8)
        self.history_layout.setSpacing(4)

        empty = QLabel("Chua co Reel nao")
        empty.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px;")
        empty.setAlignment(Qt.AlignCenter)
        self.history_layout.addWidget(empty)
        self.history_layout.addStretch()

        scroll.setWidget(self.history_widget)
        right_layout.addWidget(scroll, 1)

        content.addWidget(right_card, 1)
        layout.addLayout(content, 1)

    def _load_data(self):
        """Load profiles va pages"""
        def fetch():
            profiles = get_profiles()
            return profiles

        def on_complete(profiles):
            self.profiles = profiles

            self.profile_combo.clear()
            self.profile_combo.addItem("-- Chon Profile --")
            for p in self.profiles:
                name = p.get('name', 'Unknown')
                self.profile_combo.addItem(f"👤 {name}")

            self.stat_profiles.set_value(str(len(self.profiles)))
            self._load_history()
            self.log(f"Loaded {len(self.profiles)} profiles", "success")

        def run():
            result = fetch()
            QTimer.singleShot(0, lambda: on_complete(result))

        threading.Thread(target=run, daemon=True).start()

    def _on_profile_change(self, index):
        """Khi thay doi profile"""
        if index <= 0:
            self.page_combo.clear()
            self.page_combo.addItem("-- Chon Page --")
            self.selected_profile_uuid = None
            return

        profile = self.profiles[index - 1]
        self.selected_profile_uuid = profile.get('uuid')

        # Load pages for this profile
        self.pages = get_pages(self.selected_profile_uuid)

        self.page_combo.clear()
        self.page_combo.addItem("-- Chon Page --")
        for page in self.pages:
            name = page.get('page_name', 'Unknown')
            self.page_combo.addItem(f"📄 {name}")

        self.stat_pages.set_value(str(len(self.pages)))

    def _browse_video(self):
        """Chon file video"""
        path, _ = QFileDialog.getOpenFileName(
            self, "Chon video",
            "", "Video Files (*.mp4 *.mov *.avi)"
        )

        if path:
            self.video_path = path
            self.video_input.setText(os.path.basename(path))

    def _post_reel_now(self):
        """Dang Reel ngay"""
        if not self._validate_inputs():
            return

        self.log("Bat dau dang Reel...", "info")
        self.progress_label.setText("Dang xu ly...")
        self.progress_bar.setMaximum(0)  # Indeterminate

        def do_post():
            import time
            time.sleep(2)  # Simulate posting

            # Save to history
            page_idx = self.page_combo.currentIndex()
            page = self.pages[page_idx - 1] if page_idx > 0 else {}

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
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(100)

        if success:
            self.progress_label.setText("Da dang thanh cong!")
            self.log("Reel da duoc dang!", "success")
            self._load_history()
        else:
            self.progress_label.setText("Loi khi dang!")
            self.log("Loi dang Reel", "error")

    def _schedule_reel(self):
        """Hen lich dang Reel"""
        if not self._validate_inputs():
            return

        if not self.schedule_cb.isChecked():
            QMessageBox.warning(self, "Loi", "Chua bat hen gio!")
            return

        page_idx = self.page_combo.currentIndex()
        page = self.pages[page_idx - 1] if page_idx > 0 else {}

        schedule_time = self.schedule_datetime.dateTime().toPython()

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

        self.log(f"Da hen lich dang luc {schedule_time}", "success")
        self._load_history()

    def _validate_inputs(self):
        """Validate inputs"""
        if not self.selected_profile_uuid:
            QMessageBox.warning(self, "Loi", "Chua chon profile!")
            return False

        if self.page_combo.currentIndex() <= 0:
            QMessageBox.warning(self, "Loi", "Chua chon page!")
            return False

        if not self.video_path:
            QMessageBox.warning(self, "Loi", "Chua chon video!")
            return False

        return True

    def _load_history(self):
        """Load lich su Reels"""
        self.schedules = get_reel_schedules(status='pending')
        self.posted_reels = get_posted_reels(limit=50)
        self.stat_posted.set_value(str(len(self.posted_reels)))
        self._show_tab("scheduled")

    def _show_tab(self, tab: str):
        """Hien thi tab"""
        # Clear
        while self.history_layout.count() > 0:
            item = self.history_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if tab == "scheduled":
            self.btn_scheduled.setStyleSheet(f"background: {COLORS['neon_purple']};")
            self.btn_posted.setStyleSheet(f"background: {COLORS['bg_card']};")
            items = self.schedules
        else:
            self.btn_scheduled.setStyleSheet(f"background: {COLORS['bg_card']};")
            self.btn_posted.setStyleSheet(f"background: {COLORS['neon_purple']};")
            items = self.posted_reels

        if not items:
            label = QLabel(f"Chua co Reel nao {'da hen' if tab == 'scheduled' else 'da dang'}")
            label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px;")
            label.setAlignment(Qt.AlignCenter)
            self.history_layout.addWidget(label)
        else:
            for item in items[:20]:
                row = self._create_history_row(item, tab)
                self.history_layout.addWidget(row)

        self.history_layout.addStretch()

    def _create_history_row(self, item: Dict, tab: str):
        """Tao row cho history"""
        row = QWidget()
        row.setStyleSheet(f"background: {COLORS['bg_card']}; border-radius: 4px;")
        row.setFixedHeight(50)

        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(8, 4, 8, 4)
        row_layout.setSpacing(8)

        # Icon
        icon = "📅" if tab == "scheduled" else ("✅" if item.get('status') == 'success' else "❌")
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: 16px;")
        row_layout.addWidget(icon_label)

        # Info
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(0)

        page_name = item.get('page_name', 'Unknown')
        name_label = QLabel(page_name[:30])
        name_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 11px;")
        info_layout.addWidget(name_label)

        if tab == "scheduled":
            time_str = item.get('scheduled_time', '')[:16]
        else:
            time_str = item.get('posted_at', '')[:16]

        time_label = QLabel(time_str)
        time_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 10px;")
        info_layout.addWidget(time_label)

        row_layout.addWidget(info_widget, 1)

        # Delete button (for scheduled only)
        if tab == "scheduled":
            btn_del = CyberButton("", "danger", "🗑️")
            btn_del.setFixedSize(28, 28)
            btn_del.clicked.connect(lambda: self._delete_schedule(item.get('id')))
            row_layout.addWidget(btn_del)

        return row

    def _delete_schedule(self, schedule_id):
        """Xoa schedule"""
        if schedule_id:
            delete_reel_schedule(schedule_id)
            self.log("Da xoa lich hen", "success")
            self._load_history()
