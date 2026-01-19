"""
FB Manager Pro - Posts Tab
Posts history and tracking
"""

import customtkinter as ctk
from .base_tab import BaseTab
from config import COLORS
from widgets import CyberFrame, CyberButton, CyberStatCard


class PostsTab(BaseTab):
    """Posts history tab"""
    
    TAB_ID = "posts"
    TAB_TITLE = "Posts"
    TAB_SUBTITLE = "Theo dõi lịch sử bài đăng"
    TAB_COLOR = "green"
    
    def build_content(self):
        """Build posts tab"""
        # Stats
        stats_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 20))
        stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="stat")
        
        self.stat_total = CyberStatCard(stats_frame, label="TỔNG BÀI", value="0", color="green")
        self.stat_total.grid(row=0, column=0, padx=8, sticky="nsew")
        
        self.stat_success = CyberStatCard(stats_frame, label="THÀNH CÔNG", value="0", color="cyan")
        self.stat_success.grid(row=0, column=1, padx=8, sticky="nsew")
        
        self.stat_pending = CyberStatCard(stats_frame, label="CHỜ ĐĂNG", value="0", color="yellow")
        self.stat_pending.grid(row=0, column=2, padx=8, sticky="nsew")
        
        self.stat_failed = CyberStatCard(stats_frame, label="THẤT BẠI", value="0", color="red")
        self.stat_failed.grid(row=0, column=3, padx=8, sticky="nsew")
        
        # Posts list
        card = CyberFrame(self.content)
        card.pack(fill="both", expand=True)
        
        header = ctk.CTkFrame(card, fg_color=COLORS["bg_hover"], corner_radius=0)
        header.pack(fill="x", padx=1, pady=1)
        
        bar = ctk.CTkFrame(header, fg_color=COLORS["neon_green"], width=4)
        bar.pack(side="left", fill="y", padx=12, pady=12)
        
        title = ctk.CTkLabel(
            header,
            text="LỊCH SỬ BÀI ĐĂNG",
            font=("Orbitron", 12, "bold")
        )
        title.pack(side="left", pady=12)
        
        # Toolbar
        btn_refresh = CyberButton(header, text="⟳", variant="ghost")
        btn_refresh.configure(width=40, height=28)
        btn_refresh.pack(side="right", padx=12)
        
        # Posts list
        posts_list = ctk.CTkScrollableFrame(card, fg_color="transparent")
        posts_list.pack(fill="both", expand=True, padx=1, pady=1)
        
        placeholder = ctk.CTkLabel(
            posts_list,
            text="📊 Chưa có bài đăng nào\n\nBài đăng sẽ hiển thị ở đây sau khi bạn đăng",
            font=("Rajdhani", 13),
            text_color=COLORS["text_muted"]
        )
        placeholder.pack(pady=60)
