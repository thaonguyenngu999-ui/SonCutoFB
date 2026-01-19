"""
FB Manager Pro - Base Tab
Base class for all tab content
"""

import customtkinter as ctk
from typing import Callable, Any
import sys

sys.path.insert(0, str(__file__).rsplit('/', 2)[0])
from config import COLORS
from widgets import CyberTitle, CyberFrame


class BaseTab(ctk.CTkFrame):
    """Base class for tab content"""
    
    # Override in subclasses
    TAB_ID = "base"
    TAB_TITLE = "Base Tab"
    TAB_SUBTITLE = "Base tab description"
    TAB_COLOR = "cyan"
    
    def __init__(self, master, log_callback: Callable = None, **kwargs):
        kwargs.setdefault("fg_color", "transparent")
        super().__init__(master, **kwargs)
        
        self.log_callback = log_callback
        
        # Create title
        self.title = CyberTitle(
            self,
            title=self.TAB_TITLE,
            subtitle=self.TAB_SUBTITLE,
            color=self.TAB_COLOR
        )
        self.title.pack(fill="x", padx=28, pady=(28, 0))
        
        # Content area
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=28, pady=16)
        
        # Build tab content
        self.build_content()
    
    def build_content(self):
        """Override in subclasses to build tab content"""
        pass
    
    def log(self, message: str, level: str = "info"):
        """Log a message to terminal"""
        if self.log_callback:
            self.log_callback(message, level)
        print(f"[{self.TAB_ID.upper()}] {message}")
    
    def refresh(self):
        """Refresh tab data - override in subclasses"""
        pass
