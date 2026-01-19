"""
FB Manager Pro - Cyberpunk Effects
Glitch, Scanlines, Neon Rain, Grid animations - ENHANCED V2
"""

from PySide6.QtWidgets import QWidget, QLabel, QFrame, QGraphicsOpacityEffect, QVBoxLayout
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, Property, QRect, QPoint
from PySide6.QtGui import QPainter, QColor, QPen, QLinearGradient, QFont, QBrush, QRadialGradient
import random
import math


class TearGlitchText(QWidget):
    """Text với hiệu ứng XÉ (tear/split) Cyberpunk - MẠNH HƠN"""
    
    def __init__(self, text: str, color: str = "#00f0ff", size: int = 24, parent=None):
        super().__init__(parent)
        self.base_text = text
        self.base_color = QColor(color)
        self.font_size = size
        
        # Tear offset
        self.tear_top_offset = 0
        self.tear_bottom_offset = 0
        self.tear_active = False
        self.color_shift = 0
        self.scramble_chars = []
        self.show_cursor = True
        
        # Set size
        self.setMinimumHeight(size + 14)
        self.setMinimumWidth(len(text) * (size // 2 + 3) + 30)
        
        # Glitch timer - THƯỜNG XUYÊN HƠN
        self.glitch_timer = QTimer(self)
        self.glitch_timer.timeout.connect(self._random_glitch)
        self.glitch_timer.start(80)  # Nhanh hơn
        
        # Recovery timer
        self.recovery_timer = QTimer(self)
        self.recovery_timer.timeout.connect(self._recover)
        self.recovery_timer.setSingleShot(True)
        
        # Cursor blink
        self.cursor_timer = QTimer(self)
        self.cursor_timer.timeout.connect(self._blink_cursor)
        self.cursor_timer.start(500)
        
        # Render timer
        self.render_timer = QTimer(self)
        self.render_timer.timeout.connect(self.update)
        self.render_timer.start(40)
    
    def _blink_cursor(self):
        self.show_cursor = not self.show_cursor
    
    def _random_glitch(self):
        """Random trigger glitch - XẢY RA NHIỀU HƠN"""
        if random.random() > 0.85 and not self.tear_active:  # 15% chance mỗi 80ms
            self._do_tear_glitch()
    
    def _do_tear_glitch(self):
        """Thực hiện hiệu ứng xé - MẠNH HƠN"""
        self.tear_active = True
        
        glitch_type = random.randint(0, 5)
        
        if glitch_type <= 2:
            # Tear effect mạnh
            self.tear_top_offset = random.randint(-12, 12)
            self.tear_bottom_offset = random.randint(-12, 12)
            self.color_shift = random.randint(1, 4)
        elif glitch_type == 3:
            # Character scramble
            self.scramble_chars = random.sample(range(len(self.base_text)), 
                                                min(3, len(self.base_text)))
            self.color_shift = 2
        else:
            # Strong color shift
            self.color_shift = random.randint(2, 5)
        
        self.recovery_timer.start(random.randint(50, 180))
    
    def _recover(self):
        self.tear_active = False
        self.tear_top_offset = 0
        self.tear_bottom_offset = 0
        self.color_shift = 0
        self.scramble_chars = []
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        
        font = QFont("Segoe UI", self.font_size)
        font.setBold(True)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 3)
        painter.setFont(font)
        
        text = self.base_text
        
        # Scramble some characters
        if self.scramble_chars:
            chars = list(text)
            glitch_chars = "!@#$%^&*<>?/\\|█▓▒░"
            for i in self.scramble_chars:
                if i < len(chars):
                    chars[i] = random.choice(glitch_chars)
            text = ''.join(chars)
        
        rect = self.rect()
        
        if self.tear_active and (self.tear_top_offset != 0 or self.tear_bottom_offset != 0):
            half_height = rect.height() // 2
            
            # Phần trên - cyan ghost
            painter.setClipRect(0, 0, rect.width(), half_height)
            painter.setPen(QColor(0, 240, 255, 200))
            painter.drawText(rect.adjusted(self.tear_top_offset - 4, 0, 0, 0), 
                           Qt.AlignLeft | Qt.AlignVCenter, text)
            
            # Phần trên - main
            painter.setPen(self.base_color)
            painter.drawText(rect.adjusted(self.tear_top_offset, 0, 0, 0), 
                           Qt.AlignLeft | Qt.AlignVCenter, text)
            
            # Phần dưới - magenta ghost
            painter.setClipRect(0, half_height, rect.width(), half_height)
            painter.setPen(QColor(255, 0, 168, 200))
            painter.drawText(rect.adjusted(self.tear_bottom_offset + 4, 0, 0, 0), 
                           Qt.AlignLeft | Qt.AlignVCenter, text)
            
            # Phần dưới - main
            painter.setPen(self.base_color)
            painter.drawText(rect.adjusted(self.tear_bottom_offset, 0, 0, 0), 
                           Qt.AlignLeft | Qt.AlignVCenter, text)
            
            painter.setClipping(False)
            
            # Noise lines
            for _ in range(random.randint(2, 5)):
                y = random.randint(0, rect.height())
                painter.setPen(QPen(QColor(255, 255, 255, random.randint(80, 150)), 1))
                painter.drawLine(0, y, random.randint(50, 250), y)
        
        elif self.color_shift > 0:
            # RGB split mạnh
            offset = self.color_shift
            
            # Red/Magenta layer
            painter.setPen(QColor(255, 0, 168, 150))
            painter.drawText(rect.adjusted(-offset, 0, 0, 0), Qt.AlignLeft | Qt.AlignVCenter, text)
            
            # Cyan layer
            painter.setPen(QColor(0, 240, 255, 150))
            painter.drawText(rect.adjusted(offset, 0, 0, 0), Qt.AlignLeft | Qt.AlignVCenter, text)
            
            # Yellow layer (thêm)
            if offset > 2:
                painter.setPen(QColor(252, 238, 10, 100))
                painter.drawText(rect.adjusted(0, -1, 0, 0), Qt.AlignLeft | Qt.AlignVCenter, text)
            
            # Main text
            painter.setPen(self.base_color)
            painter.drawText(rect, Qt.AlignLeft | Qt.AlignVCenter, text)
        
        else:
            # Normal - subtle glow
            glow_color = QColor(self.base_color)
            glow_color.setAlpha(60)
            painter.setPen(glow_color)
            painter.drawText(rect.adjusted(0, 2, 0, 0), Qt.AlignLeft | Qt.AlignVCenter, text)
            painter.drawText(rect.adjusted(2, 0, 0, 0), Qt.AlignLeft | Qt.AlignVCenter, text)
            
            # Main text
            painter.setPen(self.base_color)
            painter.drawText(rect, Qt.AlignLeft | Qt.AlignVCenter, text)
        
        # Blinking cursor
        if self.show_cursor:
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.base_text)
            cursor_x = text_width + 8
            painter.setPen(QPen(self.base_color, 2))
            painter.drawLine(int(cursor_x), 8, int(cursor_x), rect.height() - 8)


