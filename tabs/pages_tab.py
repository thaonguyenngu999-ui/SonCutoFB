"""
FB Manager Pro - Pages Tab
Manage Facebook Pages
"""

import customtkinter as ctk
from .base_tab import BaseTab
from config import COLORS
from widgets import CyberFrame, CyberButton, CyberEntry, CyberComboBox, CyberStatCard
from db import get_pages, get_profiles


class PagesTab(BaseTab):
    """Pages management tab"""
    
    TAB_ID = "pages"
    TAB_TITLE = "Pages"
    TAB_SUBTITLE = "Quản lý Fanpages Facebook"
    TAB_COLOR = "purple"
    
    def build_content(self):
        """Build pages tab content"""
        # Stats row
        stats_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 20))
        stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="stat")
        
        self.stat_total = CyberStatCard(
            stats_frame,
            label="TỔNG PAGES",
            value="0",
            color="purple"
        )
        self.stat_total.grid(row=0, column=0, padx=8, sticky="nsew")
        
        self.stat_active = CyberStatCard(
            stats_frame,
            label="ACTIVE",
            value="0",
            color="green"
        )
        self.stat_active.grid(row=0, column=1, padx=8, sticky="nsew")
        
        self.stat_followers = CyberStatCard(
            stats_frame,
            label="FOLLOWERS",
            value="0",
            color="cyan"
        )
        self.stat_followers.grid(row=0, column=2, padx=8, sticky="nsew")
        
        self.stat_posts = CyberStatCard(
            stats_frame,
            label="POSTS",
            value="0",
            color="yellow"
        )
        self.stat_posts.grid(row=0, column=3, padx=8, sticky="nsew")
        
        # Toolbar
        toolbar = ctk.CTkFrame(self.content, fg_color="transparent")
        toolbar.pack(fill="x", pady=(0, 16))
        
        # Profile selector
        label = ctk.CTkLabel(
            toolbar,
            text="PROFILE:",
            font=("Orbitron", 10, "bold"),
            text_color=COLORS["neon_purple"]
        )
        label.pack(side="left", padx=(0, 8))
        
        self.profile_combo = CyberComboBox(
            toolbar,
            values=["Chọn profile..."],
            width=250
        )
        self.profile_combo.pack(side="left")
        
        # Spacer
        spacer = ctk.CTkFrame(toolbar, fg_color="transparent")
        spacer.pack(side="left", fill="x", expand=True)
        
        # Action buttons
        self.btn_scan = CyberButton(
            toolbar,
            text="SCAN PAGES",
            icon="🔍",
            variant="purple",
            command=self._scan_pages
        )
        self.btn_scan.pack(side="left", padx=4)
        
        self.btn_create = CyberButton(
            toolbar,
            text="TẠO PAGE",
            icon="➕",
            variant="success",
            command=self._create_page
        )
        self.btn_create.pack(side="left", padx=4)
        
        # Pages list
        self.pages_frame = CyberFrame(self.content)
        self.pages_frame.pack(fill="both", expand=True)
        
        # Header
        header = ctk.CTkFrame(self.pages_frame, fg_color=COLORS["bg_hover"], corner_radius=0)
        header.pack(fill="x", padx=1, pady=1)
        
        bar = ctk.CTkFrame(header, fg_color=COLORS["neon_purple"], width=4)
        bar.pack(side="left", fill="y", padx=12, pady=12)
        
        title = ctk.CTkLabel(
            header,
            text="PAGES DATABASE",
            font=("Orbitron", 12, "bold")
        )
        title.pack(side="left", pady=12)
        
        self.count_label = ctk.CTkLabel(
            header,
            text="[0]",
            font=("Orbitron", 12, "bold"),
            text_color=COLORS["neon_purple"]
        )
        self.count_label.pack(side="left", padx=8)
        
        # Scrollable list
        self.pages_list = ctk.CTkScrollableFrame(
            self.pages_frame,
            fg_color="transparent"
        )
        self.pages_list.pack(fill="both", expand=True, padx=1, pady=1)
        
        # Load data
        self._load_profiles()
        self._load_pages()
    
    def _load_profiles(self):
        """Load profiles for dropdown"""
        profiles = get_profiles()
        names = [f"{p['name']} ({p['uuid'][:8]})" for p in profiles]
        self.profile_combo.configure(values=["Chọn profile..."] + names)
        self.profiles_data = profiles
    
    def _load_pages(self):
        """Load pages from database"""
        pages = get_pages()
        
        # Clear current list
        for widget in self.pages_list.winfo_children():
            widget.destroy()
        
        # Update stats
        self.stat_total.update_value(str(len(pages)))
        self.count_label.configure(text=f"[{len(pages)}]")
        
        total_followers = sum(p.get('follower_count', 0) for p in pages)
        self.stat_followers.update_value(f"{total_followers:,}")
        
        # Add page rows
        for page in pages:
            self._add_page_row(page)
        
        if not pages:
            empty = ctk.CTkLabel(
                self.pages_list,
                text="Chưa có page nào. Chọn profile và bấm 'Scan Pages'",
                text_color=COLORS["text_muted"]
            )
            empty.pack(pady=40)
    
    def _add_page_row(self, page: dict):
        """Add a page row"""
        row = ctk.CTkFrame(self.pages_list, fg_color="transparent", height=60)
        row.pack(fill="x", pady=2)
        row.pack_propagate(False)
        
        # Checkbox
        cb = ctk.CTkCheckBox(
            row, text="", width=30,
            fg_color=COLORS["neon_purple"]
        )
        cb.pack(side="left", padx=16, pady=16)
        
        # Page info
        info = ctk.CTkFrame(row, fg_color="transparent")
        info.pack(side="left", fill="y", pady=8)
        
        name = ctk.CTkLabel(
            info,
            text=page.get('page_name', 'Unknown Page'),
            font=("Rajdhani", 14, "bold"),
            anchor="w"
        )
        name.pack(anchor="w")
        
        page_id = ctk.CTkLabel(
            info,
            text=f"ID: {page.get('page_id', 'N/A')}",
            font=("Share Tech Mono", 10),
            text_color=COLORS["text_muted"],
            anchor="w"
        )
        page_id.pack(anchor="w")
        
        # Spacer
        ctk.CTkFrame(row, fg_color="transparent").pack(side="left", fill="x", expand=True)
        
        # Followers
        followers = ctk.CTkLabel(
            row,
            text=f"👥 {page.get('follower_count', 0):,}",
            font=("Rajdhani", 13),
            text_color=COLORS["neon_cyan"]
        )
        followers.pack(side="left", padx=20)
        
        # Action buttons
        btn_view = CyberButton(row, text="VIEW", variant="ghost")
        btn_view.configure(height=28, width=60)
        btn_view.pack(side="left", padx=4)
        
        # Hover
        row.bind("<Enter>", lambda e: row.configure(fg_color=COLORS["bg_hover"]))
        row.bind("<Leave>", lambda e: row.configure(fg_color="transparent"))
    
    def _scan_pages(self):
        """Scan pages from Facebook"""
        self.log("Scanning pages...", "info")
        # TODO: Implement page scanning via CDP
    
    def _create_page(self):
        """Open create page dialog"""
        self.log("Opening create page dialog...", "info")
