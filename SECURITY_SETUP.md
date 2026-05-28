# 🚀 QUICK START - CÀI ĐẶT TÍNH NĂNG BẢO MẬT

Hướng dẫn nhanh để cài đặt các tính năng bảo mật quan trọng cho AutoRent.

---

## 📋 BƯỚC 1: Cài Đặt Dependencies

```bash
# Cài tất cả packages bảo mật
pip install -r requirements-security.txt

# Hoặc cài thủ công
pip install argon2-cffi
pip install django-otp
pip install qrcode
pip install django-encrypted-model-fields
pip install django-ratelimit
pip install django-bleach
pip install sentry-sdk
pip install python-dotenv
pip install safety bandit
```

---

## 🔧 BƯỚC 2: Cấu Hình Environment Variables

```bash
# Sao chép file ví dụ
cp .env.example .env

# Chỉnh sửa .env với các giá trị thực
nano .env
```

**Các giá trị MUST CHANGE:**
```
SECRET_KEY=<tạo key mới bằng: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())">
DATABASE_PASSWORD=<tạo password mạnh>
EMAIL_HOST_PASSWORD=<app password từ Gmail>
STRIPE_SECRET_KEY=<từ Stripe dashboard>
```

---

## 🔐 BƯỚC 3: Cấu Hình Mã Hóa Mật Khẩu

**File: core/settings.py**

```python
# Thêm vào cuối file hoặc tìm PASSWORD_HASHERS
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]
```

**Kiểm tra:**
```bash
python manage.py shell
>>> from django.contrib.auth.hashers import check_password, make_password
>>> hash = make_password('testpass123')
>>> check_password('testpass123', hash)
True
```

---

## 🔑 BƯỚC 4: Cấu Hình JWT & Authentication

**File: core/settings.py**

```python
from datetime import timedelta
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': os.getenv('JWT_SECRET_KEY', SECRET_KEY),
}

# Xác thực
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# HTTPS & Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
```

---

## 🛡️ BƯỚC 5: Cấu Hình CORS (Nếu Có Frontend Riêng)

**File: core/settings.py**

```python
CORS_ALLOWED_ORIGINS = [
    "https://frontend.autorent.vn",
    "https://app.autorent.vn",
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\.autorent\.vn$",
]
```

---

## 📊 BƯỚC 6: Cấu Hình Logging & Monitoring

### 6.1 Tạo Audit Log Model

**File: api/models.py**

```python
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    resource = models.CharField(max_length=100)
    resource_id = models.IntegerField(null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=500, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['action', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.action} - {self.resource} - {self.timestamp}"
```

**Áp dụng migration:**
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6.2 Cấu Hình Sentry (Error Tracking)

**File: core/settings.py**

```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

if os.getenv('SENTRY_DSN'):
    sentry_sdk.init(
        dsn=os.getenv('SENTRY_DSN'),
        integrations=[DjangoIntegration()],
        traces_sample_rate=float(os.getenv('SENTRY_TRACES_SAMPLE_RATE', 0.1)),
        environment=os.getenv('SENTRY_ENVIRONMENT', 'development'),
        send_default_pii=False,
    )
```

---

## 🚫 BƯỚC 7: Cấu Hình Rate Limiting

**File: api/views.py**

```python
from django_ratelimit.decorators import ratelimit
from rest_framework.decorators import api_view, permission_classes

@api_view(['POST'])
@ratelimit(key='ip', rate='5/h')  # 5 lần/giờ per IP
@permission_classes([AllowAny])
def login(request):
    # Logic login
    pass
```

---

## ✅ BƯỚC 8: Cài Đặt 2FA (Tùy Chọn)

**Cài đặt:**
```bash
pip install django-otp qrcode
```

**Thêm vào INSTALLED_APPS:**
```python
INSTALLED_APPS = [
    ...
    'django_otp',
    'django_otp.plugins.otp_totp',
    ...
]
```

**Migration:**
```bash
python manage.py migrate
```

---

## 🔒 BƯỚC 9: Mã Hóa Các Trường Nhạy Cảm

**File: api/models.py**

```bash
pip install django-encrypted-model-fields
```

```python
from django_cryptography.fields import EncryptedCharField

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cccd_number = EncryptedCharField(max_length=20)
    phone_number = EncryptedCharField(max_length=20)
    license_number = EncryptedCharField(max_length=30)
```

---

## 🧪 BƯỚC 10: Kiểm Tra Bảo Mật

```bash
# Kiểm tra vulnerabilities trong dependencies
safety check

# Kiểm tra code security issues
bandit -r api/

# Django security check
python manage.py check --deploy

# Chạy tests
python manage.py test

# Coverage
pytest --cov=api
```

