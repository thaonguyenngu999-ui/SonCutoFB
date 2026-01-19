"""
FB Manager Pro - Scripts Tab
Automation scripts management
"""

import customtkinter as ctk
from .base_tab import BaseTab
from config import COLORS
from widgets import CyberFrame, CyberButton


class ScriptsTab(BaseTab):
    """Scripts management tab"""
    
    TAB_ID = "scripts"
    TAB_TITLE = "Scripts"
    TAB_SUBTITLE = "Quản lý kịch bản tự động hóa"
    TAB_COLOR = "cyan"
    
    def build_content(self):
        """Build scripts tab"""
        card = CyberFrame(self.content, glow_color=COLORS["neon_cyan"])
        card.pack(fill="both", expand=True)
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(
            content,
            text="📜 AUTOMATION SCRIPTS",
            font=("Orbitron", 14, "bold"),
            text_color=COLORS["neon_cyan"]
        )
        title.pack(anchor="w", pady=(0, 16))
        
        info = ctk.CTkLabel(
            content,
            text="Tạo và quản lý các kịch bản tự động hóa:\n\n"
                 "• Tự động đăng bài theo lịch\n"
                 "• Tự động like, comment\n"
                 "• Tự động scan pages/groups\n"
                 "• Và nhiều hơn nữa...",
            font=("Rajdhani", 14),
            text_color=COLORS["text_secondary"],
            justify="left"
        )
        info.pack(anchor="w", pady=(0, 20))
        
        btn = CyberButton(
            content,
            text="TẠO KỊCH BẢN MỚI",
            icon="➕",
            variant="primary"
        )
        btn.pack(anchor="w")
