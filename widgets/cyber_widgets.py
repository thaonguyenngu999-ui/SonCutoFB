"""
FB Manager Pro - Cyberpunk Widgets
PySide6 UI Components - FIXED VERSION
"""

from PySide6.QtWidgets import (
    QWidget, QLabel, QFrame, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QTextEdit, QComboBox, QScrollArea, QGraphicsDropShadowEffect,
    QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor, QFont, QCursor

import sys
sys.path.insert(0, str(__file__).rsplit('/', 2)[0])
from config import COLORS


class CyberButton(QPushButton):
    """Nút với hiệu ứng neon"""
    
    def __init__(self, text: str, variant: str = "primary", icon: str = None, parent=None):
        display_text = f"{icon}  {text}" if icon else text
        super().__init__(display_text, parent)
        
        self.variant = variant
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
        colors = {
            "primary": ("#00f0ff", "#0d0f20"),
            "success": ("#00ff66", "#0d0f20"),
            "danger": ("#ff003c", "#0d0f20"),
            "warning": ("#fcee0a", "#0d0f20"),
            "magenta": ("#ff00a8", "#0d0f20"),
            "purple": ("#bf00ff", "#0d0f20"),
            "orange": ("#ff6b00", "#0d0f20"),
            "ghost": ("#7a7aa0", "transparent"),
        }
        
        self.color, self.bg = colors.get(variant, colors["primary"])
        self._apply_style()
        
        # Glow effect
        self.glow = QGraphicsDropShadowEffect(self)
        self.glow.setBlurRadius(0)
        self.glow.setColor(QColor(self.color))
        self.glow.setOffset(0, 0)
        self.setGraphicsEffect(self.glow)
    
    def _apply_style(self):
        self.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: 2px solid {self.color};
                border-radius: 6px;
                color: {self.color};
                padding: 12px 24px;
                font-weight: bold;
                font-size: 12px;
                letter-spacing: 1px;
            }}
            QPushButton:hover {{
                background: {self.color};
                color: #0d0f20;
            }}
        """)
    
    def enterEvent(self, event):
        self.glow.setBlurRadius(25)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self.glow.setBlurRadius(0)
        super().leaveEvent(event)


class CyberInput(QLineEdit):
    """Input với style neon"""
    
    def __init__(self, placeholder: str = "", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setStyleSheet(f"""
            QLineEdit {{
                background: {COLORS['bg_darker']};
                border: 2px solid {COLORS['border']};
                border-radius: 8px;
                padding: 12px 16px;
                color: {COLORS['text_primary']};
                font-size: 13px;
                font-family: 'Consolas', 'Courier New', monospace;
            }}
            QLineEdit:focus {{
                border-color: {COLORS['neon_cyan']};
                background: {COLORS['bg_card']};
            }}
        """)


class CyberComboBox(QComboBox):
    """Dropdown với style neon"""
    
    def __init__(self, items: list = None, parent=None):
        super().__init__(parent)
        if items:
            self.addItems(items)
        
        self.setStyleSheet(f"""
            QComboBox {{
                background: {COLORS['bg_darker']};
                border: 2px solid {COLORS['border']};
                border-radius: 8px;
                padding: 10px 16px;
                color: {COLORS['text_primary']};
                font-size: 13px;
                min-width: 160px;
            }}
            QComboBox:hover {{
                border-color: {COLORS['neon_cyan']};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 35px;
            }}
            QComboBox::down-arrow {{
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 8px solid {COLORS['neon_cyan']};
            }}
            QComboBox QAbstractItemView {{
                background: {COLORS['bg_card']};
                border: 2px solid {COLORS['border']};
                selection-background-color: {COLORS['bg_hover']};
                font-size: 13px;
            }}
        """)


class CyberCard(QFrame):
    """Card container"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['bg_card']};
                border: 2px solid {COLORS['border']};
                border-radius: 12px;
            }}
        """)


class CyberStatCard(QFrame):
    """Stat card với border sáng"""
    
    def __init__(self, label: str, value: str, change: str = "", color: str = "cyan", parent=None):
        super().__init__(parent)
        
        neon_color = COLORS.get(f"neon_{color}", COLORS["neon_cyan"])
        
        self.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(26,28,56,0.9), stop:1 rgba(18,20,42,0.95));
                border: 2px solid {COLORS['border']};
                border-radius: 12px;
            }}
            QFrame:hover {{
                border-color: {neon_color}80;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Accent bar
        accent = QFrame()
        accent.setFixedHeight(4)
        accent.setStyleSheet(f"background: {neon_color}; border-radius: 0;")
        layout.addWidget(accent)
        
        # Content
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 16, 20, 16)
        
        # Label
        lbl = QLabel(label)
        lbl.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 10px; font-weight: bold; letter-spacing: 2px;")
        content_layout.addWidget(lbl)
        
        # Value
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(f"color: {neon_color}; font-size: 36px; font-weight: bold;")
        content_layout.addWidget(self.value_label)
        
        # Change
        if change:
            chg = QLabel(change)
            color_change = COLORS['neon_green'] if '+' in change or '▲' in change else COLORS['text_secondary']
            chg.setStyleSheet(f"color: {color_change}; font-size: 11px;")
            content_layout.addWidget(chg)
        
        layout.addWidget(content)
    
    def set_value(self, value: str):
        self.value_label.setText(value)


class CyberTitle(QWidget):
    """Title với glitch effect - FIXED SIZE"""
    
    def __init__(self, title: str, subtitle: str = "", color: str = "cyan", parent=None):
        super().__init__(parent)
        
        neon_color = COLORS.get(f"neon_{color}", COLORS["neon_cyan"])
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 20)
        
        title_row = QHBoxLayout()
        title_row.setSpacing(14)
        
        # Accent
        accent = QLabel("◢")
        accent.setStyleSheet(f"color: {neon_color}; font-size: 28px;")
        title_row.addWidget(accent)
        
        # Title container
        title_container = QVBoxLayout()
        title_container.setSpacing(4)
        
        # Top line
        top_line = QFrame()
        top_line.setFixedHeight(2)
        top_line.setStyleSheet(f"background: qlineargradient(x1:0, x2:1, stop:0 {neon_color}, stop:1 transparent);")
        title_container.addWidget(top_line)
        
        # Title - SỬ DỤNG GLITCHTEXT với size nhỏ hơn
        from .cyber_effects import GlitchText
        title_label = GlitchText(title.upper(), neon_color, size=24)
        title_label.setFixedHeight(40)
        title_container.addWidget(title_label)
        
        # Bottom line
        bottom_line = QFrame()
        bottom_line.setFixedHeight(2)
        bottom_line.setMaximumWidth(180)
        bottom_line.setStyleSheet(f"background: qlineargradient(x1:0, x2:1, stop:0 {neon_color}, stop:1 transparent);")
        title_container.addWidget(bottom_line)
        
        # Subtitle
        if subtitle:
            sub = QLabel(f"// {subtitle}")
            sub.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 11px; letter-spacing: 2px; margin-top: 6px;")
            title_container.addWidget(sub)
        
        title_row.addLayout(title_container)
        title_row.addStretch()
        
        layout.addLayout(title_row)


class NavItem(QPushButton):
    """Navigation item"""
    
    clicked_nav = Signal(str)
    
    def __init__(self, text: str, icon: str, tab_id: str, color: str = "cyan", parent=None):
        super().__init__(f"  {icon}   {text}", parent)
        
        self.tab_id = tab_id
        self.neon_color = COLORS.get(f"neon_{color}", COLORS["neon_cyan"])
        self.is_active = False
        
        self.setFixedHeight(44)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self._apply_style()
        
        self.clicked.connect(lambda: self.clicked_nav.emit(self.tab_id))
    
    def _apply_style(self):
        if self.is_active:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, x2:1, stop:0 {self.neon_color}40, stop:1 transparent);
                    border: none;
                    border-left: 4px solid {self.neon_color};
                    text-align: left;
                    padding-left: 16px;
                    color: {self.neon_color};
                    font-weight: bold;
                    font-size: 14px;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    border: none;
                    border-left: 4px solid transparent;
                    text-align: left;
                    padding-left: 16px;
                    color: {COLORS['text_secondary']};
                    font-weight: 600;
                    font-size: 14px;
                }}
                QPushButton:hover {{
                    background: {COLORS['bg_hover']};
                    color: {COLORS['text_primary']};
                }}
            """)
    
    def set_active(self, active: bool):
        self.is_active = active
        self._apply_style()


