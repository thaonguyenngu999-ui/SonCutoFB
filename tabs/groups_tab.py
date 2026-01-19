"""
FB Manager Pro - Groups Tab
Post to Facebook Groups
"""

import customtkinter as ctk
from .base_tab import BaseTab
from config import COLORS
from widgets import CyberFrame, CyberButton, CyberEntry, CyberComboBox, CyberStatCard


class GroupsTab(BaseTab):
    """Groups posting tab"""
    
    TAB_ID = "groups"
    TAB_TITLE = "Groups"
    TAB_SUBTITLE = "Đăng bài vào nhóm Facebook"
    TAB_COLOR = "orange"
    
    def build_content(self):
        """Build groups tab"""
        # Stats
        stats_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 20))
        stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="stat")
        
        self.stat_groups = CyberStatCard(stats_frame, label="NHÓM", value="0", color="orange")
        self.stat_groups.grid(row=0, column=0, padx=8, sticky="nsew")
        
        self.stat_posts = CyberStatCard(stats_frame, label="BÀI ĐĂNG", value="0", color="green")
        self.stat_posts.grid(row=0, column=1, padx=8, sticky="nsew")
        
        self.stat_scheduled = CyberStatCard(stats_frame, label="CHỜ ĐĂNG", value="0", color="cyan")
        self.stat_scheduled.grid(row=0, column=2, padx=8, sticky="nsew")
        
        self.stat_failed = CyberStatCard(stats_frame, label="LỖI", value="0", color="red")
        self.stat_failed.grid(row=0, column=3, padx=8, sticky="nsew")
        
        # Main card
        card = CyberFrame(self.content, glow_color=COLORS["neon_orange"])
        card.pack(fill="both", expand=True)
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(
            content,
            text="👥 ĐĂNG BÀI VÀO NHÓM",
            font=("Orbitron", 14, "bold"),
            text_color=COLORS["neon_orange"]
        )
        title.pack(anchor="w", pady=(0, 16))
        
        placeholder = ctk.CTkLabel(
            content,
            text="Tính năng đang phát triển...",
            font=("Rajdhani", 14),
            text_color=COLORS["text_muted"]
        )
        placeholder.pack(pady=40)
