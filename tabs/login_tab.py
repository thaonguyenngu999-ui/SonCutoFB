"""
FB Manager Pro - Login Tab
Login Facebook accounts
"""

import customtkinter as ctk
from .base_tab import BaseTab
from config import COLORS
from widgets import CyberFrame, CyberButton, CyberEntry, CyberComboBox


class LoginTab(BaseTab):
    """Facebook login tab"""
    
    TAB_ID = "login"
    TAB_TITLE = "Login FB"
    TAB_SUBTITLE = "Đăng nhập tài khoản Facebook"
    TAB_COLOR = "green"
    
    def build_content(self):
        """Build login tab content"""
        # Instructions card
        card = CyberFrame(self.content, glow_color=COLORS["neon_green"])
        card.pack(fill="x", pady=(0, 16))
        
        instructions = ctk.CTkLabel(
            card,
            text="📋 Hướng dẫn:\n\n"
                 "1. Chọn Profile muốn đăng nhập\n"
                 "2. Chọn phương thức: Cookie hoặc Email/Password\n"
                 "3. Nhập thông tin đăng nhập\n"
                 "4. Click 'Đăng nhập' để bắt đầu",
            font=("Rajdhani", 14),
            text_color=COLORS["text_secondary"],
            justify="left",
            anchor="w"
        )
        instructions.pack(fill="x", padx=20, pady=20)
        
        # Form card
        form_card = CyberFrame(self.content)
        form_card.pack(fill="x", pady=(0, 16))
        
        form_content = ctk.CTkFrame(form_card, fg_color="transparent")
        form_content.pack(fill="x", padx=20, pady=20)
        
        # Profile selection
        label1 = ctk.CTkLabel(
            form_content,
            text="PROFILE",
            font=("Orbitron", 10, "bold"),
            text_color=COLORS["neon_green"]
        )
        label1.pack(anchor="w", pady=(0, 4))
        
        self.profile_combo = CyberComboBox(
            form_content,
            values=["Chọn profile..."],
            width=400
        )
        self.profile_combo.pack(anchor="w", pady=(0, 16))
        
        # Method selection
        label2 = ctk.CTkLabel(
            form_content,
            text="PHƯƠNG THỨC",
            font=("Orbitron", 10, "bold"),
            text_color=COLORS["neon_green"]
        )
        label2.pack(anchor="w", pady=(0, 4))
        
        self.method_combo = CyberComboBox(
            form_content,
            values=["Cookie", "Email/Password", "2FA"],
            width=400
        )
        self.method_combo.pack(anchor="w", pady=(0, 16))
        self.method_combo.set("Cookie")
        
        # Cookie input
        label3 = ctk.CTkLabel(
            form_content,
            text="COOKIE / THÔNG TIN",
            font=("Orbitron", 10, "bold"),
            text_color=COLORS["neon_green"]
        )
        label3.pack(anchor="w", pady=(0, 4))
        
        self.cookie_entry = ctk.CTkTextbox(
            form_content,
            height=120,
            fg_color=COLORS["bg_darker"],
            border_color=COLORS["border"],
            border_width=1,
            text_color=COLORS["text_primary"],
            font=("Share Tech Mono", 12)
        )
        self.cookie_entry.pack(fill="x", pady=(0, 16))
        
        # Buttons
        btn_frame = ctk.CTkFrame(form_content, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        self.btn_login = CyberButton(
            btn_frame,
            text="ĐĂNG NHẬP",
            icon="🔐",
            variant="success",
            command=self._do_login
        )
        self.btn_login.pack(side="left", padx=(0, 12))
        
        self.btn_verify = CyberButton(
            btn_frame,
            text="KIỂM TRA",
            icon="✓",
            variant="primary",
            command=self._verify_login
        )
        self.btn_verify.pack(side="left")
    
    def _do_login(self):
        """Perform login"""
        self.log("Starting login process...", "info")
    
    def _verify_login(self):
        """Verify login status"""
        self.log("Checking login status...", "info")
