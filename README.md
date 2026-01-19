# FB Manager Pro - CYBERPUNK 2077 Edition

![Version](https://img.shields.io/badge/version-2.0.77-cyan)
![Python](https://img.shields.io/badge/python-3.9+-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-green)

> 🎮 **Phần mềm quản lý Facebook tích hợp Hidemium Browser với giao diện Cyberpunk 2077**

## ✨ Tính năng

### 👤 Profiles Management
- Quản lý profiles từ Hidemium Browser
- Start/Stop browser
- Sync từ Hidemium API

### 🔐 Login Facebook
- Đăng nhập bằng Cookie
- Đăng nhập bằng Email/Password
- Hỗ trợ 2FA

### 📄 Pages Management
- Scan pages từ tài khoản
- Tạo page mới
- Quản lý danh sách pages

### 🎬 Reels Upload
- Upload Reels lên Pages
- Lên lịch đăng
- Quản lý caption & hashtags

### ✏️ Content Management
- Soạn nội dung mẫu
- Template với biến động
- Quản lý hashtags

### 👥 Groups Posting
- Đăng bài vào nhiều nhóm
- Delay ngẫu nhiên
- Lên lịch đăng

### 📜 Automation Scripts
- Tạo kịch bản tự động
- Chạy theo lịch
- Monitoring

### 📊 Posts Tracking
- Theo dõi lịch sử đăng
- Thống kê thành công/thất bại
- Export báo cáo

## 🚀 Cài đặt

### Yêu cầu
- Python 3.9+
- Hidemium Browser

### Bước 1: Clone repository
```bash
git clone https://github.com/your-repo/fb-manager-pro.git
cd fb-manager-pro
```

### Bước 2: Cài dependencies
```bash
pip install -r requirements.txt
```

### Bước 3: Chạy ứng dụng
```bash
python main.py
```

## 🎨 Theme Colors

| Color | Hex | Usage |
|-------|-----|-------|
| Neon Cyan | `#00f0ff` | Primary accent |
| Neon Magenta | `#ff00a8` | Secondary accent |
| Neon Green | `#00ff66` | Success states |
| Neon Yellow | `#fcee0a` | Warnings |
| Neon Purple | `#bf00ff` | Special elements |
| Neon Orange | `#ff6b00` | Groups tab |
| Neon Red | `#ff003c` | Errors, danger |

## ⚙️ Cấu hình Hidemium

Mặc định kết nối tới: `http://127.0.0.1:52000`

Thay đổi trong `config.py`:
```python
API_CONFIG = {
    "hidemium_base_url": "http://127.0.0.1:52000",
    "timeout": 30,
}
```

## 📝 License

MIT License

---

**Made with 💜 in Vietnam | CYBERPUNK 2077 Style**
