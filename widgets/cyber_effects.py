"""
FB Manager Pro - Cyberpunk Effects
Glitch, Scanlines, Neon Rain, Grid animations - ENHANCED VERSION
"""

from PySide6.QtWidgets import QWidget, QLabel, QFrame, QGraphicsOpacityEffect, QVBoxLayout
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, Property, QRect, QPoint
from PySide6.QtGui import QPainter, QColor, QPen, QLinearGradient, QFont, QBrush, QRadialGradient
import random
import math


class TearGlitchText(QWidget):
    """Text với hiệu ứng XÉ (tear/split) Cyberpunk - giống game"""
    
    def __init__(self, text: str, color: str = "#00f0ff", size: int = 48, parent=None):
        super().__init__(parent)
        self.base_text = text
        self.base_color = QColor(color)
        self.font_size = size
        self.glitch_colors = [QColor("#ff00a8"), QColor("#00f0ff"), QColor("#fcee0a"), QColor("#00ff66")]
        
        # Tear offset
        self.tear_top_offset = 0
        self.tear_bottom_offset = 0
        self.tear_active = False
        self.color_shift = 0
        
        # Set minimum size
        self.setMinimumHeight(size + 20)
        
        # Glitch timer
        self.glitch_timer = QTimer(self)
        self.glitch_timer.timeout.connect(self._random_glitch)
        self.glitch_timer.start(100)
        
        # Recovery timer
        self.recovery_timer = QTimer(self)
        self.recovery_timer.timeout.connect(self._recover)
        self.recovery_timer.setSingleShot(True)
        
        # Render timer
        self.render_timer = QTimer(self)
        self.render_timer.timeout.connect(self.update)
        self.render_timer.start(50)
    
    def _random_glitch(self):
        """Random trigger glitch"""
        if random.random() > 0.92 and not self.tear_active:
            self._do_tear_glitch()
    
    def _do_tear_glitch(self):
        """Thực hiện hiệu ứng xé"""
        self.tear_active = True
        
        glitch_type = random.randint(0, 4)
        
        if glitch_type <= 2:
            # Tear effect - phần trên và dưới xé ra
            self.tear_top_offset = random.randint(-8, 8)
            self.tear_bottom_offset = random.randint(-8, 8)
            self.color_shift = random.randint(0, 3)
        else:
            # Just color shift
            self.color_shift = random.randint(0, 3)
        
        self.recovery_timer.start(random.randint(80, 200))
    
    def _recover(self):
        """Khôi phục"""
        self.tear_active = False
        self.tear_top_offset = 0
        self.tear_bottom_offset = 0
        self.color_shift = 0
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        
        font = QFont("Orbitron", self.font_size)
        font.setBold(True)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 6)
        painter.setFont(font)
        
        text = self.base_text
        rect = self.rect()
        
        if self.tear_active and (self.tear_top_offset != 0 or self.tear_bottom_offset != 0):
            # Draw với tear effect
            half_height = rect.height() // 2
            
            # Phần trên - shifted và màu khác (cyan layer)
            painter.setClipRect(0, 0, rect.width(), half_height)
            painter.setPen(QColor(0, 240, 255, 180))  # Cyan ghost
            painter.drawText(rect.adjusted(self.tear_top_offset - 3, 0, 0, 0), 
                           Qt.AlignLeft | Qt.AlignVCenter, text)
            
            # Phần trên - main
            painter.setPen(self.base_color)
            painter.drawText(rect.adjusted(self.tear_top_offset, 0, 0, 0), 
                           Qt.AlignLeft | Qt.AlignVCenter, text)
            
            # Phần dưới - shifted và màu khác (magenta layer)
            painter.setClipRect(0, half_height, rect.width(), half_height)
            painter.setPen(QColor(255, 0, 168, 180))  # Magenta ghost
            painter.drawText(rect.adjusted(self.tear_bottom_offset + 3, 0, 0, 0), 
                           Qt.AlignLeft | Qt.AlignVCenter, text)
            
            # Phần dưới - main
            painter.setPen(self.base_color)
            painter.drawText(rect.adjusted(self.tear_bottom_offset, 0, 0, 0), 
                           Qt.AlignLeft | Qt.AlignVCenter, text)
            
            painter.setClipping(False)
            
            # Thêm noise lines
            for _ in range(3):
                y = random.randint(0, rect.height())
                painter.setPen(QPen(QColor(255, 255, 255, 100), 1))
                painter.drawLine(0, y, random.randint(50, 200), y)
        
        elif self.color_shift > 0:
            # Color shift only - RGB split
            # Red/Magenta layer (offset left)
            painter.setPen(QColor(255, 0, 168, 120))
            painter.drawText(rect.adjusted(-2, 0, 0, 0), Qt.AlignLeft | Qt.AlignVCenter, text)
            
            # Cyan layer (offset right)  
            painter.setPen(QColor(0, 240, 255, 120))
            painter.drawText(rect.adjusted(2, 0, 0, 0), Qt.AlignLeft | Qt.AlignVCenter, text)
            
            # Main text
            painter.setPen(self.base_color)
            painter.drawText(rect, Qt.AlignLeft | Qt.AlignVCenter, text)
        
        else:
            # Normal state với subtle glow
            # Glow layer
            glow_color = QColor(self.base_color)
            glow_color.setAlpha(50)
            painter.setPen(glow_color)
            painter.drawText(rect.adjusted(0, 2, 0, 0), Qt.AlignLeft | Qt.AlignVCenter, text)
            
            # Main text
            painter.setPen(self.base_color)
            painter.drawText(rect, Qt.AlignLeft | Qt.AlignVCenter, text)


