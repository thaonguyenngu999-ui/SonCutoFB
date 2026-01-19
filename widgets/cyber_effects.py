"""
FB Manager Pro - Cyberpunk Effects
🐱 CUTE CAT Edition - Pastel Neon 🐱
"""

from PySide6.QtWidgets import QWidget, QLabel, QFrame, QGraphicsOpacityEffect, QVBoxLayout
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, Property, QRect, QPoint
from PySide6.QtGui import QPainter, QColor, QPen, QLinearGradient, QFont, QBrush, QRadialGradient
import random
import math


class TearGlitchText(QWidget):
    """Text với hiệu ứng Glitch cute 🐱"""
    
    def __init__(self, text: str, color: str = "#ff6b9d", size: int = 24, parent=None):
        super().__init__(parent)
        self.base_text = text
        self.base_color = QColor(color)
        self.font_size = size
        
        # Glitch state
        self.tear_top_offset = 0
        self.tear_bottom_offset = 0
        self.tear_active = False
        self.color_shift = 0
        self.scramble_chars = []
        self.show_cursor = True
        self.sparkle_pos = []
        
        # Size
        self.setMinimumHeight(size + 14)
        self.setMinimumWidth(len(text) * (size // 2 + 3) + 40)
        
        # Glitch timer
        self.glitch_timer = QTimer(self)
        self.glitch_timer.timeout.connect(self._random_glitch)
        self.glitch_timer.start(100)
        
        # Recovery timer
        self.recovery_timer = QTimer(self)
        self.recovery_timer.timeout.connect(self._recover)
        self.recovery_timer.setSingleShot(True)
        
        # Cursor blink
        self.cursor_timer = QTimer(self)
        self.cursor_timer.timeout.connect(self._blink_cursor)
        self.cursor_timer.start(500)
        
        # Sparkle timer
        self.sparkle_timer = QTimer(self)
        self.sparkle_timer.timeout.connect(self._update_sparkles)
        self.sparkle_timer.start(200)
        
        # Render timer
        self.render_timer = QTimer(self)
        self.render_timer.timeout.connect(self.update)
        self.render_timer.start(50)
    
    def _blink_cursor(self):
        self.show_cursor = not self.show_cursor
    
    def _update_sparkles(self):
        # Random sparkle positions
        self.sparkle_pos = []
        for _ in range(3):
            x = random.randint(0, self.width() - 10)
            y = random.randint(0, self.height() - 10)
            self.sparkle_pos.append((x, y))
    
    def _random_glitch(self):
        if random.random() > 0.88 and not self.tear_active:
            self._do_tear_glitch()
    
    def _do_tear_glitch(self):
        self.tear_active = True
        
        glitch_type = random.randint(0, 4)
        
        if glitch_type <= 1:
            # Soft tear
            self.tear_top_offset = random.randint(-8, 8)
            self.tear_bottom_offset = random.randint(-8, 8)
            self.color_shift = random.randint(1, 3)
        elif glitch_type == 2:
            # Character scramble with cute chars
            self.scramble_chars = random.sample(range(len(self.base_text)), 
                                                min(2, len(self.base_text)))
            self.color_shift = 2
        else:
            # Color shift
            self.color_shift = random.randint(2, 4)
        
        self.recovery_timer.start(random.randint(60, 150))
    
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
        font.setLetterSpacing(QFont.AbsoluteSpacing, 2)
        painter.setFont(font)
        
        text = self.base_text
        
        # Scramble with cute chars
        if self.scramble_chars:
            chars = list(text)
            cute_chars = "✦★♡♪☆✿❀"
            for i in self.scramble_chars:
                if i < len(chars):
                    chars[i] = random.choice(cute_chars)
            text = ''.join(chars)
        
        rect = self.rect()
        
        if self.tear_active and (self.tear_top_offset != 0 or self.tear_bottom_offset != 0):
            half_height = rect.height() // 2
            
            # Top - cyan ghost
            painter.setClipRect(0, 0, rect.width(), half_height)
            painter.setPen(QColor(107, 255, 242, 180))  # Cyan pastel
            painter.drawText(rect.adjusted(self.tear_top_offset - 3, 0, 0, 0), 
                           Qt.AlignLeft | Qt.AlignVCenter, text)
            
            # Top - main
            painter.setPen(self.base_color)
            painter.drawText(rect.adjusted(self.tear_top_offset, 0, 0, 0), 
                           Qt.AlignLeft | Qt.AlignVCenter, text)
            
            # Bottom - pink ghost
            painter.setClipRect(0, half_height, rect.width(), half_height)
            painter.setPen(QColor(184, 143, 255, 180))  # Purple pastel
            painter.drawText(rect.adjusted(self.tear_bottom_offset + 3, 0, 0, 0), 
                           Qt.AlignLeft | Qt.AlignVCenter, text)
            
            # Bottom - main
            painter.setPen(self.base_color)
            painter.drawText(rect.adjusted(self.tear_bottom_offset, 0, 0, 0), 
                           Qt.AlignLeft | Qt.AlignVCenter, text)
            
            painter.setClipping(False)
        
        elif self.color_shift > 0:
            # Pastel RGB split
            offset = self.color_shift
            
            # Purple layer
            painter.setPen(QColor(184, 143, 255, 130))
            painter.drawText(rect.adjusted(-offset, 0, 0, 0), Qt.AlignLeft | Qt.AlignVCenter, text)
            
            # Cyan layer
            painter.setPen(QColor(107, 255, 242, 130))
            painter.drawText(rect.adjusted(offset, 0, 0, 0), Qt.AlignLeft | Qt.AlignVCenter, text)
            
            # Main text
            painter.setPen(self.base_color)
            painter.drawText(rect, Qt.AlignLeft | Qt.AlignVCenter, text)
        
        else:
            # Normal - soft glow
            glow_color = QColor(self.base_color)
            glow_color.setAlpha(50)
            painter.setPen(glow_color)
            painter.drawText(rect.adjusted(0, 2, 0, 0), Qt.AlignLeft | Qt.AlignVCenter, text)
            painter.drawText(rect.adjusted(2, 0, 0, 0), Qt.AlignLeft | Qt.AlignVCenter, text)
            
            # Main text
            painter.setPen(self.base_color)
            painter.drawText(rect, Qt.AlignLeft | Qt.AlignVCenter, text)
        
        # Sparkles ✦
        sparkle_font = QFont("Segoe UI", 10)
        painter.setFont(sparkle_font)
        painter.setPen(QColor(255, 255, 255, 200))
        for x, y in self.sparkle_pos:
            painter.drawText(x, y + 10, "✦")
        
        # Blinking cursor
        if self.show_cursor:
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.base_text)
            cursor_x = text_width + 10
            painter.setPen(QPen(self.base_color, 2))
            painter.drawLine(int(cursor_x), 8, int(cursor_x), rect.height() - 8)


class ScanlineOverlay(QWidget):
    """Scanline effect - softer 🐱"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.offset = 0
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)
        self.timer.start(40)
    
    def _animate(self):
        self.offset = (self.offset + 1) % 6
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Soft pink scanlines
        pen = QPen(QColor(255, 107, 157, 5))
        pen.setWidth(1)
        painter.setPen(pen)
        
        for y in range(self.offset, self.height(), 4):
            painter.drawLine(0, y, self.width(), y)


class NeonRain(QWidget):
    """Neon rain - pastel colors 🐱"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.drops = []
        self.colors = [
            QColor(255, 107, 157, 40),  # Pink
            QColor(107, 255, 242, 35),  # Cyan
            QColor(184, 143, 255, 30),  # Purple
            QColor(107, 255, 184, 35),  # Mint
        ]
        
        self._init_drops(25)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)
        self.timer.start(35)
    
    def _init_drops(self, count):
        for _ in range(count):
            self.drops.append({
                'x': random.randint(0, 2000),
                'y': random.randint(-500, 0),
                'speed': random.uniform(1.5, 5),
                'length': random.randint(30, 100),
                'width': random.uniform(1.5, 2.5),
                'color': random.choice(self.colors),
            })
    
    def _animate(self):
        for drop in self.drops:
            drop['y'] += drop['speed']
            if drop['y'] > self.height():
                drop['y'] = random.randint(-100, -30)
                drop['x'] = random.randint(0, self.width())
                drop['speed'] = random.uniform(1.5, 5)
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
    """Grid background - pastel glow 🐱"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.pulse = 0
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)
        self.timer.start(60)
    
    def _animate(self):
        self.pulse = (self.pulse + 2) % 360
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        base_opacity = 10 + int(6 * math.sin(math.radians(self.pulse)))
        grid_size = 70
        
        # Vertical lines - pink
        for x in range(0, self.width() + grid_size, grid_size):
            pen = QPen(QColor(255, 107, 157, base_opacity))
            pen.setWidth(1)
            painter.setPen(pen)
            painter.drawLine(x, 0, x, self.height())
        
        # Horizontal lines - cyan
        for y in range(0, self.height() + grid_size, grid_size):
            pen = QPen(QColor(107, 255, 242, base_opacity - 2))
            pen.setWidth(1)
            painter.setPen(pen)
            painter.drawLine(0, y, self.width(), y)
        
        # Corner glows
        self._draw_corner_glow(painter)
    
    def _draw_corner_glow(self, painter):
        glow_size = 180
        alpha = int(12 + 8 * math.sin(math.radians(self.pulse)))
        
        # Top-left pink
        gradient = QRadialGradient(0, 0, glow_size)
        gradient.setColorAt(0, QColor(255, 107, 157, alpha))
        gradient.setColorAt(1, QColor(255, 107, 157, 0))
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(-glow_size//2, -glow_size//2, glow_size, glow_size)
        
        # Bottom-right purple
        gradient = QRadialGradient(self.width(), self.height(), glow_size)
        gradient.setColorAt(0, QColor(184, 143, 255, alpha))
        gradient.setColorAt(1, QColor(184, 143, 255, 0))
        painter.setBrush(gradient)
        painter.drawEllipse(self.width() - glow_size//2, self.height() - glow_size//2, glow_size, glow_size)
        
        # Top-right cyan
        gradient = QRadialGradient(self.width(), 0, glow_size * 0.7)
        gradient.setColorAt(0, QColor(107, 255, 242, alpha - 3))
        gradient.setColorAt(1, QColor(107, 255, 242, 0))
        painter.setBrush(gradient)
        painter.drawEllipse(int(self.width() - glow_size * 0.35), int(-glow_size * 0.35), int(glow_size * 0.7), int(glow_size * 0.7))


class PulsingDot(QWidget):
    """LED dot - cute 🐱"""
    
    def __init__(self, color: str = "#ff6b9d", parent=None):
        super().__init__(parent)
        self.setFixedSize(14, 14)
        self.color = QColor(color)
        self.pulse_value = 0
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)
        self.timer.start(50)
    
    def set_color(self, color: str):
        self.color = QColor(color)
    
    def _animate(self):
        self.pulse_value = (self.pulse_value + 8) % 360
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        glow = 0.5 + 0.5 * math.sin(math.radians(self.pulse_value))
        
        # Glow layers
        for i in range(2):
            glow_color = QColor(self.color)
            glow_color.setAlpha(int((50 - i * 20) * glow))
            painter.setBrush(glow_color)
            painter.setPen(Qt.NoPen)
            size = 14 - i * 3
            offset = i * 1.5
            painter.drawEllipse(int(offset), int(offset), int(size), int(size))
        
        # Core
        painter.setBrush(self.color)
        painter.drawEllipse(3, 3, 8, 8)
        
        # Highlight
        highlight = QColor(255, 255, 255, int(150 * glow))
        painter.setBrush(highlight)
        painter.drawEllipse(4, 4, 4, 4)


class NeonFlash(QWidget):
    """Neon flash - disabled for no jitter 🐱"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
    
    def paintEvent(self, event):
        pass


# Alias
GlitchText = TearGlitchText
