# AutoRent Backend

Backend API cho ứng dụng cho thuê ô tô AutoRent. Được xây dựng bằng Django REST Framework với hỗ trợ JWT Authentication.

## 📋 Mục Lục

- [Yêu Cầu Hệ Thống](#yêu-cầu-hệ-thống)
- [Cài Đặt](#cài-đặt)
- [Cấu Hình](#cấu-hình)
- [Chạy Ứng Dụng](#chạy-ứng-dụng)
- [API Endpoints](#api-endpoints)
- [Cấu Trúc Dự Án](#cấu-trúc-dự-án)
- [Tính Năng](#tính-năng)

## 🔧 Yêu Cầu Hệ Thống

- Python 3.8+
- Django 6.0.5
- pip (Python package manager)

## 📦 Cài Đặt

### 1. Clone hoặc tải dự án

```bash
cd autorent_backend
```

### 2. Tạo và kích hoạt Virtual Environment

**Trên Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Trên macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Cài đặt Dependencies

```bash
pip install -r requirements.txt
```

Hoặc cài đặt các package cơ bản:

```bash
pip install Django==6.0.5
pip install djangorestframework
pip install django-cors-headers
pip install djangorestframework-simplejwt
```

## ⚙️ Cấu Hình

### 1. Tạo Database

```bash
python manage.py migrate
```

### 2. Tạo Super User (Admin)

```bash
python manage.py createsuperuser
```

### 3. Tạo Test User (Tùy Chọn)

```bash
python create_test_user.py
```

Thông tin đăng nhập test user mặc định:

- Email: `test@example.com`
- Password: `Test12345`

## 🚀 Chạy Ứng Dụng

### Development Server

```bash
python manage.py runserver
```

Server sẽ chạy tại: `http://localhost:8000/`

Admin panel: `http://localhost:8000/admin/`

## 📡 API Endpoints

### Authentication Endpoints

| Method | Endpoint         | Mô Tả             | Request                                | Response                        |
| ------ | ---------------- | ----------------- | -------------------------------------- | ------------------------------- |
| POST   | `/api/register/` | Đăng ký tài khoản | `{name, phone, email, password, cccd}` | `{success/error}`               |
| POST   | `/api/login/`    | Đăng nhập         | `{email, password}`                    | `{access_token, refresh_token}` |

### Ví dụ Request

**Đăng Ký:**

```json
{
  "name": "Nguyễn Văn A",
  "phone": "0912345678",
  "email": "user@example.com",
  "password": "SecurePass123",
  "cccd": "123456789012"
}
```

**Đăng Nhập:**

```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

## 📁 Cấu Trúc Dự Án

```
autorent_backend/
├── core/                    # Cấu hình chính Django
│   ├── settings.py         # Cài đặt Django
│   ├── urls.py             # URL routing chính
│   ├── asgi.py             # ASGI config
│   └── wsgi.py             # WSGI config
├── api/                     # Ứng dụng API chính
│   ├── models.py           # Database models
│   ├── views.py            # API views
│   ├── urls.py             # URL routing cho API
│   ├── admin.py            # Django admin config
│   ├── apps.py             # App config
│   ├── tests.py            # Unit tests
│   └── migrations/         # Database migrations
├── templates/              # HTML templates
│   └── index.html          # Trang chính
├── static/                 # Static files (CSS, JS, images)
├── manage.py               # Django management script
├── db.sqlite3              # Database (SQLite)
├── create_test_user.py     # Script tạo test user
└── README.md               # File này
```

## ✨ Tính Năng

- ✅ Đăng ký và Đăng nhập người dùng
- ✅ JWT Token Authentication
- ✅ CORS Support (hỗ trợ frontend từ các domain khác)
- ✅ REST API cho thao tác dữ liệu
- ✅ Admin panel để quản lý dữ liệu
- ✅ Validation đầu vào

## 🔐 Bảo Mật

**⚠️ Quan Trọng - Development Only:**

Hiện tại, dự án được cấu hình cho môi trường **development**. Trước khi deploy lên production:

1. **Đổi SECRET_KEY** trong `core/settings.py`
2. **Thiết lập DEBUG = False**
3. **Cấu hình ALLOWED_HOSTS**
4. **Sử dụng database production** (PostgreSQL, MySQL, v.v.)
5. **Cấu hình HTTPS**
6. **Thiết lập environment variables** cho các thông tin nhạy cảm

## 📝 Các Lệnh Hữu Ích

```bash
# Tạo migration cho models mới
python manage.py makemigrations

# Áp dụng migrations
python manage.py migrate

# Tạo superuser mới
python manage.py createsuperuser

# Chạy Django shell
python manage.py shell

# Chạy tests
python manage.py test

# Collect static files (cho production)
python manage.py collectstatic
```

## 🐛 Troubleshooting

### Lỗi: ModuleNotFoundError

**Giải pháp:** Đảm bảo virtual environment được kích hoạt và tất cả dependencies được cài đặt:

```bash
pip install -r requirements.txt
```

### Lỗi: Port 8000 đã được sử dụng

**Giải pháp:** Chạy trên port khác:

```bash
python manage.py runserver 8001
```

### Lỗi: Database migration

**Giải pháp:** Chạy migrations:

```bash
python manage.py migrate
```

## 📞 Liên Hệ & Hỗ Trợ

Nếu có vấn đề hoặc câu hỏi, vui lòng tạo issue hoặc liên hệ với team phát triển.

## 📄 License

Dự án này được tạo cho mục đích học tập và phát triển.

---

**Cập nhật lần cuối:** Tháng 5, 2026