class ScanlineOverlay(QWidget):
    """Hiệu ứng scanline CRT - ENHANCED với flicker"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.offset = 0
        self.flicker_intensity = 0
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)
        self.timer.start(30)
        
        self.flicker_timer = QTimer(self)
        self.flicker_timer.timeout.connect(self._random_flicker)
        self.flicker_timer.start(100)
    
    def _animate(self):
        self.offset = (self.offset + 2) % 20
        self.update()
    
    def _random_flicker(self):
        if random.random() > 0.95:
            self.flicker_intensity = random.randint(15, 30)
        else:
            self.flicker_intensity = max(0, self.flicker_intensity - 2)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        base_alpha = 8 + self.flicker_intensity
        pen = QPen(QColor(0, 240, 255, base_alpha))
        pen.setWidth(1)
        painter.setPen(pen)
        
        for y in range(self.offset, self.height(), 3):
            painter.drawLine(0, y, self.width(), y)


class NeonRain(QWidget):
    """Hiệu ứng mưa neon - ENHANCED"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.drops = []
        self.colors = [
            QColor(0, 240, 255, 80),
            QColor(255, 0, 168, 60),
            QColor(0, 255, 102, 70),
            QColor(191, 0, 255, 50),
        ]
        
        self._init_drops(50)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)
        self.timer.start(25)
    
    def _init_drops(self, count):
        for _ in range(count):
            self.drops.append({
                'x': random.randint(0, 2000),
                'y': random.randint(-500, 0),
                'speed': random.uniform(4, 12),
                'length': random.randint(40, 120),
                'width': random.uniform(1.5, 3),
                'color': random.choice(self.colors),
            })
    
    def _animate(self):
        for drop in self.drops:
            drop['y'] += drop['speed']
            if drop['y'] > self.height():
                drop['y'] = random.randint(-150, -50)
                drop['x'] = random.randint(0, self.width())
                drop['speed'] = random.uniform(4, 12)
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
    """Hiệu ứng grid background - ENHANCED"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.pulse = 0
        self.wave_offset = 0
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)
        self.timer.start(40)
    
    def _animate(self):
        self.pulse = (self.pulse + 3) % 360
        self.wave_offset = (self.wave_offset + 1) % 60
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        base_opacity = 18 + int(12 * math.sin(math.radians(self.pulse)))
        grid_size = 60
        
        for x in range(0, self.width() + grid_size, grid_size):
            wave = int(5 * math.sin(math.radians((x + self.wave_offset * 3) % 360)))
            opacity = base_opacity + int(10 * math.sin(math.radians((x * 2 + self.pulse) % 360)))
            pen = QPen(QColor(0, 240, 255, max(5, min(40, opacity))))
            pen.setWidth(1)
            painter.setPen(pen)
            painter.drawLine(x, 0, x + wave, self.height())
        
        for y in range(0, self.height() + grid_size, grid_size):
            opacity = base_opacity + int(8 * math.sin(math.radians((y * 2 + self.pulse) % 360)))
            pen = QPen(QColor(0, 240, 255, max(5, min(35, opacity))))
            pen.setWidth(1)
            painter.setPen(pen)
            painter.drawLine(0, y, self.width(), y)
        
        self._draw_corner_glow(painter)
    
    def _draw_corner_glow(self, painter):
        glow_size = 200
        alpha = int(25 + 15 * math.sin(math.radians(self.pulse)))
        
        gradient = QRadialGradient(0, 0, glow_size)
        gradient.setColorAt(0, QColor(0, 240, 255, alpha))
        gradient.setColorAt(1, QColor(0, 240, 255, 0))
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(-glow_size//2, -glow_size//2, glow_size, glow_size)
        
        gradient = QRadialGradient(self.width(), self.height(), glow_size)
        gradient.setColorAt(0, QColor(255, 0, 168, alpha))
        gradient.setColorAt(1, QColor(255, 0, 168, 0))
        painter.setBrush(gradient)
        painter.drawEllipse(self.width() - glow_size//2, self.height() - glow_size//2, glow_size, glow_size)


class PulsingDot(QWidget):
    """Đèn LED nhấp nháy"""
    
    def __init__(self, color: str = "#00ff66", parent=None):
        super().__init__(parent)
        self.setFixedSize(16, 16)
        self.color = QColor(color)
        self.pulse_value = 0
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)
        self.timer.start(40)
    
    def set_color(self, color: str):
        self.color = QColor(color)
    
    def _animate(self):
        self.pulse_value = (self.pulse_value + 8) % 360
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        glow = 0.5 + 0.5 * math.sin(math.radians(self.pulse_value))
        
        for i in range(3):
            glow_color = QColor(self.color)
            glow_color.setAlpha(int((80 - i * 25) * glow))
            painter.setBrush(glow_color)
            painter.setPen(Qt.NoPen)
            size = 16 - i * 3
            offset = i * 1.5
            painter.drawEllipse(int(offset), int(offset), int(size), int(size))
        
        painter.setBrush(self.color)
        painter.drawEllipse(5, 5, 6, 6)
        
        highlight = QColor(255, 255, 255, int(150 * glow))
        painter.setBrush(highlight)
        painter.drawEllipse(6, 6, 3, 3)


class NeonFlash(QWidget):
    """Random neon flash effect"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.flash_alpha = 0
        self.flash_color = QColor(0, 240, 255)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)
        self.timer.start(50)
        
        self.flash_timer = QTimer(self)
        self.flash_timer.timeout.connect(self._trigger_flash)
        self.flash_timer.start(3000)
    
    def _trigger_flash(self):
        if random.random() > 0.5:
            self.flash_alpha = random.randint(12, 25)
            colors = [QColor(0, 240, 255), QColor(255, 0, 168), QColor(0, 255, 102)]
            self.flash_color = random.choice(colors)
    
    def _animate(self):
        if self.flash_alpha > 0:
            self.flash_alpha = max(0, self.flash_alpha - 3)
            self.update()
    
    def paintEvent(self, event):
        if self.flash_alpha > 0:
            painter = QPainter(self)
            color = QColor(self.flash_color)
            color.setAlpha(self.flash_alpha)
            painter.fillRect(self.rect(), color)


# Alias for backward compatibility
GlitchText = TearGlitchText
