"""
Posts Page - Quan ly cac bai dang va buff tuong tac
PySide6 version
"""
import threading
from typing import List, Dict
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QScrollArea, QMessageBox, QSpinBox, QProgressBar
)
from PySide6.QtCore import Qt, QTimer

from config import COLORS
from widgets import (
    CyberButton, CyberInput, CyberComboBox, CyberCard,
    CyberTitle, CyberStatCard, CyberCheckBox
)
from db import get_posts, save_post, delete_post, update_post_stats


class PostsPage(QWidget):
    """Posts Page - Quan ly bai dang"""

    def __init__(self, log_func, parent=None):
        super().__init__(parent)
        self.log = log_func
        self.posts: List[Dict] = []
        self.editing_post = None

        # State
        self._is_running = False
        self._stop_requested = False

        self._setup_ui()
        QTimer.singleShot(500, self._load_data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(10)

        # Top bar
        top_bar = QHBoxLayout()
        title = CyberTitle("Posts", "Buff tuong tac", "mint")
        top_bar.addWidget(title)
        top_bar.addStretch()

        self.stat_total = CyberStatCard("POSTS", "0", "📝", "mint")
        self.stat_total.setFixedWidth(140)
        top_bar.addWidget(self.stat_total)

        self.stat_likes = CyberStatCard("LIKES", "0", "❤️", "pink")
        self.stat_likes.setFixedWidth(140)
        top_bar.addWidget(self.stat_likes)

        self.stat_comments = CyberStatCard("COMMENTS", "0", "💬", "cyan")
        self.stat_comments.setFixedWidth(140)
        top_bar.addWidget(self.stat_comments)

        layout.addLayout(top_bar)

        # Main content - 2 columns
        content = QHBoxLayout()
        content.setSpacing(12)

        # Left panel - Add post
        left_card = CyberCard(COLORS['neon_mint'])
        left_card.setFixedWidth(380)
        left_layout = QVBoxLayout(left_card)
        left_layout.setContentsMargins(12, 12, 12, 12)

        # Header
        add_label = QLabel("➕ Them bai dang")
        add_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 14px; font-weight: bold;")
        left_layout.addWidget(add_label)

        # URL
        url_label = QLabel("URL bai viet:")
        url_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        left_layout.addWidget(url_label)

        self.url_input = CyberInput("https://facebook.com/...")
        left_layout.addWidget(self.url_input)

        # Title
        title_label = QLabel("Tieu de (tuy chon):")
        title_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        left_layout.addWidget(title_label)

        self.title_input = CyberInput("Mo ta bai viet...")
        left_layout.addWidget(self.title_input)

        # Target likes
        likes_row = QHBoxLayout()
        likes_label = QLabel("Muc tieu Likes:")
        likes_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        likes_label.setFixedWidth(120)
        likes_row.addWidget(likes_label)

        self.target_likes = QSpinBox()
        self.target_likes.setRange(0, 10000)
        self.target_likes.setValue(100)
        self.target_likes.setStyleSheet(f"""
            QSpinBox {{
                background: {COLORS['bg_darker']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                padding: 6px;
            }}
        """)
        likes_row.addWidget(self.target_likes, 1)

        left_layout.addLayout(likes_row)

        # Target comments
        comments_row = QHBoxLayout()
        comments_label = QLabel("Muc tieu Comments:")
        comments_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        comments_label.setFixedWidth(120)
        comments_row.addWidget(comments_label)

        self.target_comments = QSpinBox()
        self.target_comments.setRange(0, 10000)
        self.target_comments.setValue(50)
        self.target_comments.setStyleSheet(f"""
            QSpinBox {{
                background: {COLORS['bg_darker']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                padding: 6px;
            }}
        """)
        comments_row.addWidget(self.target_comments, 1)

        left_layout.addLayout(comments_row)

        # Add button
        btn_row = QHBoxLayout()

        self.btn_add = CyberButton("Them bai", "success", "+")
        self.btn_add.clicked.connect(self._add_post)
        btn_row.addWidget(self.btn_add)

        self.btn_clear = CyberButton("Xoa form", "secondary")
        self.btn_clear.clicked.connect(self._clear_form)
        btn_row.addWidget(self.btn_clear)

        left_layout.addLayout(btn_row)

        # Divider
        divider = QFrame()
        divider.setFixedHeight(2)
        divider.setStyleSheet(f"background: {COLORS['border']}; margin: 10px 0;")
        left_layout.addWidget(divider)

        # Buff settings
        settings_label = QLabel("⚙️ Cai dat Buff")
        settings_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 14px; font-weight: bold;")
        left_layout.addWidget(settings_label)

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
                background: {COLORS['bg_darker']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                padding: 6px;
            }}
        """)
        threads_row.addWidget(self.threads_spin)

        delay_label = QLabel("Delay (s):")
        delay_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        threads_row.addWidget(delay_label)

        self.delay_spin = QSpinBox()
        self.delay_spin.setRange(1, 60)
        self.delay_spin.setValue(5)
        self.delay_spin.setStyleSheet(f"""
            QSpinBox {{
                background: {COLORS['bg_darker']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                padding: 6px;
            }}
        """)
        threads_row.addWidget(self.delay_spin)
        threads_row.addStretch()

        left_layout.addLayout(threads_row)

        # Action buttons
        action_row = QHBoxLayout()

        self.btn_start = CyberButton("Bat dau Buff", "success", "▶️")
        self.btn_start.clicked.connect(self._start_buff)
        action_row.addWidget(self.btn_start)

        self.btn_stop = CyberButton("Dung", "danger", "⏹️")
        self.btn_stop.clicked.connect(self._stop_buff)
        action_row.addWidget(self.btn_stop)

        left_layout.addLayout(action_row)

        # Progress
        self.progress_label = QLabel("")
        self.progress_label.setStyleSheet(f"color: {COLORS['neon_mint']}; font-size: 11px;")
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
                background: {COLORS['neon_mint']};
                border-radius: 3px;
            }}
        """)
        left_layout.addWidget(self.progress_bar)

        left_layout.addStretch()
        content.addWidget(left_card)

        # Right panel - Post list
        right_card = CyberCard(COLORS['neon_pink'])
        right_layout = QVBoxLayout(right_card)
        right_layout.setContentsMargins(12, 12, 12, 12)

        # Header
        header_row = QHBoxLayout()
        posts_label = QLabel("📋 Danh sach bai dang")
        posts_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 14px; font-weight: bold;")
        header_row.addWidget(posts_label)

        header_row.addStretch()

        btn_refresh = CyberButton("", "ghost", "🔄")
        btn_refresh.setFixedWidth(36)
        btn_refresh.clicked.connect(self._load_data)
        header_row.addWidget(btn_refresh)

        right_layout.addLayout(header_row)

        # Search
        self.search_input = CyberInput("🔍 Tim kiem...")
        self.search_input.textChanged.connect(self._filter_posts)
        right_layout.addWidget(self.search_input)

        # Table header
        table_header = QFrame()
        table_header.setFixedHeight(32)
        table_header.setStyleSheet(f"background: {COLORS['bg_card']}; border-radius: 4px;")
        table_header_layout = QHBoxLayout(table_header)
        table_header_layout.setContentsMargins(8, 0, 8, 0)

        headers = [("URL / Tieu de", 250), ("Likes", 80), ("Comments", 80), ("Trang thai", 80)]
        for text, width in headers:
            lbl = QLabel(text)
            lbl.setFixedWidth(width)
            lbl.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 10px; font-weight: bold;")
            table_header_layout.addWidget(lbl)

        table_header_layout.addStretch()
        right_layout.addWidget(table_header)

        # Post list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                background: {COLORS['bg_darker']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
            }}
        """)

        self.post_list_widget = QWidget()
        self.post_list_layout = QVBoxLayout(self.post_list_widget)
        self.post_list_layout.setContentsMargins(8, 8, 8, 8)
        self.post_list_layout.setSpacing(4)

        empty = QLabel("Chua co bai dang nao")
        empty.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px;")
        empty.setAlignment(Qt.AlignCenter)
        self.post_list_layout.addWidget(empty)
        self.post_list_layout.addStretch()

        scroll.setWidget(self.post_list_widget)
        right_layout.addWidget(scroll, 1)

        content.addWidget(right_card, 1)
        layout.addLayout(content, 1)

    def _load_data(self):
        """Load posts"""
        self.posts = get_posts()
        self._render_posts()
        self._update_stats()
        self.log(f"Loaded {len(self.posts)} posts", "success")

    def _render_posts(self, search_text=None):
        """Render danh sach posts"""
        while self.post_list_layout.count() > 0:
            item = self.post_list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        posts_to_show = self.posts
        if search_text:
            search_lower = search_text.lower()
            posts_to_show = [p for p in self.posts
                           if search_lower in p.get('url', '').lower()
                           or search_lower in p.get('title', '').lower()]

        if not posts_to_show:
            empty = QLabel("Chua co bai dang nao")
            empty.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px;")
            empty.setAlignment(Qt.AlignCenter)
            self.post_list_layout.addWidget(empty)
        else:
            for post in posts_to_show:
                row = self._create_post_row(post)
                self.post_list_layout.addWidget(row)

        self.post_list_layout.addStretch()

    def _create_post_row(self, post: Dict):
        """Tao row cho post"""
        row = QWidget()
        row.setStyleSheet(f"background: {COLORS['bg_card']}; border-radius: 4px;")
        row.setFixedHeight(50)

        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(8, 4, 8, 4)
        row_layout.setSpacing(8)

        # Title/URL
        title = post.get('title') or post.get('url', '')[:40]
        title_label = QLabel(title[:35] + "..." if len(title) > 35 else title)
        title_label.setFixedWidth(250)
        title_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 11px;")
        row_layout.addWidget(title_label)

        # Likes
        likes = f"{post.get('like_count', 0)}/{post.get('target_likes', 0)}"
        likes_label = QLabel(likes)
        likes_label.setFixedWidth(80)
        likes_label.setStyleSheet(f"color: {COLORS['neon_pink']}; font-size: 11px;")
        row_layout.addWidget(likes_label)

        # Comments
        comments = f"{post.get('comment_count', 0)}/{post.get('target_comments', 0)}"
        comments_label = QLabel(comments)
        comments_label.setFixedWidth(80)
        comments_label.setStyleSheet(f"color: {COLORS['neon_cyan']}; font-size: 11px;")
        row_layout.addWidget(comments_label)

        # Status
        status = post.get('status', 'pending')
        status_colors = {
            'pending': COLORS['neon_yellow'],
            'running': COLORS['neon_cyan'],
            'completed': COLORS['neon_mint'],
            'error': COLORS['neon_coral']
        }
        status_label = QLabel(status.upper())
        status_label.setFixedWidth(80)
        status_label.setStyleSheet(f"color: {status_colors.get(status, COLORS['text_muted'])}; font-size: 10px; font-weight: bold;")
        row_layout.addWidget(status_label)

        # Delete button
        btn_del = CyberButton("🗑️", "danger")
        btn_del.setFixedSize(28, 28)
        btn_del.clicked.connect(lambda: self._delete_post(post.get('id')))
        row_layout.addWidget(btn_del)

        row_layout.addStretch()
        return row

    def _filter_posts(self, text):
        self._render_posts(text)

    def _add_post(self):
        """Them bai dang moi"""
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Loi", "Chua nhap URL!")
            return

        if not url.startswith('http'):
            QMessageBox.warning(self, "Loi", "URL khong hop le!")
            return

        save_post({
            'url': url,
            'title': self.title_input.text(),
            'target_likes': self.target_likes.value(),
            'target_comments': self.target_comments.value(),
            'status': 'pending'
        })

        self.log(f"Da them bai dang: {url[:40]}...", "success")
        self._clear_form()
        self._load_data()

    def _delete_post(self, post_id):
        """Xoa bai dang"""
        reply = QMessageBox.question(
            self, "Xac nhan",
            "Ban co chac muon xoa bai dang nay?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            delete_post(post_id)
            self.log("Da xoa bai dang", "success")
            self._load_data()

    def _clear_form(self):
        """Clear form"""
        self.url_input.clear()
        self.title_input.clear()
        self.target_likes.setValue(100)
        self.target_comments.setValue(50)

    def _start_buff(self):
        """Bat dau buff tuong tac"""
        pending_posts = [p for p in self.posts if p.get('status') == 'pending']

        if not pending_posts:
            QMessageBox.warning(self, "Loi", "Khong co bai dang nao dang cho!")
            return

        self._is_running = True
        self._stop_requested = False
        self.progress_bar.setMaximum(len(pending_posts))
        self.log(f"Bat dau buff {len(pending_posts)} bai dang...", "info")

        def do_buff():
            for i, post in enumerate(pending_posts):
                if self._stop_requested:
                    break

                QTimer.singleShot(0, lambda v=i+1: self.progress_bar.setValue(v))
                QTimer.singleShot(0, lambda m=f"Buff bai {i+1}/{len(pending_posts)}...": self.progress_label.setText(m))

                # TODO: Implement actual buffing
                import time
                time.sleep(self.delay_spin.value())

            self._is_running = False
            QTimer.singleShot(0, lambda: self.log("Buff hoan thanh!", "success"))
            QTimer.singleShot(0, lambda: self.progress_label.setText("Hoan thanh!"))

        threading.Thread(target=do_buff, daemon=True).start()

    def _stop_buff(self):
        """Dung buff"""
        self._stop_requested = True
        self.log("Dang dung...", "info")

    def _update_stats(self):
        total = len(self.posts)
        total_likes = sum(p.get('like_count', 0) for p in self.posts)
        total_comments = sum(p.get('comment_count', 0) for p in self.posts)

        self.stat_total.set_value(str(total))
        self.stat_likes.set_value(str(total_likes))
        self.stat_comments.set_value(str(total_comments))