---

## 📝 BƯỚC 11: Cấu Hình Production

### 11.1 Sử Dụng Gunicorn

```bash
pip install gunicorn

# Chạy
gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### 11.2 Cấu Hình Nginx Reverse Proxy

**File: /etc/nginx/sites-available/autorent**

```nginx
upstream django {
    server 127.0.0.1:8000;
}

server {
    listen 443 ssl http2;
    server_name api.autorent.vn;
    
    ssl_certificate /etc/letsencrypt/live/autorent.vn/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/autorent.vn/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    client_max_body_size 5M;
    
    location /static/ {
        alias /app/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias /app/media/;
        expires 7d;
    }
    
    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name api.autorent.vn;
    return 301 https://$server_name$request_uri;
}
```

**Enable:**
```bash
sudo ln -s /etc/nginx/sites-available/autorent /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 11.3 SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d api.autorent.vn -d autorent.vn

# Auto-renewal
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

---

## 🔄 BƯỚC 12: Automated Backup

**File: backup.sh**

```bash
#!/bin/bash
BACKUP_DIR="/backups/autorent"
DB_NAME="autorent_db"
DB_USER="postgres"
DATE=$(date +%Y-%m-%d_%H:%M:%S)

# Tạo backup directory nếu chưa có
mkdir -p $BACKUP_DIR

# Database backup
pg_dump -U $DB_USER $DB_NAME | gzip > "$BACKUP_DIR/db_$DATE.sql.gz"

# Media files backup
tar -czf "$BACKUP_DIR/media_$DATE.tar.gz" /app/media/ 2>/dev/null || true

# Xóa backup cũ hơn 30 ngày
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete

echo "Backup completed: $DATE" >> /var/log/backup.log
```

**Cấp quyền execute:**
```bash
chmod +x backup.sh

# Thêm vào crontab (mỗi ngày 2:00 AM)
crontab -e
# Thêm dòng:
0 2 * * * /app/backup.sh
```

---

## ✨ BƯỚC 13: Tạo Superuser Admin

```bash
python manage.py createsuperuser

# Hoặc từ shell
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.create_superuser('admin', 'admin@autorent.vn', 'SecurePassword123!')
```

---

## 🧐 BƯỚC 14: Testing Bảo Mật

### Test Login
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test12345"}'
```

### Test HTTPS/HSTS
```bash
curl -I https://api.autorent.vn

# Kiểm tra headers
# Strict-Transport-Security: max-age=31536000
# X-Frame-Options: DENY
# X-Content-Type-Options: nosniff
```

### Test CORS
```bash
curl -X OPTIONS http://localhost:8000/api/ \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST"
```

---

## 📋 FINAL CHECKLIST

```
✅ TRƯỚC KHI DEPLOY:

Environment
☐ .env file được tạo với giá trị thực
☐ SECRET_KEY đã được thay đổi
☐ DEBUG = False
☐ ALLOWED_HOSTS cấu hình đúng

Database
☐ PostgreSQL được cài đặt
☐ Migrations chạy thành công
☐ Superuser được tạo

Security
☐ Argon2 password hashing được bật
☐ HTTPS/TLS được cấu hình
☐ Rate limiting được bật
☐ CORS được cấu hình đúng
☐ Logging & audit được cấu hình

Testing
☐ Django check --deploy chạy không lỗi
☐ Tests chạy pass (90%+ coverage)
☐ Safety check không có vulnerabilities
☐ Bandit scan không có critical issues

Monitoring
☐ Sentry được cấu hình
☐ Logging được cấu hình
☐ Backup script được kiểm tra

Deployment
☐ Gunicorn/ASGI server được cấu hình
☐ Nginx reverse proxy được cấu hình
☐ SSL certificate được cài đặt
☐ Firewall rules được cấu hình
```

---

## 📞 SUPPORT

Nếu gặp vấn đề:

1. **Check Django logs:**
   ```bash
   tail -f /var/log/django/error.log
   ```

2. **Check Nginx logs:**
   ```bash
   tail -f /var/log/nginx/error.log
   ```

3. **Django shell debugging:**
   ```bash
   python manage.py shell
   >>> from django.contrib.auth.models import User
   >>> User.objects.all()
   ```

4. **Kiểm tra database connection:**
   ```bash
   python manage.py dbshell
   ```

---

**Cập Nhật Lần Cuối**: Tháng 5, 2026
**Độ Ưu Tiên**: 🔴 IMPLEMENT TRƯỚC KHI PRODUCTION
