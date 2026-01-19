"""
FB Manager Pro - Window Manager
Manage browser window positions and sizes
"""

import subprocess
import platform
from typing import Dict, Tuple, Optional


class WindowManager:
    """Manage browser window positioning"""
    
    def __init__(self):
        self.system = platform.system()
    
    def get_screen_size(self) -> Tuple[int, int]:
        """Get screen resolution"""
        if self.system == "Windows":
            try:
                import ctypes
                user32 = ctypes.windll.user32
                return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
            except:
                return 1920, 1080
        elif self.system == "Darwin":  # macOS
            try:
                output = subprocess.check_output(
                    ["system_profiler", "SPDisplaysDataType"],
                    text=True
                )
                # Parse resolution from output
                for line in output.split('\n'):
                    if "Resolution" in line:
                        parts = line.split(':')[1].strip().split('x')
                        return int(parts[0].strip()), int(parts[1].split()[0])
            except:
                return 1920, 1080
        else:  # Linux
            try:
                output = subprocess.check_output(["xrandr"], text=True)
                for line in output.split('\n'):
                    if '*' in line:  # Current resolution
                        res = line.split()[0].split('x')
                        return int(res[0]), int(res[1])
            except:
                return 1920, 1080
        
        return 1920, 1080
    
    def calculate_grid_position(
        self,
        index: int,
        total: int,
        screen_width: int = None,
        screen_height: int = None
    ) -> Dict[str, int]:
        """Calculate window position in a grid layout"""
        if screen_width is None or screen_height is None:
            screen_width, screen_height = self.get_screen_size()
        
        # Calculate grid dimensions
        if total <= 1:
            cols, rows = 1, 1
        elif total <= 2:
            cols, rows = 2, 1
        elif total <= 4:
            cols, rows = 2, 2
        elif total <= 6:
            cols, rows = 3, 2
        elif total <= 9:
            cols, rows = 3, 3
        else:
            cols, rows = 4, 3
        
        # Calculate cell size
        cell_width = screen_width // cols
        cell_height = screen_height // rows
        
        # Calculate position
        col = index % cols
        row = index // cols
        
        x = col * cell_width
        y = row * cell_height
        
        return {
            "x": x,
            "y": y,
            "width": cell_width,
            "height": cell_height
        }
    
    def move_window(self, window_id: str, x: int, y: int, width: int, height: int) -> bool:
        """Move and resize a window (platform specific)"""
        if self.system == "Windows":
            return self._move_window_windows(window_id, x, y, width, height)
        elif self.system == "Darwin":
            return self._move_window_macos(window_id, x, y, width, height)
        else:
            return self._move_window_linux(window_id, x, y, width, height)
    
    def _move_window_windows(self, window_id: str, x: int, y: int, width: int, height: int) -> bool:
        """Move window on Windows"""
        try:
            import ctypes
            user32 = ctypes.windll.user32
            hwnd = int(window_id)
            user32.MoveWindow(hwnd, x, y, width, height, True)
            return True
        except Exception as e:
            print(f"[WindowManager] Error moving window: {e}")
            return False
    
    def _move_window_macos(self, window_id: str, x: int, y: int, width: int, height: int) -> bool:
        """Move window on macOS using AppleScript"""
        try:
            script = f'''
            tell application "System Events"
                set frontApp to first application process whose frontmost is true
                tell frontApp
                    set position of window 1 to {{{x}, {y}}}
                    set size of window 1 to {{{width}, {height}}}
                end tell
            end tell
            '''
            subprocess.run(["osascript", "-e", script], check=True)
            return True
        except Exception as e:
            print(f"[WindowManager] Error moving window: {e}")
            return False
    
    def _move_window_linux(self, window_id: str, x: int, y: int, width: int, height: int) -> bool:
        """Move window on Linux using wmctrl or xdotool"""
        try:
            # Try wmctrl first
            subprocess.run([
                "wmctrl", "-i", "-r", window_id,
                "-e", f"0,{x},{y},{width},{height}"
            ], check=True)
            return True
        except:
            try:
                # Fallback to xdotool
                subprocess.run([
                    "xdotool", "windowmove", window_id, str(x), str(y)
                ], check=True)
                subprocess.run([
                    "xdotool", "windowsize", window_id, str(width), str(height)
                ], check=True)
                return True
            except Exception as e:
                print(f"[WindowManager] Error moving window: {e}")
                return False


# Global instance
window_manager = WindowManager()
