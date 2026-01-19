"""
FB Manager Pro - Cyberpunk Widgets
V3 - BIGGER TEXT & CYBERPUNK BORDERS
"""

from PySide6.QtWidgets import (
    QWidget, QLabel, QFrame, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QTextEdit, QComboBox, QScrollArea, QGraphicsDropShadowEffect,
    QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor, QFont, QCursor, QPainter, QPen, QBrush, QLinearGradient, QPainterPath

import sys
sys.path.insert(0, str(__file__).rsplit('/', 2)[0])
from config import COLORS


class CyberFrame(QFrame):
    """Frame với CYBERPUNK corner cuts"""
    
    def __init__(self, glow_color: str = None, parent=None):
        super().__init__(parent)
        self.glow_color = QColor(glow_color) if glow_color else QColor(COLORS['neon_cyan'])
        self.corner_size = 12
        self.setAttribute(Qt.WA_StyledBackground, True)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        w, h = self.width(), self.height()
        cs = self.corner_size
        
        # Path với corner cuts
        path = QPainterPath()
        path.moveTo(cs, 0)
        path.lineTo(w - cs, 0)
        path.lineTo(w, cs)
        path.lineTo(w, h - cs)
        path.lineTo(w - cs, h)
        path.lineTo(cs, h)
        path.lineTo(0, h - cs)
        path.lineTo(0, cs)
        path.closeSubpath()
        
        # Fill
        painter.fillPath(path, QColor(COLORS['bg_card']))
        
        # Border gradient
        gradient = QLinearGradient(0, 0, w, h)
        gradient.setColorAt(0, self.glow_color)
        gradient.setColorAt(0.5, QColor(self.glow_color.red(), self.glow_color.green(), self.glow_color.blue(), 100))
        gradient.setColorAt(1, self.glow_color)
        
        pen = QPen(QBrush(gradient), 2)
        painter.setPen(pen)
        painter.drawPath(path)
        
        # Corner accents
        painter.setPen(QPen(self.glow_color, 3))
        # Top-left
        painter.drawLine(0, cs, 0, cs + 15)
        painter.drawLine(cs, 0, cs + 15, 0)
        # Top-right  
        painter.drawLine(w, cs, w, cs + 15)
        painter.drawLine(w - cs, 0, w - cs - 15, 0)
        # Bottom-left
        painter.drawLine(0, h - cs, 0, h - cs - 15)
        painter.drawLine(cs, h, cs + 15, h)
        # Bottom-right
        painter.drawLine(w, h - cs, w, h - cs - 15)
        painter.drawLine(w - cs, h, w - cs - 15, h)


class CyberButton(QPushButton):
    """Button CYBERPUNK với glow"""
    
    def __init__(self, text: str, variant: str = "primary", icon: str = None, parent=None):
        display_text = f"{icon}  {text}" if icon else text
        super().__init__(display_text, parent)
        
        self.variant = variant
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setMinimumHeight(42)
        
        colors = {
            "primary": COLORS["neon_cyan"],
            "success": COLORS["neon_green"],
            "danger": COLORS["neon_red"],
            "warning": COLORS["neon_yellow"],
            "magenta": COLORS["neon_magenta"],
            "purple": COLORS["neon_purple"],
            "orange": COLORS["neon_orange"],
            "ghost": COLORS["text_muted"],
        }
        
        self.color = colors.get(variant, colors["primary"])
        self._apply_style()
        
        # Glow
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
                color: {self.color};
                padding: 12px 28px;
                font-weight: bold;
                font-size: 13px;
                letter-spacing: 2px;
            }}
            QPushButton:hover {{
                background: {self.color};
                color: #06060f;
            }}
            QPushButton:pressed {{
                background: {self.color}cc;
            }}
        """)
    
    def enterEvent(self, event):
        self.glow.setBlurRadius(25)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self.glow.setBlurRadius(0)
        super().leaveEvent(event)


class CyberInput(QLineEdit):
    """Input CYBERPUNK - BIGGER"""
    
    def __init__(self, placeholder: str = "", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(46)
        self.setStyleSheet(f"""
            QLineEdit {{
                background: {COLORS['bg_darker']};
                border: 2px solid {COLORS['border']};
                border-left: 4px solid {COLORS['neon_cyan']};
                padding: 12px 18px;
                color: {COLORS['text_primary']};
                font-size: 15px;
                font-family: 'Consolas', monospace;
            }}
            QLineEdit:focus {{
                border-color: {COLORS['neon_cyan']};
                background: {COLORS['bg_card']};
            }}
            QLineEdit::placeholder {{
                color: {COLORS['text_muted']};
            }}
        """)


class CyberComboBox(QComboBox):
    """Dropdown CYBERPUNK - BIGGER"""
    
    def __init__(self, items: list = None, parent=None):
        super().__init__(parent)
        if items:
            self.addItems(items)
        self.setMinimumHeight(46)
        
        self.setStyleSheet(f"""
            QComboBox {{
                background: {COLORS['bg_darker']};
                border: 2px solid {COLORS['border']};
                border-left: 4px solid {COLORS['neon_purple']};
                padding: 12px 18px;
                color: {COLORS['text_primary']};
                font-size: 14px;
                min-width: 180px;
            }}
            QComboBox:hover {{
                border-color: {COLORS['neon_cyan']};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 40px;
            }}
            QComboBox::down-arrow {{
                border-left: 7px solid transparent;
                border-right: 7px solid transparent;
                border-top: 9px solid {COLORS['neon_cyan']};
            }}
            QComboBox QAbstractItemView {{
                background: {COLORS['bg_card']};
                border: 2px solid {COLORS['border']};
                selection-background-color: {COLORS['bg_hover']};
                font-size: 14px;
                padding: 6px;
            }}
        """)


class CyberCard(QWidget):
    """Card với CYBERPUNK corner cuts và glow"""
    
    def __init__(self, glow_color: str = None, parent=None):
        super().__init__(parent)
        self.glow_color = QColor(glow_color) if glow_color else QColor(COLORS['neon_cyan'])
        self.corner_size = 15
        
        # Glow effect
        glow = QGraphicsDropShadowEffect(self)
        glow.setBlurRadius(20)
        glow.setColor(self.glow_color)
        glow.setOffset(0, 0)
        self.setGraphicsEffect(glow)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        w, h = self.width(), self.height()
        cs = self.corner_size
        
        # Path với corner cuts
        path = QPainterPath()
        path.moveTo(cs, 0)
        path.lineTo(w - cs, 0)
        path.lineTo(w, cs)
        path.lineTo(w, h - cs)
        path.lineTo(w - cs, h)
        path.lineTo(cs, h)
        path.lineTo(0, h - cs)
        path.lineTo(0, cs)
        path.closeSubpath()
        
        # Fill gradient
        gradient = QLinearGradient(0, 0, 0, h)
        gradient.setColorAt(0, QColor(COLORS['bg_card']))
        gradient.setColorAt(1, QColor(COLORS['bg_darker']))
        painter.fillPath(path, gradient)
        
        # Border
        pen = QPen(self.glow_color, 2)
        painter.setPen(pen)
        painter.drawPath(path)
        
        # Top accent line
        painter.setPen(QPen(self.glow_color, 4))
        painter.drawLine(cs + 5, 0, min(w // 3, 150), 0)


class CyberStatCard(QWidget):
    """Stat card CYBERPUNK - BIGGER"""
    
    def __init__(self, label: str, value: str, change: str = "", color: str = "cyan", parent=None):
        super().__init__(parent)
        
        self.neon_color = QColor(COLORS.get(f"neon_{color}", COLORS["neon_cyan"]))
        self.corner_size = 10
        
        # Glow
        glow = QGraphicsDropShadowEffect(self)
        glow.setBlurRadius(15)
        glow.setColor(self.neon_color)
        glow.setOffset(0, 0)
        self.setGraphicsEffect(glow)
        
        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 18, 22, 18)
        layout.setSpacing(6)
        
        # Label - BIGGER
        lbl = QLabel(label)
        lbl.setStyleSheet(f"""
            color: {COLORS['text_muted']}; 
            font-size: 12px; 
            font-weight: bold; 
            letter-spacing: 3px;
        """)
        layout.addWidget(lbl)
        
        # Value - BIGGER
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(f"""
            color: {self.neon_color.name()}; 
            font-size: 42px; 
            font-weight: bold;
        """)
        layout.addWidget(self.value_label)
        
        # Change
        if change:
            chg = QLabel(change)
            chg_color = COLORS['neon_green'] if '+' in change or '▲' in change else COLORS['text_secondary']
            chg.setStyleSheet(f"color: {chg_color}; font-size: 13px;")
            layout.addWidget(chg)
    
    def set_value(self, value: str):
        self.value_label.setText(value)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        w, h = self.width(), self.height()
        cs = self.corner_size
        
        # Path
        path = QPainterPath()
        path.moveTo(cs, 0)
        path.lineTo(w, 0)
        path.lineTo(w, h - cs)
        path.lineTo(w - cs, h)
        path.lineTo(0, h)
        path.lineTo(0, cs)
        path.closeSubpath()
        
        # Fill
        gradient = QLinearGradient(0, 0, w, h)
        gradient.setColorAt(0, QColor(COLORS['bg_card']))
        gradient.setColorAt(1, QColor(COLORS['bg_darker']))
        painter.fillPath(path, gradient)
        
        # Border
        painter.setPen(QPen(QColor(COLORS['border']), 2))
        painter.drawPath(path)
        
        # Left accent
        painter.setPen(QPen(self.neon_color, 4))
        painter.drawLine(0, cs + 5, 0, h - 5)


class CyberTitle(QWidget):
    """Title với GlitchText - CYBERPUNK"""
    
    def __init__(self, title: str, subtitle: str = "", color: str = "cyan", parent=None):
        super().__init__(parent)
        
        neon_color = COLORS.get(f"neon_{color}", COLORS["neon_cyan"])
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 20)
        
        title_row = QHBoxLayout()
        title_row.setSpacing(16)
        
        # Corner accent - BIGGER
        corner = QFrame()
        corner.setFixedSize(10, 50)
        corner.setStyleSheet(f"""
            background: qlineargradient(y1:0, y2:1, 
                stop:0 {neon_color}, stop:1 transparent);
        """)
        title_row.addWidget(corner)
        
        # Title container
        title_container = QVBoxLayout()
        title_container.setSpacing(4)
        
        # Top line - LONGER
        top_line = QFrame()
        top_line.setFixedHeight(3)
        top_line.setMaximumWidth(400)
        top_line.setStyleSheet(f"background: qlineargradient(x1:0, x2:1, stop:0 {neon_color}, stop:1 transparent);")
        title_container.addWidget(top_line)
        
        # Title với GlitchText - SIZE 26
        from .cyber_effects import GlitchText
        title_label = GlitchText(title.upper(), neon_color, size=26)
        title_label.setFixedHeight(44)
        title_container.addWidget(title_label)
        
        # Bottom line
        bottom_line = QFrame()
        bottom_line.setFixedHeight(3)
        bottom_line.setMaximumWidth(200)
        bottom_line.setStyleSheet(f"background: qlineargradient(x1:0, x2:1, stop:0 {neon_color}, stop:1 transparent);")
        title_container.addWidget(bottom_line)
        
        # Subtitle - BIGGER
        if subtitle:
            sub = QLabel(f"// {subtitle}")
            sub.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px; letter-spacing: 2px; margin-top: 6px;")
            title_container.addWidget(sub)
        
        title_row.addLayout(title_container)
        title_row.addStretch()
        
        layout.addLayout(title_row)


class NavItem(QPushButton):
    """Navigation item - BIGGER"""
    
    clicked_nav = Signal(str)
    
    def __init__(self, text: str, icon: str, tab_id: str, color: str = "cyan", parent=None):
        super().__init__(f"  {icon}    {text}", parent)
        
        self.tab_id = tab_id
        self.neon_color = COLORS.get(f"neon_{color}", COLORS["neon_cyan"])
        self.is_active = False
        
        self.setFixedHeight(50)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self._apply_style()
        
        self.clicked.connect(lambda: self.clicked_nav.emit(self.tab_id))
    
    def _apply_style(self):
        if self.is_active:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, x2:1, stop:0 {self.neon_color}50, stop:1 transparent);
                    border: none;
                    border-left: 4px solid {self.neon_color};
                    text-align: left;
                    padding-left: 16px;
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
                    text-align: left;
                    padding-left: 16px;
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
    """Terminal CYBERPUNK với corner cuts"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.corner_size = 10
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setStyleSheet(f"""
            QTextEdit {{
                background: transparent;
                border: none;
                color: {COLORS['text_primary']};
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 13px;
                line-height: 1.5;
            }}
        """)
        layout.addWidget(self.text_area)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        w, h = self.width(), self.height()
        cs = self.corner_size
        
        # Path
        path = QPainterPath()
        path.moveTo(cs, 0)
        path.lineTo(w - cs, 0)
        path.lineTo(w, cs)
        path.lineTo(w, h - cs)
        path.lineTo(w - cs, h)
        path.lineTo(cs, h)
        path.lineTo(0, h - cs)
        path.lineTo(0, cs)
        path.closeSubpath()
        
        # Fill
        painter.fillPath(path, QColor(COLORS['bg_darker']))
        
        # Border
        painter.setPen(QPen(QColor(COLORS['border']), 2))
        painter.drawPath(path)
        
        # Top accent
        painter.setPen(QPen(QColor(COLORS['neon_green']), 3))
        painter.drawLine(cs, 0, cs + 80, 0)
    
    def add_line(self, message: str, level: str = "info"):
        from datetime import datetime
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        
        colors = {
            "info": COLORS["neon_cyan"],
            "success": COLORS["neon_green"],
            "warning": COLORS["neon_yellow"],
            "error": COLORS["neon_red"],
        }
        icons = {"info": "▸", "success": "✓", "warning": "⚠", "error": "✗"}
        
        color = colors.get(level, colors["info"])
        icon = icons.get(level, "▸")
        
        html = f'<div style="margin: 4px 0; font-size: 13px;">'
        html += f'<span style="color:{COLORS["text_muted"]}">{timestamp}</span> '
        html += f'<span style="color:{color}; font-weight: bold;">{icon}</span> '
        html += f'<span style="color:{COLORS["text_primary"]}">{message}</span></div>'
        
        self.text_area.insertHtml(html)
        self.text_area.verticalScrollBar().setValue(self.text_area.verticalScrollBar().maximum())
    
    def clear(self):
        self.text_area.clear()
        self.add_line("Terminal cleared", "info")


class CyberTable(QTableWidget):
    """Table CYBERPUNK - BIGGER"""
    
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
                background: rgba(0, 240, 255, 0.2);
                border-left: 4px solid {COLORS['neon_cyan']};
            }}
            QTableWidget::item:hover {{
                background: {COLORS['bg_hover']};
            }}
            QHeaderView::section {{
                background: {COLORS['bg_darker']};
                color: {COLORS['neon_cyan']};
                padding: 14px;
                border: none;
                border-bottom: 3px solid {COLORS['neon_cyan']};
                font-weight: bold;
                font-size: 13px;
                letter-spacing: 2px;
            }}
        """)
        
        header = self.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        self.verticalHeader().setVisible(False)
        self.setShowGrid(False)
        self.setSelectionBehavior(QTableWidget.SelectRows)
