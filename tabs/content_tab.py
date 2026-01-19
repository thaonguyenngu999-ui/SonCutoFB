"""
FB Manager Pro - Content Tab
Create and manage content templates
"""

import customtkinter as ctk
from .base_tab import BaseTab
from config import COLORS
from widgets import CyberFrame, CyberButton, CyberEntry


class ContentTab(BaseTab):
    """Content creation tab"""
    
    TAB_ID = "content"
    TAB_TITLE = "Content"
    TAB_SUBTITLE = "Soạn và quản lý nội dung"
    TAB_COLOR = "yellow"
    
    def build_content(self):
        """Build content tab"""
        # Two column layout
        container = ctk.CTkFrame(self.content, fg_color="transparent")
        container.pack(fill="both", expand=True)
        container.grid_columnconfigure(0, weight=2)
        container.grid_columnconfigure(1, weight=1)
        
        # Left - Editor
        left = CyberFrame(container, glow_color=COLORS["neon_yellow"])
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        
        left_content = ctk.CTkFrame(left, fg_color="transparent")
        left_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(
            left_content,
            text="✏️ SOẠN NỘI DUNG",
            font=("Orbitron", 14, "bold"),
            text_color=COLORS["neon_yellow"]
        )
        title.pack(anchor="w", pady=(0, 16))
        
        # Template name
        name_label = ctk.CTkLabel(
            left_content,
            text="TÊN MẪU",
            font=("Orbitron", 10, "bold"),
            text_color=COLORS["neon_yellow"]
        )
        name_label.pack(anchor="w", pady=(0, 4))
        
        self.name_entry = CyberEntry(left_content, placeholder="Tên template...")
        self.name_entry.pack(fill="x", pady=(0, 12))
        
        # Content editor
        content_label = ctk.CTkLabel(
            left_content,
            text="NỘI DUNG",
            font=("Orbitron", 10, "bold"),
            text_color=COLORS["neon_yellow"]
        )
        content_label.pack(anchor="w", pady=(0, 4))
        
        self.content_text = ctk.CTkTextbox(
            left_content,
            height=200,
            fg_color=COLORS["bg_darker"],
            border_color=COLORS["border"],
            border_width=1,
            font=("Rajdhani", 14)
        )
        self.content_text.pack(fill="both", expand=True, pady=(0, 12))
        
        # Variables info
        vars_info = ctk.CTkLabel(
            left_content,
            text="📌 Biến có thể dùng: {name}, {date}, {time}, {random}",
            font=("Share Tech Mono", 11),
            text_color=COLORS["text_muted"]
        )
        vars_info.pack(anchor="w", pady=(0, 12))
        
        # Hashtags
        tags_label = ctk.CTkLabel(
            left_content,
            text="HASHTAGS",
            font=("Orbitron", 10, "bold"),
            text_color=COLORS["neon_yellow"]
        )
        tags_label.pack(anchor="w", pady=(0, 4))
        
        self.tags_entry = CyberEntry(left_content, placeholder="#viral #trending")
        self.tags_entry.pack(fill="x", pady=(0, 16))
        
        # Buttons
        btn_frame = ctk.CTkFrame(left_content, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        self.btn_save = CyberButton(
            btn_frame,
            text="LƯU MẪU",
            icon="💾",
            variant="warning",
            command=self._save_template
        )
        self.btn_save.pack(side="left", padx=(0, 8))
        
        self.btn_clear = CyberButton(
            btn_frame,
            text="XÓA",
            icon="🗑️",
            variant="ghost",
            command=self._clear_form
        )
        self.btn_clear.pack(side="left")
        
        # Right - Templates list
        right = CyberFrame(container)
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        
        right_header = ctk.CTkFrame(right, fg_color=COLORS["bg_hover"], corner_radius=0)
        right_header.pack(fill="x", padx=1, pady=1)
        
        bar = ctk.CTkFrame(right_header, fg_color=COLORS["neon_yellow"], width=4)
        bar.pack(side="left", fill="y", padx=12, pady=12)
        
        header_title = ctk.CTkLabel(
            right_header,
            text="MẪU ĐÃ LƯU",
            font=("Orbitron", 12, "bold")
        )
        header_title.pack(side="left", pady=12)
        
        # Templates list
        self.templates_list = ctk.CTkScrollableFrame(right, fg_color="transparent")
        self.templates_list.pack(fill="both", expand=True, padx=1, pady=1)
        
        # Placeholder
        placeholder = ctk.CTkLabel(
            self.templates_list,
            text="📝 Chưa có mẫu nào\n\nTạo mẫu mới ở bên trái",
            font=("Rajdhani", 13),
            text_color=COLORS["text_muted"]
        )
        placeholder.pack(pady=60)
    
    def _save_template(self):
        """Save content template"""
        name = self.name_entry.get()
        if not name:
            self.log("Please enter template name", "warning")
            return
        
        content = self.content_text.get("1.0", "end-1c")
        tags = self.tags_entry.get()
        
        self.log(f"Saved template: {name}", "success")
    
    def _clear_form(self):
        """Clear the form"""
        self.name_entry.delete(0, "end")
        self.content_text.delete("1.0", "end")
        self.tags_entry.delete(0, "end")
        self.log("Form cleared", "info")