class ScanlineOverlay(QWidget):
    """Hiệu ứng scanline CRT - chỉ ở main area"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.offset = 0
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)
        self.timer.start(35)
    
    def _animate(self):
        self.offset = (self.offset + 1) % 6
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Chỉ vẽ scanlines nhẹ
        pen = QPen(QColor(0, 240, 255, 8))
        pen.setWidth(1)
        painter.setPen(pen)
        
        for y in range(self.offset, self.height(), 3):
            painter.drawLine(0, y, self.width(), y)


class NeonRain(QWidget):
    """Hiệu ứng mưa neon - chỉ ở main area"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.drops = []
        self.colors = [
            QColor(0, 240, 255, 50),
            QColor(255, 0, 168, 35),
            QColor(0, 255, 102, 45),
            QColor(191, 0, 255, 30),
        ]
        
        self._init_drops(30)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)
        self.timer.start(30)
    
    def _init_drops(self, count):
        for _ in range(count):
            self.drops.append({
                'x': random.randint(0, 2000),
                'y': random.randint(-500, 0),
                'speed': random.uniform(2, 8),
                'length': random.randint(20, 80),
                'width': random.uniform(1, 2),
                'color': random.choice(self.colors),
            })
    
    def _animate(self):
        for drop in self.drops:
            drop['y'] += drop['speed']
            if drop['y'] > self.height():
                drop['y'] = random.randint(-100, -30)
                drop['x'] = random.randint(0, self.width())
                drop['speed'] = random.uniform(2, 8)
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        for drop in self.drops:
            gradient = QLinearGradient(
                drop['x'], drop['y'],
                drop['x'], drop['y'] + drop['length']
            )
            gradient.setColorAt(0, QColor(0, 0, 0, 0))
            gradient.setColorAt(0.3, drop['color'])
            gradient.setColorAt(0.7, drop['color'])
            gradient.setColorAt(1, QColor(0, 0, 0, 0))
            
            pen = QPen(QBrush(gradient), drop['width'])
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)
            painter.drawLine(
                int(drop['x']), int(drop['y']),
                int(drop['x']), int(drop['y'] + drop['length'])
            )


