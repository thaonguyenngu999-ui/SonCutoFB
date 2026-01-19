"""
FB Manager Pro - Profiles Tab
Manage Hidemium browser profiles
"""

import customtkinter as ctk
from typing import List, Dict
import threading

from .base_tab import BaseTab
from config import COLORS
from widgets import (
    CyberFrame, CyberButton, CyberEntry, 
    CyberComboBox, CyberStatCard, CyberBadge, CyberTable
)
from db import get_profiles, save_profile, sync_profiles, update_profile_status
from api_service import hidemium_api


class ProfilesTab(BaseTab):
    """Profiles management tab"""
    
    TAB_ID = "profiles"
    TAB_TITLE = "Profiles"
    TAB_SUBTITLE = "Quản lý tài khoản Hidemium Browser"
    TAB_COLOR = "cyan"
    
    def __init__(self, master, **kwargs):
        self.profiles: List[Dict] = []
        self.folders: List[str] = ["ALL FOLDERS"]
        super().__init__(master, **kwargs)
    
    def build_content(self):
        """Build profiles tab content"""
        # Stats row
        self.stats_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        self.stats_frame.pack(fill="x", pady=(0, 20))
        
        # Configure grid
        self.stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="stat")
        
        # Stat cards
        self.stat_total = CyberStatCard(
            self.stats_frame,
            label="TỔNG PROFILES",
            value="0",
            change="Loading...",
            color="cyan"
        )
        self.stat_total.grid(row=0, column=0, padx=8, sticky="nsew")
        
        self.stat_running = CyberStatCard(
            self.stats_frame,
            label="ĐANG CHẠY",
            value="0",
            change="● Active",
            color="green"
        )
        self.stat_running.grid(row=0, column=1, padx=8, sticky="nsew")
        
        self.stat_folders = CyberStatCard(
            self.stats_frame,
            label="FOLDERS",
            value="0",
            change="Categories",
            color="purple"
        )
        self.stat_folders.grid(row=0, column=2, padx=8, sticky="nsew")
        
        self.stat_scripts = CyberStatCard(
            self.stats_frame,
            label="SCRIPTS",
            value="0",
            change="Automation",
            color="yellow"
        )
        self.stat_scripts.grid(row=0, column=3, padx=8, sticky="nsew")
        
        # Toolbar
        self.toolbar = ctk.CTkFrame(self.content, fg_color="transparent")
        self.toolbar.pack(fill="x", pady=(0, 16))
        
        # Search
        self.search_entry = CyberEntry(
            self.toolbar,
            placeholder="🔍 SEARCH...",
            width=280
        )
        self.search_entry.pack(side="left")
        self.search_entry.bind("<KeyRelease>", self._on_search)
        
        # Folder filter
        self.folder_combo = CyberComboBox(
            self.toolbar,
            values=self.folders,
            width=160
        )
        self.folder_combo.pack(side="left", padx=12)
        self.folder_combo.set("ALL FOLDERS")
        self.folder_combo.configure(command=self._on_folder_change)
        
        # Spacer
        spacer = ctk.CTkFrame(self.toolbar, fg_color="transparent")
        spacer.pack(side="left", fill="x", expand=True)
        
        # Action buttons
        self.btn_refresh = CyberButton(
            self.toolbar,
            text="REFRESH",
            icon="⟳",
            variant="ghost",
            command=self._load_profiles
        )
        self.btn_refresh.pack(side="left", padx=4)
        
        self.btn_sync = CyberButton(
            self.toolbar,
            text="SYNC",
            icon="🔄",
            variant="primary",
            command=self._sync_from_hidemium
        )
        self.btn_sync.pack(side="left", padx=4)
        
        self.btn_create = CyberButton(
            self.toolbar,
            text="CREATE",
            icon="➕",
            variant="success",
            command=self._create_profile
        )
        self.btn_create.pack(side="left", padx=4)
        
        # Table card
        self.table_card = CyberFrame(self.content)
        self.table_card.pack(fill="both", expand=True)
        
        # Card header
        self.card_header = ctk.CTkFrame(self.table_card, fg_color=COLORS["bg_hover"], corner_radius=0)
        self.card_header.pack(fill="x", padx=1, pady=1)
        
        # Header bar
        header_bar = ctk.CTkFrame(self.card_header, fg_color=COLORS["neon_cyan"], width=4, corner_radius=2)
        header_bar.pack(side="left", fill="y", padx=(12, 0), pady=12)
        
        header_title = ctk.CTkLabel(
            self.card_header,
            text="PROFILE DATABASE",
            font=("Orbitron", 12, "bold"),
            text_color=COLORS["text_primary"]
        )
        header_title.pack(side="left", padx=12, pady=12)
        
        self.count_label = ctk.CTkLabel(
            self.card_header,
            text="[0]",
            font=("Orbitron", 12, "bold"),
            text_color=COLORS["neon_cyan"]
        )
        self.count_label.pack(side="left")
        
        # Table
        self.table = CyberTable(
            self.table_card,
            columns=[
                {"id": "checkbox", "text": "", "width": 40},
                {"id": "profile", "text": "Profile", "width": 250},
                {"id": "status", "text": "Status", "width": 120},
                {"id": "platform", "text": "Platform", "width": 100},
                {"id": "folder", "text": "Folder", "width": 120},
                {"id": "last", "text": "Last", "width": 80},
                {"id": "action", "text": "Action", "width": 100},
            ],
            fg_color="transparent"
        )
        self.table.pack(fill="both", expand=True, padx=1, pady=1)
        
        # Load initial data
        self._load_profiles()
    
    def _load_profiles(self):
        """Load profiles from database"""
        self.log("Loading profiles from database...")
        self.profiles = get_profiles()
        self._update_display()
        self.log(f"Loaded {len(self.profiles)} profiles", "success")
    
    def _update_display(self):
        """Update the table display"""
        self.table.clear()
        
        # Count stats
        total = len(self.profiles)
        running = len([p for p in self.profiles if p.get('status') == 'running'])
        folders = len(set(p.get('folder_name', 'Default') for p in self.profiles))
        
        # Update stat cards
        self.stat_total.update_value(str(total), f"▲ +{min(total, 12)} tuần này")
        self.stat_running.update_value(str(running))
        self.stat_folders.update_value(str(folders))
        self.count_label.configure(text=f"[{total}]")
        
        # Update folder dropdown
        folder_names = sorted(set(p.get('folder_name', 'Default') for p in self.profiles if p.get('folder_name')))
        self.folders = ["ALL FOLDERS"] + folder_names
        self.folder_combo.configure(values=self.folders)
        
        # Add rows
        for profile in self.profiles:
            self._add_profile_row(profile)
    
    def _add_profile_row(self, profile: Dict):
        """Add a profile row to table"""
        row_frame = ctk.CTkFrame(
            self.table.body,
            fg_color="transparent",
            corner_radius=0,
            height=56
        )
        row_frame.pack(fill="x", pady=1)
        row_frame.pack_propagate(False)
        
        # Checkbox
        checkbox = ctk.CTkCheckBox(
            row_frame,
            text="",
            width=40,
            checkbox_width=18,
            checkbox_height=18,
            fg_color=COLORS["neon_cyan"],
            hover_color=COLORS["neon_magenta"]
        )
        checkbox.pack(side="left", padx=(16, 8), pady=8)
        
        # Profile info
        profile_frame = ctk.CTkFrame(row_frame, fg_color="transparent", width=250)
        profile_frame.pack(side="left", padx=8)
        profile_frame.pack_propagate(False)
        
        # Avatar & info
        info_container = ctk.CTkFrame(profile_frame, fg_color="transparent")
        info_container.pack(fill="both", expand=True, pady=8)
        
        avatar = ctk.CTkLabel(
            info_container,
            text="🪟" if profile.get('platform') == 'windows' else "🍎",
            font=("Arial", 20),
            width=40
        )
        avatar.pack(side="left")
        
        name_frame = ctk.CTkFrame(info_container, fg_color="transparent")
        name_frame.pack(side="left", padx=8)
        
        name = ctk.CTkLabel(
            name_frame,
            text=profile.get('name', 'Unknown'),
            font=("Rajdhani", 14, "bold"),
            text_color=COLORS["text_primary"],
            anchor="w"
        )
        name.pack(anchor="w")
        
        uuid = ctk.CTkLabel(
            name_frame,
            text=profile.get('uuid', '')[:12] + "...",
            font=("Share Tech Mono", 10),
            text_color=COLORS["text_muted"],
            anchor="w"
        )
        uuid.pack(anchor="w")
        
        # Status badge
        status = profile.get('status', 'stopped')
        status_colors = {
            'running': ('RUNNING', 'green', True),
            'stopped': ('STOPPED', 'gray', False),
            'error': ('ERROR', 'red', False)
        }
        badge_text, badge_color, pulse = status_colors.get(status, status_colors['stopped'])
        
        if badge_color == 'gray':
            badge_color_val = COLORS["text_muted"]
        else:
            badge_color_val = COLORS.get(f"neon_{badge_color}", COLORS["text_muted"])
        
        status_badge = ctk.CTkLabel(
            row_frame,
            text=f"● {badge_text}",
            font=("Orbitron", 10, "bold"),
            text_color=badge_color_val,
            width=120
        )
        status_badge.pack(side="left", padx=8)
        
        # Platform
        platform = profile.get('platform', 'windows').upper()
        platform_colors = {'WINDOWS': 'cyan', 'MACOS': 'purple', 'LINUX': 'orange'}
        platform_label = ctk.CTkLabel(
            row_frame,
            text=platform[:6],
            font=("Orbitron", 10, "bold"),
            text_color=COLORS.get(f"neon_{platform_colors.get(platform, 'cyan')}", COLORS["neon_cyan"]),
            width=100
        )
        platform_label.pack(side="left", padx=8)
        
        # Folder
        folder = ctk.CTkLabel(
            row_frame,
            text=profile.get('folder_name', 'Default'),
            font=("Rajdhani", 13),
            text_color=COLORS["text_secondary"],
            width=120
        )
        folder.pack(side="left", padx=8)
        
        # Last active
        last = ctk.CTkLabel(
            row_frame,
            text="--",
            font=("Share Tech Mono", 11),
            text_color=COLORS["text_muted"],
            width=80
        )
        last.pack(side="left", padx=8)
        
        # Action button
        if status == 'running':
            action_btn = CyberButton(
                row_frame,
                text="STOP",
                variant="danger",
                command=lambda p=profile: self._stop_profile(p)
            )
        else:
            action_btn = CyberButton(
                row_frame,
                text="START",
                variant="success",
                command=lambda p=profile: self._start_profile(p)
            )
        action_btn.configure(height=28, width=80)
        action_btn.pack(side="left", padx=16)
        
        # Hover effect
        row_frame.bind("<Enter>", lambda e, f=row_frame: f.configure(fg_color=COLORS["bg_hover"]))
        row_frame.bind("<Leave>", lambda e, f=row_frame: f.configure(fg_color="transparent"))
        
        self.table.row_frames.append(row_frame)
    
    def _on_search(self, event):
        """Filter profiles by search text"""
        search_text = self.search_entry.get().lower()
        # Filter logic here
        self.log(f"Searching: {search_text}")
    
    def _on_folder_change(self, value):
        """Filter by folder"""
        self.log(f"Filter by folder: {value}")
    
    def _sync_from_hidemium(self):
        """Sync profiles from Hidemium API"""
        self.log("Syncing from Hidemium API...")
        
        def sync_task():
            result = hidemium_api.get_profiles()
            if result.get('success'):
                profiles = result.get('data', {}).get('data', [])
                if profiles:
                    # Transform API data to our format
                    for p in profiles:
                        save_profile({
                            'uuid': p.get('uuid') or p.get('id'),
                            'name': p.get('name'),
                            'folder_name': p.get('folder', {}).get('name') if p.get('folder') else None,
                            'platform': p.get('platform', 'windows'),
                            'status': 'running' if p.get('is_running') else 'stopped'
                        })
                    self.after(0, lambda: self.log(f"Synced {len(profiles)} profiles", "success"))
                    self.after(0, self._load_profiles)
                else:
                    self.after(0, lambda: self.log("No profiles found in Hidemium", "warning"))
            else:
                self.after(0, lambda: self.log(f"Sync failed: {result.get('error')}", "error"))
        
        threading.Thread(target=sync_task, daemon=True).start()
    
    def _start_profile(self, profile: Dict):
        """Start browser for profile"""
        uuid = profile.get('uuid')
        self.log(f"Starting browser: {profile.get('name')}")
        
        def start_task():
            result = hidemium_api.start_browser(uuid)
            if result.get('success'):
                update_profile_status(uuid, 'running')
                self.after(0, lambda: self.log(f"Browser started: {profile.get('name')}", "success"))
                self.after(0, self._load_profiles)
            else:
                self.after(0, lambda: self.log(f"Failed to start: {result.get('error')}", "error"))
        
        threading.Thread(target=start_task, daemon=True).start()
    
    def _stop_profile(self, profile: Dict):
        """Stop browser for profile"""
        uuid = profile.get('uuid')
        self.log(f"Stopping browser: {profile.get('name')}")
        
        def stop_task():
            result = hidemium_api.stop_browser(uuid)
            if result.get('success'):
                update_profile_status(uuid, 'stopped')
                self.after(0, lambda: self.log(f"Browser stopped: {profile.get('name')}", "success"))
                self.after(0, self._load_profiles)
            else:
                self.after(0, lambda: self.log(f"Failed to stop: {result.get('error')}", "error"))
        
        threading.Thread(target=stop_task, daemon=True).start()
    
    def _create_profile(self):
        """Open create profile dialog"""
        self.log("Create profile dialog...")
    
    def refresh(self):
        """Refresh tab data"""
        self._load_profiles()
