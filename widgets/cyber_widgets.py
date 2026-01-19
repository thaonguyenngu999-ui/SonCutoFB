"""
FB Manager Pro - Cyberpunk Widgets
🐱 CUTE CAT EDITION - Rounded & Soft 🐱
"""

from PySide6.QtWidgets import (
    QWidget, QLabel, QFrame, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QTextEdit, QComboBox, QScrollArea, QGraphicsDropShadowEffect,
    QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtGui import QColor, QFont, QCursor, QPainter, QPen, QBrush, QLinearGradient, QPainterPath

import sys
sys.path.insert(0, str(__file__).rsplit('/', 2)[0])
from config import COLORS


class CyberButton(QPushButton):
    """Button cute rounded với gradient glow 🐱"""
    
    def __init__(self, text: str, variant: str = "primary", icon: str = None, parent=None):
        display_text = f"{icon}  {text}" if icon else text
        super().__init__(display_text, parent)
        
        self.variant = variant
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setMinimumHeight(44)
        
        colors = {
            "primary": (COLORS["neon_pink"], COLORS["neon_purple"]),
            "success": (COLORS["neon_mint"], COLORS["neon_cyan"]),
            "danger": (COLORS["neon_coral"], COLORS["neon_pink"]),
            "warning": (COLORS["neon_yellow"], COLORS["neon_coral"]),
            "purple": (COLORS["neon_purple"], COLORS["neon_blue"]),
            "cyan": (COLORS["neon_cyan"], COLORS["neon_mint"]),
            "ghost": (COLORS["text_muted"], COLORS["text_muted"]),
        }
        
        self.color1, self.color2 = colors.get(variant, colors["primary"])
        self._apply_style()
        
        # Soft glow
        self.glow = QGraphicsDropShadowEffect(self)
        self.glow.setBlurRadius(0)
        self.glow.setColor(QColor(self.color1))
        self.glow.setOffset(0, 0)
        self.setGraphicsEffect(self.glow)
    
    def _apply_style(self):
        self.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: 2px solid {self.color1};
                border-radius: 14px;
                color: {self.color1};
                padding: 12px 28px;
                font-weight: bold;
                font-size: 13px;
                letter-spacing: 1px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, x2:1, stop:0 {self.color1}, stop:1 {self.color2});
                border-color: transparent;
                color: #0c0c18;
            }}
            QPushButton:pressed {{
                background: {self.color2};
            }}
        """)
    
    def enterEvent(self, event):
        self.glow.setBlurRadius(25)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self.glow.setBlurRadius(0)
        super().leaveEvent(event)


class CyberInput(QLineEdit):
    """Input cute rounded 🐱"""
    
    def __init__(self, placeholder: str = "", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(48)
        self.setStyleSheet(f"""
            QLineEdit {{
                background: {COLORS['bg_card']};
                border: 2px solid {COLORS['border']};
                border-radius: 14px;
                padding: 12px 20px;
                color: {COLORS['text_primary']};
                font-size: 15px;
            }}
            QLineEdit:focus {{
                border-color: {COLORS['neon_cyan']};
                background: {COLORS['bg_hover']};
            }}
            QLineEdit::placeholder {{
                color: {COLORS['text_muted']};
            }}
        """)


class CyberComboBox(QComboBox):
    """Dropdown cute rounded 🐱"""
    
    def __init__(self, items: list = None, parent=None):
        super().__init__(parent)
        if items:
            self.addItems(items)
        self.setMinimumHeight(48)
        
        self.setStyleSheet(f"""
            QComboBox {{
                background: {COLORS['bg_card']};
                border: 2px solid {COLORS['border']};
                border-radius: 14px;
                padding: 12px 20px;
                color: {COLORS['text_primary']};
                font-size: 14px;
                min-width: 180px;
            }}
            QComboBox:hover {{
                border-color: {COLORS['neon_purple']};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 40px;
            }}
            QComboBox::down-arrow {{
                border-left: 7px solid transparent;
                border-right: 7px solid transparent;
                border-top: 9px solid {COLORS['neon_purple']};
            }}
            QComboBox QAbstractItemView {{
                background: {COLORS['bg_card']};
                border: 2px solid {COLORS['border']};
                border-radius: 12px;
                selection-background-color: {COLORS['bg_hover']};
                font-size: 14px;
                padding: 8px;
            }}
        """)


class CyberCard(QWidget):
    """Card cute rounded với soft glow 🐱"""
    
    def __init__(self, glow_color: str = None, parent=None):
        super().__init__(parent)
        self.glow_color = QColor(glow_color) if glow_color else QColor(COLORS['neon_pink'])
        self.border_radius = 20
        
        # Soft glow effect
        glow = QGraphicsDropShadowEffect(self)
        glow.setBlurRadius(30)
        glow.setColor(QColor(self.glow_color.red(), self.glow_color.green(), self.glow_color.blue(), 80))
        glow.setOffset(0, 4)
        self.setGraphicsEffect(glow)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Rounded rect
        path = QPainterPath()
        path.addRoundedRect(1, 1, self.width()-2, self.height()-2, self.border_radius, self.border_radius)
        
        # Gradient fill
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(COLORS['bg_card']))
        gradient.setColorAt(1, QColor(COLORS['bg_darker']))
        painter.fillPath(path, gradient)
        
        # Gradient border
        border_gradient = QLinearGradient(0, 0, self.width(), self.height())
        border_gradient.setColorAt(0, self.glow_color)
        border_gradient.setColorAt(0.5, QColor(self.glow_color.red(), self.glow_color.green(), self.glow_color.blue(), 100))
        border_gradient.setColorAt(1, self.glow_color)
        
        painter.setPen(QPen(QBrush(border_gradient), 2))
        painter.drawPath(path)


class CyberStatCard(QWidget):
    """Stat card cute với gradient border 🐱"""
    
    def __init__(self, label: str, value: str, change: str = "", color: str = "pink", parent=None):
        super().__init__(parent)
        
        color_map = {
            "pink": (COLORS["neon_pink"], COLORS["neon_purple"]),
            "cyan": (COLORS["neon_cyan"], COLORS["neon_mint"]),
            "purple": (COLORS["neon_purple"], COLORS["neon_blue"]),
            "mint": (COLORS["neon_mint"], COLORS["neon_cyan"]),
            "green": (COLORS["neon_mint"], COLORS["neon_cyan"]),
            "yellow": (COLORS["neon_yellow"], COLORS["neon_coral"]),
            "coral": (COLORS["neon_coral"], COLORS["neon_pink"]),
        }
        
        self.color1, self.color2 = color_map.get(color, color_map["pink"])
        self.border_radius = 18
        
        # Soft glow
        glow = QGraphicsDropShadowEffect(self)
        glow.setBlurRadius(25)
        glow.setColor(QColor(self.color1))
        glow.setOffset(0, 3)
        self.setGraphicsEffect(glow)
        
        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(8)
        
        # Cat emoji + Label
        top_row = QHBoxLayout()
        cat = QLabel("😺")
        cat.setStyleSheet("font-size: 16px;")
        top_row.addWidget(cat)
        
        lbl = QLabel(label)
        lbl.setStyleSheet(f"""
            color: {COLORS['text_muted']}; 
            font-size: 12px; 
            font-weight: bold; 
            letter-spacing: 2px;
        """)
        top_row.addWidget(lbl)
        top_row.addStretch()
        layout.addLayout(top_row)
        
        # Value
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(f"""
            color: {self.color1}; 
            font-size: 40px; 
            font-weight: bold;
        """)
        layout.addWidget(self.value_label)
        
        # Change
        if change:
            chg = QLabel(change)
            chg_color = COLORS['neon_mint'] if '+' in change or '▲' in change else COLORS['text_secondary']
            chg.setStyleSheet(f"color: {chg_color}; font-size: 13px;")
            layout.addWidget(chg)
    
    def set_value(self, value: str):
        self.value_label.setText(value)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Rounded rect
        path = QPainterPath()
        path.addRoundedRect(1, 1, self.width()-2, self.height()-2, self.border_radius, self.border_radius)
        
        # Fill
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(COLORS['bg_card']))
        gradient.setColorAt(1, QColor(COLORS['bg_darker']))
        painter.fillPath(path, gradient)
        
        # Gradient border
        border_gradient = QLinearGradient(0, 0, self.width(), 0)
        border_gradient.setColorAt(0, QColor(self.color1))
        border_gradient.setColorAt(1, QColor(self.color2))
        
        painter.setPen(QPen(QBrush(border_gradient), 3))
        painter.drawPath(path)


class CyberTitle(QWidget):
    """Title với GlitchText + cat decorations 🐱"""
    
    def __init__(self, title: str, subtitle: str = "", color: str = "pink", parent=None):
        super().__init__(parent)
        
        color_map = {
            "pink": COLORS["neon_pink"],
            "cyan": COLORS["neon_cyan"],
            "purple": COLORS["neon_purple"],
            "mint": COLORS["neon_mint"],
            "green": COLORS["neon_mint"],
            "yellow": COLORS["neon_yellow"],
        }
        neon_color = color_map.get(color, COLORS["neon_pink"])
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 24)
        
        title_row = QHBoxLayout()
        title_row.setSpacing(12)
        
        # Cat decoration
        cat_left = QLabel("🐱")
        cat_left.setStyleSheet("font-size: 28px;")
        title_row.addWidget(cat_left)
        
        # Title container
        title_container = QVBoxLayout()
        title_container.setSpacing(6)
        
        # Sparkle line
        sparkle_line = QLabel("✦ ─────────────── ✦")
        sparkle_line.setStyleSheet(f"color: {neon_color}; font-size: 12px;")
        title_container.addWidget(sparkle_line)
        
        # Title với GlitchText
        from .cyber_effects import GlitchText
        title_label = GlitchText(title.upper(), neon_color, size=26)
        title_label.setFixedHeight(44)
        title_container.addWidget(title_label)
        
        # Bottom sparkle
        sparkle_line2 = QLabel("✦ ───────── ✦")
        sparkle_line2.setStyleSheet(f"color: {neon_color}; font-size: 10px;")
        title_container.addWidget(sparkle_line2)
        
        # Subtitle
        if subtitle:
            sub = QLabel(f"♡ {subtitle}")
            sub.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px; margin-top: 4px;")
            title_container.addWidget(sub)
        
        title_row.addLayout(title_container)
        title_row.addStretch()
        
        # Cat decoration right
        cat_right = QLabel("😸")
        cat_right.setStyleSheet("font-size: 24px;")
        title_row.addWidget(cat_right)
        
        layout.addLayout(title_row)


class NavItem(QPushButton):
    """Navigation item cute rounded 🐱"""
    
    clicked_nav = Signal(str)
    
    def __init__(self, text: str, icon: str, tab_id: str, color: str = "pink", parent=None):
        super().__init__(f"  {icon}    {text}", parent)
        
        self.tab_id = tab_id
        
        color_map = {
            "pink": COLORS["neon_pink"],
            "cyan": COLORS["neon_cyan"],
            "purple": COLORS["neon_purple"],
            "mint": COLORS["neon_mint"],
            "green": COLORS["neon_mint"],
            "yellow": COLORS["neon_yellow"],
            "coral": COLORS["neon_coral"],
            "blue": COLORS["neon_blue"],
        }
        self.neon_color = color_map.get(color, COLORS["neon_pink"])
        self.is_active = False
        
        self.setFixedHeight(52)
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
                    border-radius: 0 12px 12px 0;
                    text-align: left;
                    padding-left: 18px;
                    color: {self.neon_color};
                    font-weight: bold;
                    font-size: 15px;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    border: none;
                    border-left: 4px solid transparent;
                    border-radius: 0 12px 12px 0;
                    text-align: left;
                    padding-left: 18px;
                    color: {COLORS['text_secondary']};
                    font-weight: 600;
                    font-size: 15px;
                }}
                QPushButton:hover {{
                    background: {COLORS['bg_hover']};
                    border-left: 4px solid {COLORS['border_bright']};
                    color: {COLORS['text_primary']};
                }}
            """)
    
    def set_active(self, active: bool):
        self.is_active = active
        self._apply_style()