class CyberGrid(QWidget):
    """Hiệu ứng grid background - chỉ ở main area"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.pulse = 0
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)
        self.timer.start(50)
    
    def _animate(self):
        self.pulse = (self.pulse + 2) % 360
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        base_opacity = 12 + int(8 * math.sin(math.radians(self.pulse)))
        grid_size = 60
        
        # Vertical lines
        for x in range(0, self.width() + grid_size, grid_size):
            pen = QPen(QColor(0, 240, 255, base_opacity))
            pen.setWidth(1)
            painter.setPen(pen)
            painter.drawLine(x, 0, x, self.height())
        
        # Horizontal lines
        for y in range(0, self.height() + grid_size, grid_size):
            pen = QPen(QColor(0, 240, 255, base_opacity - 3))
            pen.setWidth(1)
            painter.setPen(pen)
            painter.drawLine(0, y, self.width(), y)
        
        # Corner glows
        self._draw_corner_glow(painter)
    
    def _draw_corner_glow(self, painter):
        glow_size = 150
        alpha = int(15 + 10 * math.sin(math.radians(self.pulse)))
        
        # Top-left cyan
        gradient = QRadialGradient(0, 0, glow_size)
        gradient.setColorAt(0, QColor(0, 240, 255, alpha))
        gradient.setColorAt(1, QColor(0, 240, 255, 0))
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(-glow_size//2, -glow_size//2, glow_size, glow_size)
        
        # Bottom-right magenta
        gradient = QRadialGradient(self.width(), self.height(), glow_size)
        gradient.setColorAt(0, QColor(255, 0, 168, alpha))
        gradient.setColorAt(1, QColor(255, 0, 168, 0))
        painter.setBrush(gradient)
        painter.drawEllipse(self.width() - glow_size//2, self.height() - glow_size//2, glow_size, glow_size)


class PulsingDot(QWidget):
    """Đèn LED nhấp nháy"""
    
    def __init__(self, color: str = "#00ff66", parent=None):
        super().__init__(parent)
        self.setFixedSize(12, 12)
        self.color = QColor(color)
        self.pulse_value = 0
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)
        self.timer.start(50)
    
    def set_color(self, color: str):
        self.color = QColor(color)
    
    def _animate(self):
        self.pulse_value = (self.pulse_value + 10) % 360
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        glow = 0.5 + 0.5 * math.sin(math.radians(self.pulse_value))
        
        # Glow layers
        for i in range(2):
            glow_color = QColor(self.color)
            glow_color.setAlpha(int((60 - i * 25) * glow))
            painter.setBrush(glow_color)
            painter.setPen(Qt.NoPen)
            size = 12 - i * 3
            offset = i * 1.5
            painter.drawEllipse(int(offset), int(offset), int(size), int(size))
        
        # Core
        painter.setBrush(self.color)
        painter.drawEllipse(3, 3, 6, 6)
        
        # Highlight
        highlight = QColor(255, 255, 255, int(120 * glow))
        painter.setBrush(highlight)
        painter.drawEllipse(4, 4, 3, 3)


class NeonFlash(QWidget):
    """Neon flash - TẮT HOÀN TOÀN để không giật"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # Không có timer, không có effect
    
    def paintEvent(self, event):
        # Không vẽ gì cả
        pass


# Alias
GlitchText = TearGlitchText