class CyberTerminal(QFrame):
    """Terminal log"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setStyleSheet(f"""
            QFrame {{
                background: rgba(10, 12, 25, 0.9);
                border: 2px solid {COLORS['border']};
                border-radius: 10px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setStyleSheet(f"""
            QTextEdit {{
                background: transparent;
                border: none;
                color: {COLORS['text_primary']};
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
            }}
        """)
        layout.addWidget(self.text_area)
    
    def add_line(self, message: str, level: str = "info"):
        from datetime import datetime
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        
        colors = {
            "info": COLORS["neon_cyan"],
            "success": COLORS["neon_green"],
            "warning": COLORS["neon_yellow"],
            "error": COLORS["neon_red"],
        }
        icons = {"info": "ℹ", "success": "✓", "warning": "⚠", "error": "✗"}
        
        color = colors.get(level, colors["info"])
        icon = icons.get(level, "ℹ")
        
        html = f'<div style="margin: 3px 0;"><span style="color:{COLORS["text_muted"]}">{timestamp}</span> '
        html += f'<span style="color:{color}; font-weight: bold;">{icon} {message}</span></div>'
        
        self.text_area.insertHtml(html)
        self.text_area.verticalScrollBar().setValue(self.text_area.verticalScrollBar().maximum())
    
    def clear(self):
        self.text_area.clear()
        self.add_line("Terminal cleared", "info")


class CyberTable(QTableWidget):
    """Table với border sáng"""
    
    def __init__(self, columns: list, parent=None):
        super().__init__(parent)
        
        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels([c.upper() for c in columns])
        
        self.setStyleSheet(f"""
            QTableWidget {{
                background: transparent;
                border: none;
                gridline-color: {COLORS['border']};
                font-size: 13px;
            }}
            QTableWidget::item {{
                padding: 12px;
                border-bottom: 1px solid {COLORS['border']};
                color: {COLORS['text_primary']};
            }}
            QTableWidget::item:selected {{
                background: rgba(0, 240, 255, 0.2);
            }}
            QTableWidget::item:hover {{
                background: {COLORS['bg_hover']};
            }}
            QHeaderView::section {{
                background: rgba(0, 240, 255, 0.1);
                color: {COLORS['neon_cyan']};
                padding: 12px;
                border: none;
                border-bottom: 2px solid {COLORS['border']};
                font-weight: bold;
                font-size: 11px;
                letter-spacing: 2px;
            }}
        """)
        
        header = self.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        self.verticalHeader().setVisible(False)
        self.setShowGrid(False)
        self.setSelectionBehavior(QTableWidget.SelectRows)