class CyberTerminal(QWidget):
    """Terminal cute rounded 🐱"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.border_radius = 16
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setStyleSheet(f"""
            QTextEdit {{
                background: transparent;
                border: none;
                color: {COLORS['text_primary']};
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 13px;
                line-height: 1.6;
            }}
        """)
        layout.addWidget(self.text_area)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Rounded rect
        path = QPainterPath()
        path.addRoundedRect(1, 1, self.width()-2, self.height()-2, self.border_radius, self.border_radius)
        
        # Fill
        painter.fillPath(path, QColor(COLORS['bg_darker']))
        
        # Border gradient
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor(COLORS['neon_mint']))
        gradient.setColorAt(1, QColor(COLORS['neon_cyan']))
        
        painter.setPen(QPen(QBrush(gradient), 2))
        painter.drawPath(path)
    
    def add_line(self, message: str, level: str = "info"):
        from datetime import datetime
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        
        colors = {
            "info": COLORS["neon_cyan"],
            "success": COLORS["neon_mint"],
            "warning": COLORS["neon_yellow"],
            "error": COLORS["neon_coral"],
        }
        icons = {"info": "▸", "success": "✓", "warning": "⚠", "error": "✗"}
        cats = {"info": "😺", "success": "😸", "warning": "🙀", "error": "😿"}
        
        color = colors.get(level, colors["info"])
        icon = icons.get(level, "▸")
        cat = cats.get(level, "😺")
        
        html = f'<div style="margin: 4px 0; font-size: 13px;">'
        html += f'<span style="color:{COLORS["text_muted"]}">{timestamp}</span> '
        html += f'<span>{cat}</span> '
        html += f'<span style="color:{color}; font-weight: bold;">{icon}</span> '
        html += f'<span style="color:{COLORS["text_primary"]}">{message}</span></div>'
        
        self.text_area.insertHtml(html)
        self.text_area.verticalScrollBar().setValue(self.text_area.verticalScrollBar().maximum())
    
    def clear(self):
        self.text_area.clear()
        self.add_line("Terminal cleared ~nyaa", "info")


class CyberTable(QTableWidget):
    """Table cute rounded 🐱"""
    
    def __init__(self, columns: list, parent=None):
        super().__init__(parent)
        
        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels([c.upper() for c in columns])
        
        self.setStyleSheet(f"""
            QTableWidget {{
                background: transparent;
                border: none;
                gridline-color: {COLORS['border']};
                font-size: 14px;
            }}
            QTableWidget::item {{
                padding: 14px;
                border-bottom: 1px solid {COLORS['border']};
                color: {COLORS['text_primary']};
            }}
            QTableWidget::item:selected {{
                background: rgba(255, 107, 157, 0.2);
                border-radius: 8px;
            }}
            QTableWidget::item:hover {{
                background: {COLORS['bg_hover']};
            }}
            QHeaderView::section {{
                background: qlineargradient(x1:0, x2:1, stop:0 {COLORS['neon_pink']}30, stop:1 {COLORS['neon_purple']}30);
                color: {COLORS['neon_cyan']};
                padding: 14px;
                border: none;
                border-bottom: 2px solid {COLORS['neon_cyan']};
                font-weight: bold;
                font-size: 12px;
                letter-spacing: 2px;
            }}
        """)
        
        header = self.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        self.verticalHeader().setVisible(False)
        self.setShowGrid(False)
        self.setSelectionBehavior(QTableWidget.SelectRows)
