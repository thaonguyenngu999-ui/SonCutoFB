"""
FB Manager Pro - Reels Tab
Upload and schedule Reels to Pages
"""

import customtkinter as ctk
from tkinter import filedialog
from .base_tab import BaseTab
from config import COLORS
from widgets import CyberFrame, CyberButton, CyberEntry, CyberComboBox


class ReelsTab(BaseTab):
    """Reels upload tab"""
    
    TAB_ID = "reels"
    TAB_TITLE = "Reels"
    TAB_SUBTITLE = "Upload Reels lên Facebook Pages"
    TAB_COLOR = "magenta"
    
    def build_content(self):
        """Build reels tab content"""
        # Main container with 2 columns
        container = ctk.CTkFrame(self.content, fg_color="transparent")
        container.pack(fill="both", expand=True)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        
        # Left column - Upload form
        left = CyberFrame(container, glow_color=COLORS["neon_magenta"])
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        
        left_content = ctk.CTkFrame(left, fg_color="transparent")
        left_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Section title
        section_title = ctk.CTkLabel(
            left_content,
            text="📹 UPLOAD REELS",
            font=("Orbitron", 14, "bold"),
            text_color=COLORS["neon_magenta"]
        )
        section_title.pack(anchor="w", pady=(0, 16))
        
        # Profile selection
        label1 = ctk.CTkLabel(
            left_content,
            text="PROFILE",
            font=("Orbitron", 10, "bold"),
            text_color=COLORS["neon_magenta"]
        )
        label1.pack(anchor="w", pady=(0, 4))
        
        self.profile_combo = CyberComboBox(
            left_content,
            values=["Chọn profile..."]
        )
        self.profile_combo.pack(fill="x", pady=(0, 12))
        
        # Page selection
        label2 = ctk.CTkLabel(
            left_content,
            text="PAGE",
            font=("Orbitron", 10, "bold"),
            text_color=COLORS["neon_magenta"]
        )
        label2.pack(anchor="w", pady=(0, 4))
        
        self.page_combo = CyberComboBox(
            left_content,
            values=["Chọn page..."]
        )
        self.page_combo.pack(fill="x", pady=(0, 12))
        
        # Video file
        label3 = ctk.CTkLabel(
            left_content,
            text="VIDEO FILE",
            font=("Orbitron", 10, "bold"),
            text_color=COLORS["neon_magenta"]
        )
        label3.pack(anchor="w", pady=(0, 4))
        
        video_frame = ctk.CTkFrame(left_content, fg_color="transparent")
        video_frame.pack(fill="x", pady=(0, 12))
        
        self.video_entry = CyberEntry(video_frame, placeholder="Chọn video...")
        self.video_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        
        self.btn_browse = CyberButton(
            video_frame,
            text="📂",
            variant="magenta",
            command=self._browse_video
        )
        self.btn_browse.configure(width=40)
        self.btn_browse.pack(side="right")
        
        # Caption
        label4 = ctk.CTkLabel(
            left_content,
            text="CAPTION",
            font=("Orbitron", 10, "bold"),
            text_color=COLORS["neon_magenta"]
        )
        label4.pack(anchor="w", pady=(0, 4))
        
        self.caption_text = ctk.CTkTextbox(
            left_content,
            height=100,
            fg_color=COLORS["bg_darker"],
            border_color=COLORS["border"],
            border_width=1,
            font=("Rajdhani", 13)
        )
        self.caption_text.pack(fill="x", pady=(0, 12))
        
        # Hashtags
        label5 = ctk.CTkLabel(
            left_content,
            text="HASHTAGS",
            font=("Orbitron", 10, "bold"),
            text_color=COLORS["neon_magenta"]
        )
        label5.pack(anchor="w", pady=(0, 4))
        
        self.hashtags_entry = CyberEntry(
            left_content,
            placeholder="#reels #viral #trending"
        )
        self.hashtags_entry.pack(fill="x", pady=(0, 16))
        
        # Action buttons
        btn_frame = ctk.CTkFrame(left_content, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        self.btn_upload = CyberButton(
            btn_frame,
            text="ĐĂNG NGAY",
            icon="🚀",
            variant="magenta",
            command=self._upload_now
        )
        self.btn_upload.pack(side="left", padx=(0, 8))
        
        self.btn_schedule = CyberButton(
            btn_frame,
            text="LÊN LỊCH",
            icon="📅",
            variant="primary",
            command=self._schedule_upload
        )
        self.btn_schedule.pack(side="left")
        
        # Right column - Schedule list
        right = CyberFrame(container)
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        
        right_header = ctk.CTkFrame(right, fg_color=COLORS["bg_hover"], corner_radius=0)
        right_header.pack(fill="x", padx=1, pady=1)
        
        bar = ctk.CTkFrame(right_header, fg_color=COLORS["neon_cyan"], width=4)
        bar.pack(side="left", fill="y", padx=12, pady=12)
        
        title = ctk.CTkLabel(
            right_header,
            text="LỊCH ĐĂNG",
            font=("Orbitron", 12, "bold")
        )
        title.pack(side="left", pady=12)
        
        # Schedule list
        self.schedule_list = ctk.CTkScrollableFrame(right, fg_color="transparent")
        self.schedule_list.pack(fill="both", expand=True, padx=1, pady=1)
        
        # Placeholder
        placeholder = ctk.CTkLabel(
            self.schedule_list,
            text="📋 Chưa có lịch đăng nào\n\nClick 'Lên lịch' để thêm",
            font=("Rajdhani", 13),
            text_color=COLORS["text_muted"]
        )
        placeholder.pack(pady=60)
    
    def _browse_video(self):
        """Browse for video file"""
        filetypes = [
            ("Video files", "*.mp4 *.mov *.avi *.mkv"),
            ("All files", "*.*")
        ]
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.video_entry.delete(0, "end")
            self.video_entry.insert(0, filename)
            self.log(f"Selected video: {filename}", "info")
    
    def _upload_now(self):
        """Upload reel immediately"""
        video = self.video_entry.get()
        if not video:
            self.log("Please select a video file", "warning")
            return
        
        caption = self.caption_text.get("1.0", "end-1c")
        hashtags = self.hashtags_entry.get()
        
        self.log(f"Uploading reel: {video}", "info")
        # TODO: Implement actual upload via CDP
    
    def _schedule_upload(self):
        """Schedule reel upload"""
        video = self.video_entry.get()
        if not video:
            self.log("Please select a video file!", "warning")
            return
        
        self.log("Opening schedule dialog...", "info")
        # TODO: Implement schedule dialog
