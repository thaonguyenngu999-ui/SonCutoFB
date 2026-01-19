"""
Content Page - Quan ly noi dung dang bai
PySide6 version
"""
import threading
from typing import List, Dict
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QScrollArea, QMessageBox, QTextEdit, QFileDialog
)
from PySide6.QtCore import Qt, QTimer

from config import COLORS
from widgets import (
    CyberButton, CyberInput, CyberComboBox, CyberCard,
    CyberTitle, CyberStatCard, CyberCheckBox
)
from db import (
    get_categories, save_category, delete_category,
    get_contents, save_content, delete_content, get_contents_count
)


class ContentPage(QWidget):
    """Content Page - Quan ly noi dung"""

    def __init__(self, log_func, parent=None):
        super().__init__(parent)
        self.log = log_func
        self.categories: List[Dict] = []
        self.contents: List[Dict] = []
        self.current_category_id = None
        self.editing_content = None

        self._setup_ui()
        QTimer.singleShot(500, self._load_data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(10)

        # Top bar
        top_bar = QHBoxLayout()
        title = CyberTitle("Content", "Quan ly noi dung", "yellow")
        top_bar.addWidget(title)
        top_bar.addStretch()

        self.stat_categories = CyberStatCard("CATEGORIES", "0", "📁", "yellow")
        self.stat_categories.setFixedWidth(140)
        top_bar.addWidget(self.stat_categories)

        self.stat_contents = CyberStatCard("NOI DUNG", "0", "📝", "cyan")
        self.stat_contents.setFixedWidth(140)
        top_bar.addWidget(self.stat_contents)

        layout.addLayout(top_bar)

        # Main content - 3 columns
        content = QHBoxLayout()
        content.setSpacing(12)

        # Left panel - Categories
        left_card = CyberCard(COLORS['neon_yellow'])
        left_card.setFixedWidth(220)
        left_layout = QVBoxLayout(left_card)
        left_layout.setContentsMargins(12, 12, 12, 12)

        # Header
        cat_header = QHBoxLayout()
        cat_label = QLabel("📁 Danh muc")
        cat_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 14px; font-weight: bold;")
        cat_header.addWidget(cat_label)

        btn_add_cat = CyberButton("+", "success")
        btn_add_cat.setFixedSize(32, 32)
        btn_add_cat.clicked.connect(self._add_category)
        cat_header.addWidget(btn_add_cat)

        left_layout.addLayout(cat_header)

        # Category list
        scroll_cat = QScrollArea()
        scroll_cat.setWidgetResizable(True)
        scroll_cat.setStyleSheet(f"""
            QScrollArea {{
                background: {COLORS['bg_darker']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
            }}
        """)

        self.cat_list_widget = QWidget()
        self.cat_list_layout = QVBoxLayout(self.cat_list_widget)
        self.cat_list_layout.setContentsMargins(8, 8, 8, 8)
        self.cat_list_layout.setSpacing(4)
        self.cat_list_layout.addStretch()

        scroll_cat.setWidget(self.cat_list_widget)
        left_layout.addWidget(scroll_cat, 1)

        content.addWidget(left_card)

        # Middle panel - Content list
        middle_card = CyberCard(COLORS['neon_cyan'])
        middle_layout = QVBoxLayout(middle_card)
        middle_layout.setContentsMargins(12, 12, 12, 12)

        # Header
        content_header = QHBoxLayout()
        content_label = QLabel("📝 Noi dung")
        content_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 14px; font-weight: bold;")
        content_header.addWidget(content_label)

        content_header.addStretch()

        self.search_input = CyberInput("🔍 Tim kiem...")
        self.search_input.setFixedWidth(200)
        self.search_input.textChanged.connect(self._filter_contents)
        content_header.addWidget(self.search_input)

        btn_add_content = CyberButton("Them noi dung", "success", "+")
        btn_add_content.clicked.connect(self._add_content)
        content_header.addWidget(btn_add_content)

        middle_layout.addLayout(content_header)

        # Content list
        scroll_content = QScrollArea()
        scroll_content.setWidgetResizable(True)
        scroll_content.setStyleSheet(f"""
            QScrollArea {{
                background: {COLORS['bg_darker']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
            }}
        """)

        self.content_list_widget = QWidget()
        self.content_list_layout = QVBoxLayout(self.content_list_widget)
        self.content_list_layout.setContentsMargins(8, 8, 8, 8)
        self.content_list_layout.setSpacing(4)

        empty = QLabel("Chon danh muc de xem noi dung")
        empty.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px;")
        empty.setAlignment(Qt.AlignCenter)
        self.content_list_layout.addWidget(empty)
        self.content_list_layout.addStretch()

        scroll_content.setWidget(self.content_list_widget)
        middle_layout.addWidget(scroll_content, 1)

        content.addWidget(middle_card, 1)

        # Right panel - Editor
        right_card = CyberCard(COLORS['neon_mint'])
        right_card.setFixedWidth(350)
        right_layout = QVBoxLayout(right_card)
        right_layout.setContentsMargins(12, 12, 12, 12)

        # Header
        editor_label = QLabel("✏️ Chinh sua")
        editor_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 14px; font-weight: bold;")
        right_layout.addWidget(editor_label)

        # Title
        title_label = QLabel("Tieu de:")
        title_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        right_layout.addWidget(title_label)

        self.title_input = CyberInput("Nhap tieu de...")
        right_layout.addWidget(self.title_input)

        # Content
        content_label2 = QLabel("Noi dung:")
        content_label2.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        right_layout.addWidget(content_label2)

        self.content_text = QTextEdit()
        self.content_text.setPlaceholderText("Nhap noi dung bai viet...")
        self.content_text.setStyleSheet(f"""
            QTextEdit {{
                background: {COLORS['bg_darker']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                padding: 8px;
            }}
        """)
        right_layout.addWidget(self.content_text, 1)

        # Image
        image_row = QHBoxLayout()
        image_label = QLabel("Hinh anh:")
        image_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        image_row.addWidget(image_label)

        self.image_input = CyberInput("Chon hinh...")
        self.image_input.setReadOnly(True)
        image_row.addWidget(self.image_input, 1)

        btn_image = CyberButton("📂", "secondary")
        btn_image.setFixedWidth(40)
        btn_image.clicked.connect(self._browse_image)
        image_row.addWidget(btn_image)

        right_layout.addLayout(image_row)

        # Buttons
        btn_row = QHBoxLayout()

        self.btn_save = CyberButton("Luu", "success", "💾")
        self.btn_save.clicked.connect(self._save_content)
        btn_row.addWidget(self.btn_save)

        self.btn_cancel = CyberButton("Huy", "secondary")
        self.btn_cancel.clicked.connect(self._clear_editor)
        btn_row.addWidget(self.btn_cancel)

        self.btn_delete = CyberButton("Xoa", "danger", "🗑️")
        self.btn_delete.clicked.connect(self._delete_content)
        btn_row.addWidget(self.btn_delete)

        right_layout.addLayout(btn_row)

        content.addWidget(right_card)
        layout.addLayout(content, 1)

    def _load_data(self):
        """Load categories"""
        self.categories = get_categories()
        self._render_categories()
        self._update_stats()
        self.log(f"Loaded {len(self.categories)} categories", "success")

    def _render_categories(self):
        """Render danh sach categories"""
        while self.cat_list_layout.count() > 0:
            item = self.cat_list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for cat in self.categories:
            cat_id = cat.get('id')
            name = cat.get('name', 'Unknown')
            count = get_contents_count(cat_id)

            row = QWidget()
            is_selected = cat_id == self.current_category_id
            bg_color = COLORS['neon_yellow'] if is_selected else COLORS['bg_card']
            row.setStyleSheet(f"background: {bg_color}; border-radius: 4px;")
            row.setFixedHeight(40)
            row.setCursor(Qt.PointingHandCursor)

            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(8, 4, 8, 4)
            row_layout.setSpacing(8)

            name_label = QLabel(name[:15])
            name_label.setStyleSheet(f"color: {COLORS['bg_dark'] if is_selected else COLORS['text_primary']}; font-size: 12px;")
            row_layout.addWidget(name_label, 1)

            count_label = QLabel(f"({count})")
            count_label.setStyleSheet(f"color: {COLORS['bg_darker'] if is_selected else COLORS['text_muted']}; font-size: 10px;")
            row_layout.addWidget(count_label)

            # Click handler
            row.mousePressEvent = lambda e, c=cat_id: self._select_category(c)

            # Delete button (not for default category)
            if cat_id != 1:
                btn_del = CyberButton("×", "danger")
                btn_del.setFixedSize(24, 24)
                btn_del.clicked.connect(lambda _, cid=cat_id: self._delete_category(cid))
                row_layout.addWidget(btn_del)

            self.cat_list_layout.addWidget(row)

        self.cat_list_layout.addStretch()

    def _select_category(self, cat_id):
        """Chon category"""
        self.current_category_id = cat_id
        self._render_categories()
        self._load_contents()

    def _load_contents(self):
        """Load contents theo category"""
        if not self.current_category_id:
            return

        self.contents = get_contents(self.current_category_id)
        self._render_contents()

    def _render_contents(self, search_text=None):
        """Render danh sach contents"""
        while self.content_list_layout.count() > 0:
            item = self.content_list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        contents_to_show = self.contents
        if search_text:
            search_lower = search_text.lower()
            contents_to_show = [c for c in self.contents
                               if search_lower in c.get('title', '').lower()
                               or search_lower in c.get('content', '').lower()]

        if not contents_to_show:
            empty = QLabel("Chua co noi dung nao")
            empty.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px;")
            empty.setAlignment(Qt.AlignCenter)
            self.content_list_layout.addWidget(empty)
        else:
            for content in contents_to_show:
                row = self._create_content_row(content)
                self.content_list_layout.addWidget(row)

        self.content_list_layout.addStretch()
        self._update_stats()

    def _create_content_row(self, content: Dict):
        """Tao row cho content"""
        row = QWidget()
        is_selected = content.get('id') == (self.editing_content.get('id') if self.editing_content else None)
        bg_color = COLORS['neon_cyan'] if is_selected else COLORS['bg_card']
        row.setStyleSheet(f"background: {bg_color}; border-radius: 4px;")
        row.setFixedHeight(60)
        row.setCursor(Qt.PointingHandCursor)

        row_layout = QVBoxLayout(row)
        row_layout.setContentsMargins(8, 4, 8, 4)
        row_layout.setSpacing(2)

        title = content.get('title', 'Khong co tieu de')
        title_label = QLabel(title[:40] + "..." if len(title) > 40 else title)
        title_label.setStyleSheet(f"color: {COLORS['bg_dark'] if is_selected else COLORS['text_primary']}; font-size: 12px; font-weight: bold;")
        row_layout.addWidget(title_label)

        preview = content.get('content', '')[:60] + "..." if len(content.get('content', '')) > 60 else content.get('content', '')
        preview_label = QLabel(preview)
        preview_label.setStyleSheet(f"color: {COLORS['bg_darker'] if is_selected else COLORS['text_muted']}; font-size: 10px;")
        row_layout.addWidget(preview_label)

        # Click handler
        row.mousePressEvent = lambda e, c=content: self._edit_content(c)

        return row

    def _filter_contents(self, text):
        self._render_contents(text)

    def _add_category(self):
        """Them category moi"""
        from PySide6.QtWidgets import QInputDialog

        name, ok = QInputDialog.getText(self, "Them danh muc", "Ten danh muc:")
        if ok and name:
            save_category({'name': name})
            self.log(f"Da them danh muc: {name}", "success")
            self._load_data()

    def _delete_category(self, cat_id):
        """Xoa category"""
        reply = QMessageBox.question(
            self, "Xac nhan",
            "Ban co chac muon xoa danh muc nay?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            delete_category(cat_id)
            self.log("Da xoa danh muc", "success")
            self.current_category_id = None
            self._load_data()

    def _add_content(self):
        """Them content moi"""
        if not self.current_category_id:
            QMessageBox.warning(self, "Loi", "Chua chon danh muc!")
            return

        self.editing_content = None
        self._clear_editor()

    def _edit_content(self, content: Dict):
        """Edit content"""
        self.editing_content = content
        self.title_input.setText(content.get('title', ''))
        self.content_text.setText(content.get('content', ''))
        self.image_input.setText(content.get('image_path', ''))
        self._render_contents()

    def _save_content(self):
        """Luu content"""
        if not self.current_category_id:
            QMessageBox.warning(self, "Loi", "Chua chon danh muc!")
            return

        title = self.title_input.text().strip()
        content_text = self.content_text.toPlainText().strip()

        if not title:
            QMessageBox.warning(self, "Loi", "Chua nhap tieu de!")
            return

        data = {
            'category_id': self.current_category_id,
            'title': title,
            'content': content_text,
            'image_path': self.image_input.text()
        }

        if self.editing_content:
            data['id'] = self.editing_content.get('id')

        save_content(data)
        self.log(f"Da luu noi dung: {title}", "success")

        self._clear_editor()
        self._load_contents()
        self._render_categories()

    def _delete_content(self):
        """Xoa content"""
        if not self.editing_content:
            return

        reply = QMessageBox.question(
            self, "Xac nhan",
            "Ban co chac muon xoa noi dung nay?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            delete_content(self.editing_content.get('id'))
            self.log("Da xoa noi dung", "success")
            self._clear_editor()
            self._load_contents()
            self._render_categories()

    def _clear_editor(self):
        """Clear editor"""
        self.editing_content = None
        self.title_input.clear()
        self.content_text.clear()
        self.image_input.clear()
        self._render_contents()

    def _browse_image(self):
        """Chon hinh anh"""
        path, _ = QFileDialog.getOpenFileName(
            self, "Chon hinh anh",
            "", "Images (*.png *.jpg *.jpeg *.gif)"
        )

        if path:
            self.image_input.setText(path)

    def _update_stats(self):
        self.stat_categories.set_value(str(len(self.categories)))
        self.stat_contents.set_value(str(len(self.contents)))
