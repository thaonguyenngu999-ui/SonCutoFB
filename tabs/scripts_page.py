"""
Scripts Page - Quan ly Scripts tu dong hoa
PySide6 version
"""
import threading
from typing import List, Dict
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QMessageBox, QTextEdit
)
from PySide6.QtCore import Qt, QTimer

from config import COLORS
from widgets import (
    CyberButton, CyberInput, CyberComboBox, CyberCard,
    CyberTitle, CyberStatCard, CyberCheckBox
)
from db import get_scripts, save_script, delete_script


class ScriptsPage(QWidget):
    """Scripts Page - Quan ly Scripts"""

    def __init__(self, log_func, parent=None):
        super().__init__(parent)
        self.log = log_func
        self.scripts: List[Dict] = []
        self.editing_script = None

        self._setup_ui()
        QTimer.singleShot(500, self._load_data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(10)

        # Top bar
        top_bar = QHBoxLayout()
        title = CyberTitle("Scripts", "Quan ly Scripts", "cyan")
        top_bar.addWidget(title)
        top_bar.addStretch()

        self.stat_total = CyberStatCard("SCRIPTS", "0", "📜", "cyan")
        self.stat_total.setFixedWidth(140)
        top_bar.addWidget(self.stat_total)

        self.stat_python = CyberStatCard("PYTHON", "0", "🐍", "mint")
        self.stat_python.setFixedWidth(140)
        top_bar.addWidget(self.stat_python)

        self.stat_hidemium = CyberStatCard("HIDEMIUM", "0", "🔧", "purple")
        self.stat_hidemium.setFixedWidth(140)
        top_bar.addWidget(self.stat_hidemium)

        layout.addLayout(top_bar)

        # Main content - 2 columns
        content = QHBoxLayout()
        content.setSpacing(12)

        # Left panel - Script list
        left_card = CyberCard(COLORS['neon_cyan'])
        left_card.setFixedWidth(320)
        left_layout = QVBoxLayout(left_card)
        left_layout.setContentsMargins(12, 12, 12, 12)

        # Header
        header_row = QHBoxLayout()
        header_label = QLabel("📜 Danh sach Scripts")
        header_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 14px; font-weight: bold;")
        header_row.addWidget(header_label)

        btn_add = CyberButton("+", "success")
        btn_add.setFixedSize(32, 32)
        btn_add.clicked.connect(self._add_script)
        header_row.addWidget(btn_add)

        left_layout.addLayout(header_row)

        # Filter
        filter_row = QHBoxLayout()
        filter_label = QLabel("Loai:")
        filter_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        filter_row.addWidget(filter_label)

        self.type_combo = CyberComboBox(["Tat ca", "Python", "Hidemium"])
        self.type_combo.currentIndexChanged.connect(self._filter_scripts)
        filter_row.addWidget(self.type_combo, 1)

        left_layout.addLayout(filter_row)

        # Search
        self.search_input = CyberInput("🔍 Tim kiem...")
        self.search_input.textChanged.connect(self._filter_scripts)
        left_layout.addWidget(self.search_input)

        # Script list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                background: {COLORS['bg_darker']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
            }}
        """)

        self.script_list_widget = QWidget()
        self.script_list_layout = QVBoxLayout(self.script_list_widget)
        self.script_list_layout.setContentsMargins(8, 8, 8, 8)
        self.script_list_layout.setSpacing(4)
        self.script_list_layout.addStretch()

        scroll.setWidget(self.script_list_widget)
        left_layout.addWidget(scroll, 1)

        content.addWidget(left_card)

        # Right panel - Editor
        right_card = CyberCard(COLORS['neon_mint'])
        right_layout = QVBoxLayout(right_card)
        right_layout.setContentsMargins(12, 12, 12, 12)

        # Header
        editor_label = QLabel("✏️ Chinh sua Script")
        editor_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 14px; font-weight: bold;")
        right_layout.addWidget(editor_label)

        # Name
        name_row = QHBoxLayout()
        name_label = QLabel("Ten:")
        name_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        name_label.setFixedWidth(80)
        name_row.addWidget(name_label)

        self.name_input = CyberInput("Nhap ten script...")
        name_row.addWidget(self.name_input, 1)

        right_layout.addLayout(name_row)

        # Type
        type_row = QHBoxLayout()
        type_label = QLabel("Loai:")
        type_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        type_label.setFixedWidth(80)
        type_row.addWidget(type_label)

        self.script_type_combo = CyberComboBox(["python", "hidemium"])
        self.script_type_combo.setFixedWidth(150)
        type_row.addWidget(self.script_type_combo)
        type_row.addStretch()

        right_layout.addLayout(type_row)

        # Description
        desc_label = QLabel("Mo ta:")
        desc_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        right_layout.addWidget(desc_label)

        self.desc_input = CyberInput("Mo ta ngan...")
        right_layout.addWidget(self.desc_input)

        # Hidemium Key (for hidemium scripts)
        key_row = QHBoxLayout()
        key_label = QLabel("Hidemium Key:")
        key_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        key_label.setFixedWidth(100)
        key_row.addWidget(key_label)

        self.key_input = CyberInput("Key tu Hidemium Scripts...")
        key_row.addWidget(self.key_input, 1)

        right_layout.addLayout(key_row)

        # Content
        content_label = QLabel("Noi dung script:")
        content_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        right_layout.addWidget(content_label)

        self.content_text = QTextEdit()
        self.content_text.setPlaceholderText("# Python script code here...")
        self.content_text.setStyleSheet(f"""
            QTextEdit {{
                background: {COLORS['bg_darker']};
                color: {COLORS['neon_mint']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                padding: 8px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
            }}
        """)
        right_layout.addWidget(self.content_text, 1)

        # Buttons
        btn_row = QHBoxLayout()

        self.btn_save = CyberButton("Luu", "success", "💾")
        self.btn_save.clicked.connect(self._save_script)
        btn_row.addWidget(self.btn_save)

        self.btn_run = CyberButton("Chay", "primary", "▶️")
        self.btn_run.clicked.connect(self._run_script)
        btn_row.addWidget(self.btn_run)

        self.btn_cancel = CyberButton("Huy", "secondary")
        self.btn_cancel.clicked.connect(self._clear_editor)
        btn_row.addWidget(self.btn_cancel)

        self.btn_delete = CyberButton("Xoa", "danger", "🗑️")
        self.btn_delete.clicked.connect(self._delete_script)
        btn_row.addWidget(self.btn_delete)

        right_layout.addLayout(btn_row)

        content.addWidget(right_card, 1)
        layout.addLayout(content, 1)

    def _load_data(self):
        """Load scripts"""
        self.scripts = get_scripts()
        self._render_scripts()
        self._update_stats()
        self.log(f"Loaded {len(self.scripts)} scripts", "success")

    def _render_scripts(self, filter_type=None, search_text=None):
        """Render danh sach scripts"""
        while self.script_list_layout.count() > 0:
            item = self.script_list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        scripts_to_show = self.scripts

        # Filter by type
        if filter_type and filter_type != "Tat ca":
            type_map = {"Python": "python", "Hidemium": "hidemium"}
            scripts_to_show = [s for s in scripts_to_show if s.get('type') == type_map.get(filter_type)]

        # Filter by search
        if search_text:
            search_lower = search_text.lower()
            scripts_to_show = [s for s in scripts_to_show
                              if search_lower in s.get('name', '').lower()
                              or search_lower in s.get('description', '').lower()]

        if not scripts_to_show:
            label = QLabel("Chua co script nao")
            label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px;")
            label.setAlignment(Qt.AlignCenter)
            self.script_list_layout.addWidget(label)
        else:
            for script in scripts_to_show:
                row = self._create_script_row(script)
                self.script_list_layout.addWidget(row)

        self.script_list_layout.addStretch()

    def _create_script_row(self, script: Dict):
        """Tao row cho script"""
        row = QWidget()
        is_selected = script.get('id') == (self.editing_script.get('id') if self.editing_script else None)
        bg_color = COLORS['neon_cyan'] if is_selected else COLORS['bg_card']
        row.setStyleSheet(f"background: {bg_color}; border-radius: 4px;")
        row.setFixedHeight(55)
        row.setCursor(Qt.PointingHandCursor)

        row_layout = QVBoxLayout(row)
        row_layout.setContentsMargins(8, 4, 8, 4)
        row_layout.setSpacing(2)

        # Name row
        name_row = QHBoxLayout()

        # Type icon
        type_icon = "🐍" if script.get('type') == 'python' else "🔧"
        icon_label = QLabel(type_icon)
        icon_label.setStyleSheet(f"font-size: 14px;")
        name_row.addWidget(icon_label)

        name = script.get('name', 'Khong ten')
        name_label = QLabel(name[:25] + "..." if len(name) > 25 else name)
        name_label.setStyleSheet(f"color: {COLORS['bg_dark'] if is_selected else COLORS['text_primary']}; font-size: 12px; font-weight: bold;")
        name_row.addWidget(name_label, 1)

        row_layout.addLayout(name_row)

        # Description
        desc = script.get('description', '')[:40]
        desc_label = QLabel(desc + "..." if len(script.get('description', '')) > 40 else desc)
        desc_label.setStyleSheet(f"color: {COLORS['bg_darker'] if is_selected else COLORS['text_muted']}; font-size: 10px;")
        row_layout.addWidget(desc_label)

        # Click handler
        row.mousePressEvent = lambda e, s=script: self._edit_script(s)

        return row

    def _filter_scripts(self):
        filter_type = self.type_combo.currentText()
        search_text = self.search_input.text()
        self._render_scripts(filter_type, search_text)

    def _add_script(self):
        """Them script moi"""
        self.editing_script = None
        self._clear_editor()

    def _edit_script(self, script: Dict):
        """Edit script"""
        self.editing_script = script
        self.name_input.setText(script.get('name', ''))
        self.desc_input.setText(script.get('description', ''))
        self.key_input.setText(script.get('hidemium_key', ''))
        self.content_text.setText(script.get('content', ''))

        # Set type
        script_type = script.get('type', 'python')
        idx = 0 if script_type == 'python' else 1
        self.script_type_combo.setCurrentIndex(idx)

        self._render_scripts()

    def _save_script(self):
        """Luu script"""
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Loi", "Chua nhap ten script!")
            return

        data = {
            'name': name,
            'description': self.desc_input.text(),
            'type': self.script_type_combo.currentText(),
            'hidemium_key': self.key_input.text(),
            'content': self.content_text.toPlainText()
        }

        if self.editing_script:
            data['id'] = self.editing_script.get('id')

        save_script(data)
        self.log(f"Da luu script: {name}", "success")

        self._clear_editor()
        self._load_data()

    def _run_script(self):
        """Chay script"""
        if not self.editing_script:
            QMessageBox.warning(self, "Loi", "Chua chon script nao!")
            return

        script_type = self.editing_script.get('type', 'python')
        name = self.editing_script.get('name', '')

        self.log(f"Dang chay script: {name}", "info")

        if script_type == 'hidemium':
            key = self.editing_script.get('hidemium_key', '')
            if key:
                self.log(f"Su dung Hidemium key: {key}", "info")
            else:
                QMessageBox.warning(self, "Loi", "Chua co Hidemium key!")
        else:
            # Python script
            content = self.editing_script.get('content', '')
            if content:
                self.log("Thuc thi Python script...", "info")
                # TODO: Execute Python script
            else:
                QMessageBox.warning(self, "Loi", "Script rong!")

    def _delete_script(self):
        """Xoa script"""
        if not self.editing_script:
            return

        reply = QMessageBox.question(
            self, "Xac nhan",
            "Ban co chac muon xoa script nay?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            delete_script(self.editing_script.get('id'))
            self.log("Da xoa script", "success")
            self._clear_editor()
            self._load_data()

    def _clear_editor(self):
        """Clear editor"""
        self.editing_script = None
        self.name_input.clear()
        self.desc_input.clear()
        self.key_input.clear()
        self.content_text.clear()
        self.script_type_combo.setCurrentIndex(0)
        self._render_scripts()

    def _update_stats(self):
        total = len(self.scripts)
        python_count = sum(1 for s in self.scripts if s.get('type') == 'python')
        hidemium_count = sum(1 for s in self.scripts if s.get('type') == 'hidemium')

        self.stat_total.set_value(str(total))
        self.stat_python.set_value(str(python_count))
        self.stat_hidemium.set_value(str(hidemium_count))
