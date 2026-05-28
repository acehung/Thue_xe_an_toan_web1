# 🔒 HƯỚNG DẪN BẢO MẬT WEB - AutoRent

Tài liệu này hướng dẫn các tính năng bảo mật cần triển khai để bảo vệ dữ liệu người dùng, xe, và giao dịch.

---

## 1️⃣ MÃ HÓA DỮ LIỆU

### 1.1 Mã Hóa Mật Khẩu

**Hiện Tại (⚠️ Cải Thiện Cần Thiết):**
```python
# Django mặc định sử dụng PBKDF2 (ổn định nhưng chậm)
# settings.py - PASSWORD_HASHERS
```

**Cải Thiện - Sử Dụng Argon2:**
```bash
pip install argon2-cffi
```

```python
# core/settings.py
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',  # Mạnh nhất
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',  # Dự phòng
]

# Cấu hình Argon2
PASSWORD_VALIDATION_FUNCTION = {
    'Argon2PasswordHasher': {
        'time_cost': 2,      # Số lần lặp (càng cao càng mạnh nhưng chậm)
        'memory_cost': 512,  # MB RAM dùng
        'parallelism': 2,    # Số threads
    }
}
```

**Kiểm Tra Mã Hóa:**
```python
from django.contrib.auth.hashers import make_password, check_password

# Tạo hash
hashed = make_password("password123")
print(hashed)  # argon2$argon2id$v=19$m=512,t=2,p=2$...

# Kiểm tra
is_valid = check_password("password123", hashed)  # True
```

### 1.2 Mã Hóa Trường Dữ Liệu Nhạy Cảm

**Cài Đặt:**
```bash
pip install django-encrypted-model-fields
```

**Models.py:**
```python
from django_cryptography.fields import EncryptedCharField
from django.db import models

class CustomerDocument(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE)
    # Các trường này sẽ được mã hóa AES-256
    cccd_number = EncryptedCharField(max_length=20)
    phone_number = EncryptedCharField(max_length=20)
    license_number = EncryptedCharField(max_length=30)
    
    class Meta:
        db_table = 'api_customer_document'
```

**Cách Hoạt Động:**
- Dữ liệu được mã hóa trước khi lưu vào DB
- Tự động giải mã khi lấy từ DB
- Nếu bị hack database, dữ liệu vẫn an toàn

### 1.3 Mã Hóa HTTPS/TLS

**Production Settings:**
```python
# core/settings.py
SECURE_SSL_REDIRECT = True           # Chuyển HTTP → HTTPS
SESSION_COOKIE_SECURE = True         # Cookie chỉ qua HTTPS
CSRF_COOKIE_SECURE = True            # CSRF token qua HTTPS
SECURE_HSTS_SECONDS = 31536000       # 1 năm HSTS
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'             # Chống clickjacking
SECURE_CONTENT_SECURITY_POLICY = {
    "default-src": ("'self'",),
}
```

**Cấu Hình Nginx (Reverse Proxy):**
```nginx
server {
    listen 443 ssl http2;
    server_name autorent.vn;
    
    ssl_certificate /etc/letsencrypt/live/autorent.vn/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/autorent.vn/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Chuyển HTTP sang HTTPS
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Chuyển HTTP -> HTTPS
server {
    listen 80;
    server_name autorent.vn;
    return 301 https://$server_name$request_uri;
}
```

---

## 2️⃣ XÁC THỰC & PHÂN QUYỀN

### 2.1 Xác Thực 2 Yếu Tố (2FA/MFA)

**Cài Đặt:**
```bash
pip install django-otp qrcode
```

**Models.py:**
```python
from django_otp.models import user_has_device
from django_otp.plugins.otp_totp.models import Device

class User(AbstractUser):
    two_factor_enabled = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    
    def setup_2fa(self):
        """Thiết lập 2FA qua authenticator app (Google Authenticator, Authy)"""
        device = Device.objects.create(
            user=self,
            confirmed=False,
            name='default'
        )
        # Trả về QR code cho người dùng quét
        return device.config_url
```

**Views.py:**
```python
from django_otp.decorators import otp_required
from django_otp.plugins.otp_totp.models import Device
from django_otp.util import random_hex

@api_view(['POST'])
@permission_classes([AllowAny])
def setup_2fa(request):
    """
    Người dùng gọi API này để bắt đầu thiết lập 2FA
    Response: QR code URL
    """
    try:
        user = request.user
        
        # Tạo device mới
        device = Device.objects.create(
            user=user,
            confirmed=False,
            name='default'
        )
        
        # Trả về QR code
        import qrcode
        qr = qrcode.QRCode()
        qr.add_data(device.config_url)
        qr.make(fit=True)
        
        return Response({
            'qr_code': device.config_url,
            'secret_key': device.key,
            'message': 'Scan this QR code with authenticator app'
        })
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_2fa(request):
    """
    Người dùng nhập OTP từ authenticator app
    Request: {otp: "123456"}
    """
    otp_code = request.data.get('otp')
    
    try:
        device = Device.objects.get(user=request.user, confirmed=False)
        
        # Kiểm tra OTP (mỗi OTP có hiệu lực ~30 giây)
        if device.verify_token(otp_code):
            device.confirmed = True
            device.save()
            
            request.user.two_factor_enabled = True
            request.user.save()
            
            return Response({'success': 'Two-factor authentication enabled'})
        else:
            return Response({'error': 'Invalid OTP'}, status=400)
    except Device.DoesNotExist:
        return Response({'error': 'Device not found'}, status=404)

# Bảo vệ API quan trọng với 2FA
@api_view(['POST'])
@otp_required
def withdraw_money(request):
    """API này yêu cầu OTP xác thực thêm"""
    # Chỉ người dùng đã xác thực OTP mới vào được
    pass
```

### 2.2 Token JWT an Toàn

**Cải Thiện Settings:**
```python
# core/settings.py
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),      # Token hết hạn sau 1 giờ
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),      # Refresh token 7 ngày
    'ROTATE_REFRESH_TOKENS': True,                    # Xoay refresh token sau mỗi lần dùng
    'BLACKLIST_AFTER_ROTATION': True,                 # Blacklist token cũ
    
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': settings.SECRET_KEY,               # ⚠️ Thay bằng key riêng trong production
    
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    
    # Cấu hình bảo mật thêm
    'TOKEN_VALIDATE_LIFETIME': True,
    'SLIDING_TOKEN_LIFETIME': timedelta(hours=1),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=7),
}
```

**Token Blacklist:**
```bash
pip install djangorestframework-simplejwt[cryptography]
```

```python
# models.py
from rest_framework_simplejwt.models import TokenBlacklist

# Tự động tạo table TokenBlacklist
```

```python
# views.py
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def logout(request):
    """
    Logout: Thêm token vào blacklist
    Request: {refresh: "token"}
    """
    try:
        refresh = RefreshToken(request.data['refresh'])
        refresh.blacklist()
        return Response({'success': 'Logged out successfully'})
    except Exception as e:
        return Response({'error': str(e)}, status=400)
```

### 2.3 Quản Lý Quyền Truy Cập (Permission)

```python
# models.py
from django.contrib.auth.models import AbstractUser
from rest_framework.permissions import BasePermission

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('customer', 'Customer'),
        ('support', 'Support Staff'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

class IsAdmin(BasePermission):
    """Chỉ admin được truy cập"""
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'

class IsCustomer(BasePermission):
    """Chỉ khách hàng được truy cập"""
    def has_permission(self, request, view):
        return request.user and request.user.role == 'customer'

class IsOwner(BasePermission):
    """Chỉ chủ sở hữu dữ liệu được truy cập"""
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

# Sử dụng trong views
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsCustomer])
def get_my_bookings(request):
    """Chỉ khách hàng xác thực mới truy cập được"""
    bookings = Booking.objects.filter(customer=request.user)
    return Response(serializers.BookingSerializer(bookings, many=True).data)
```

---

## 3️⃣ CHỐNG TẤN CÔNG

### 3.1 Chống SQL Injection

**✅ Django ORM Bảo Vệ Tự Động:**
```python
# ✅ AN TOÀN - sử dụng ORM
user = User.objects.filter(email=request.data['email']).first()

# ❌ NGUY HIỂM - raw query
user = User.objects.raw(f"SELECT * FROM auth_user WHERE email = '{email}'")
```

**Nếu phải dùng raw SQL:**
```python
from django.db import connection

# ✅ AN TOÀN - sử dụng parameter binding
with connection.cursor() as cursor:
    cursor.execute(
        "SELECT * FROM auth_user WHERE email = %s",
        [request.data['email']]
    )
    user = cursor.fetchone()
```

### 3.2 Chống XSS (Cross-Site Scripting)

**Cài Đặt:**
```bash
pip install django-bleach
```

```python
# models.py
from bleach import clean
from django.db import models

class Review(models.Model):
    text = models.TextField()
    
    def save(self, *args, **kwargs):
        # Làm sạch HTML/script
        self.text = clean(
            self.text,
            tags=['b', 'i', 'u', 'p', 'br'],  # Chỉ cho phép các tag an toàn
            strip=True  # Xóa các tag không an toàn
        )
        super().save(*args, **kwargs)

# Settings
BLEACH_ALLOWED_TAGS = ['b', 'i', 'u', 'p', 'br', 'a']
BLEACH_ALLOWED_ATTRIBUTES = {'a': ['href', 'title']}
BLEACH_STRIP_TAGS = True
```

**Frontend Angular/React:**
```javascript
// Angular - ngSanitizer
<div [innerHTML]="userComment | sanitize"></div>

// React - dangerouslySetInnerHTML (hạn chế sử dụng)
import DOMPurify from 'dompurify';
<div dangerouslySetInnerHTML={{__html: DOMPurify.sanitize(userComment)}} />
```

### 3.3 Chống CSRF (Cross-Site Request Forgery)

**Django Bảo Vệ Tự Động:**
```python
# settings.py - Mặc định kích hoạt
MIDDLEWARE = [
    ...
    'django.middleware.csrf.CsrfViewMiddleware',
    ...
]

CSRF_COOKIE_SECURE = True  # Chỉ qua HTTPS
CSRF_COOKIE_HTTPONLY = False  # JavaScript có thể truy cập token để gửi lại
CSRF_COOKIE_SAMESITE = 'Strict'  # Chỉ gửi với same-site requests
```

**Frontend gửi CSRF token:**
```html
<!-- HTML -->
<form method="POST">
    {% csrf_token %}
    <input type="text" name="data">
</form>
```

```javascript
// JavaScript - Lấy CSRF token từ cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Gửi request với CSRF token
fetch('/api/register/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify({name: 'test'})
})
```

### 3.4 Chống Brute Force / Rate Limiting

**Cài Đặt:**
```bash
pip install django-ratelimit
```

```python
# views.py
from django_ratelimit.decorators import ratelimit

@api_view(['POST'])
@ratelimit(key='ip', rate='5/h', method='POST')  # 5 lần/giờ per IP
@permission_classes([AllowAny])
def login(request):
    """Giới hạn 5 lần đăng nhập thất bại/giờ"""
    email = request.data.get('email')
    password = request.data.get('password')
    
    user = authenticate(username=email, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })
    else:
        # Log failed attempt
        return Response({'error': 'Invalid credentials'}, status=401)

# Rate limit per API endpoint
@api_view(['POST'])
@ratelimit(key='user', rate='10/d')  # 10 lần/ngày per user
@permission_classes([IsAuthenticated])
def create_booking(request):
    """Giới hạn 10 đặt xe/ngày per khách hàng"""
    pass
```

**Settings:**
```python
# core/settings.py
RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = 'default'

# Cache cấu hình
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

---

## 4️⃣ QUẢN LÝ SESSION & COOKIE

### 4.1 Session Configuration

```python
# core/settings.py
# Session bảo mật
SESSION_COOKIE_SECURE = True        # Chỉ HTTPS
SESSION_COOKIE_HTTPONLY = True      # JavaScript không truy cập
SESSION_COOKIE_SAMESITE = 'Strict'  # Chỉ same-site
SESSION_COOKIE_AGE = 3600           # Hết hạn sau 1 giờ
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_DOMAIN = 'autorent.vn'

# Lưu session trên Redis (an toàn hơn file)
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
```

### 4.2 Logout & Session Invalidation

```python
from django.contrib.auth import logout
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Logout: Hủy session và token
    """
    try:
        # Hủy refresh token
        refresh = RefreshToken(request.data['refresh'])
        refresh.blacklist()
        
        # Hủy Django session
        logout(request)
        
        return Response({'success': 'Logged out'})
    except Exception as e:
        return Response({'error': str(e)}, status=400)
```

---

## 5️⃣ QUẢN LÝ API KEY & SECRET

### 5.1 API Key Rotation

```python
# models.py
import secrets
from django.db import models

class APIKey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=40, unique=True)
    secret = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    rotated_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        if not self.key:
            # Tạo key ngẫu nhiên 40 ký tự
            self.key = secrets.token_urlsafe(30)
            self.secret = secrets.token_urlsafe(30)
        super().save(*args, **kwargs)
    
    @classmethod
    def rotate_key(cls, user):
        """Tạo key mới, hủy key cũ"""
        old_key = cls.objects.filter(user=user, is_active=True).first()
        if old_key:
            old_key.is_active = False
            old_key.save()
        
        new_key = cls.objects.create(user=user)
        return new_key
```

```python
# views.py
from django.contrib.auth.decorators import login_required

@api_view(['GET'])
@login_required
def get_api_key(request):
    """Lấy API key của user"""
    api_key = APIKey.objects.filter(user=request.user, is_active=True).first()
    if not api_key:
        api_key = APIKey.objects.create(user=request.user)
    
    return Response({
        'key': api_key.key,
        'created_at': api_key.created_at
    })

@api_view(['POST'])
@login_required
def rotate_api_key(request):
    """Xoay API key - hủy cái cũ, tạo cái mới"""
    new_key = APIKey.rotate_key(request.user)
    return Response({
        'key': new_key.key,
        'message': 'New API key generated, old key disabled'
    })
```

### 5.2 Chứng Thực API Key

```python
# Middleware hoặc Authentication class
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class APIKeyAuthentication(BaseAuthentication):
    """
    Header cần có: X-API-Key: <api_key>
    """
    def authenticate(self, request):
        api_key = request.META.get('HTTP_X_API_KEY')
        if not api_key:
            return None  # Không sử dụng authentication này
        
        try:
            api_key_obj = APIKey.objects.get(key=api_key, is_active=True)
        except APIKey.DoesNotExist:
            raise AuthenticationFailed('Invalid API key')
        
        return (api_key_obj.user, None)

# Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'api.authentication.APIKeyAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}
```

---

## 6️⃣ LOGGING & MONITORING

### 6.1 Audit Log (Lưu Trữ Hoạt Động)

```python
# models.py
from django.db import models
from django.contrib.auth.models import User
import json

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('view', 'View'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    resource = models.CharField(max_length=100)  # Model name (Booking, Car, etc)
    resource_id = models.IntegerField(null=True, blank=True)
    
    old_values = models.JSONField(null=True, blank=True)
    new_values = models.JSONField(null=True, blank=True)
    
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=500)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['resource', 'action']),
        ]

# Utility function để ghi log
def log_action(request, action, resource, resource_id=None, old_values=None, new_values=None):
    """Ghi audit log"""
    AuditLog.objects.create(
        user=request.user if request.user.is_authenticated else None,
        action=action,
        resource=resource,
        resource_id=resource_id,
        old_values=old_values,
        new_values=new_values,
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
    )

def get_client_ip(request):
    """Lấy IP thực của client (qua proxy)"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
```

```python
# views.py
@api_view(['POST'])
def register(request):
    # ... code đăng ký ...
    
    # Ghi log đăng ký
    log_action(request, 'create', 'User', new_user.id, 
               new_values={'email': new_user.email, 'name': new_user.first_name})
    
    return Response({'success': 'User created'})
```

### 6.2 Error Logging (Sentry)

**Cài Đặt:**
```bash
pip install sentry-sdk
```

```python
# core/settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://your-sentry-dsn@sentry.io/project-id",
    integrations=[DjangoIntegration()],
    
    # Set traces_sample_rate to 1.0 to capture 100% of transactions for performance monitoring
    traces_sample_rate=1.0,
    
    # Set `profiles_sample_rate` to sample 0.1 (10%) of all transactions
    profiles_sample_rate=0.1,
    
    # If you wish to associate users to errors
    send_default_pii=False,
    
    environment="production",
)

# Cấu hình logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/django/error.log',
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'api': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```

---

## 7️⃣ QUẢN LÝ DEPENDENCIES & VULNERABILITIES

### 7.1 Kiểm Tra Lỗ Hổng Bảo Mật

```bash
# Cài đặt tool kiểm tra
pip install safety bandit

# Kiểm tra dependencies có lỗ hổng
safety check

# Kiểm tra code bảo mật
bandit -r api/ -f json > bandit-report.json
```

### 7.2 Requirements.txt with Pinned Versions

```
# requirements.txt
Django==6.0.5
djangorestframework==3.14.0
djangorestframework-simplejwt==5.2.2
django-cors-headers==4.0.0
django-otp==1.1.3
qrcode==7.4.2
argon2-cffi==23.1.0
django-encrypted-model-fields==0.5.10
django-ratelimit==4.1.0
sentry-sdk==1.25.1
django-bleach==0.6.1

# Database
psycopg2-binary==2.9.6  # PostgreSQL

# Cache & Task Queue
redis==5.0.0
celery==5.3.1

# Testing
pytest==7.4.0
pytest-django==4.5.2
pytest-cov==4.1.0
factory-boy==3.3.0

# Code Quality
black==23.7.0
flake8==6.0.0
isort==5.12.0
pylint==2.17.5
```

---

## 8️⃣ BACKUP & DISASTER RECOVERY

### 8.1 Automated Database Backup

```bash
#!/bin/bash
# backup.sh - Chạy mỗi ngày lúc 2:00 AM

BACKUP_DIR="/backups/django"
DB_NAME="autorent_db"
DB_USER="postgres"
DATE=$(date +%Y-%m-%d_%H:%M:%S)

# Backup database
pg_dump -U $DB_USER $DB_NAME | gzip > "$BACKUP_DIR/db_$DATE.sql.gz"

# Backup media files
tar -czf "$BACKUP_DIR/media_$DATE.tar.gz" /app/media/

# Xóa backup cũ hơn 30 ngày
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete

echo "Backup completed: $DATE"
```

```bash
# Thêm vào crontab
crontab -e

# Backup mỗi ngày 2:00 AM
0 2 * * * /app/backup.sh >> /var/log/backup.log 2>&1
```

### 8.2 Database Replication (PostgreSQL)

```sql
-- Primary server: Streaming Replication
-- /etc/postgresql/14/main/postgresql.conf
wal_level = replica
max_wal_senders = 10
max_replication_slots = 10

-- Tạo replication user
CREATE ROLE replicator WITH REPLICATION PASSWORD 'replica_password' LOGIN;
```

---

## 9️⃣ ENVIRONMENT VARIABLES

### 9.1 Sử Dụng .env

```bash
pip install python-dotenv
```

```python
# core/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Thay vì hard-code
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
DATABASE_URL = os.getenv('DATABASE_URL')

# Email config
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# Payment gateway
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')

# Sentry
SENTRY_DSN = os.getenv('SENTRY_DSN')
```

```env
# .env (KHÔNG COMMIT LÊN GIT!)
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=False
ALLOWED_HOSTS=autorent.vn,www.autorent.vn,api.autorent.vn
DATABASE_URL=postgresql://user:password@db:5432/autorent_db
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
STRIPE_SECRET_KEY=sk_live_xxxx
STRIPE_PUBLISHABLE_KEY=pk_live_xxxx
SENTRY_DSN=https://xxxxx@sentry.io/xxxxx
```

```gitignore
# .gitignore
.env
.env.local
*.pyc
__pycache__/
*.log
/media/
/static/
/venv/
.DS_Store
```

---

## 🔟 CHECKLIST BẢO MẬT PRODUCTION

```
✅ TRƯỚC KHI DEPLOY:

Authentication & Authorization
☐ Thay SECRET_KEY (bằng giá trị ngẫu nhiên mạnh)
☐ Bật 2FA cho admin accounts
☐ Thiết lập JWT token lifetime hợp lý
☐ Kiểm tra quyền access (permissions) tất cả endpoints
☐ Xóa test users, test accounts

Database & Storage
☐ Sử dụng database strong password
☐ Restrict database network access (firewall)
☐ Enable database replication/backup
☐ Test restore từ backup
☐ Encrypt sensitive database fields

API Security
☐ Enable HTTPS/TLS (SSL certificate)
☐ Cấu hình CORS hợp lý (chỉ trusted domains)
☐ Bật rate limiting
☐ Implement API key rotation
☐ Xóa debug endpoints

Code & Dependencies
☐ Chạy `safety check` - không có vulnerabilities
☐ Chạy `bandit` - check security issues
☐ Code review bởi 2+ developers
☐ Xóa các print statements, debug logs
☐ Pin dependencies versions

Configuration
☐ DEBUG = False
☐ ALLOWED_HOSTS = chỉ production domains
☐ SESSION_COOKIE_SECURE = True
☐ CSRF_COOKIE_SECURE = True
☐ SECURE_SSL_REDIRECT = True
☐ SECURE_HSTS_SECONDS = 31536000

Monitoring & Logging
☐ Setup Sentry để track errors
☐ Setup logging (file rotation)
☐ Setup audit logging
☐ Alert system để notify errors
☐ Monitor database size & performance

Environment
☐ .env file bảo mật (không trong git)
☐ Process monitoring (supervisor, systemd)
☐ Log rotation (logrotate)
☐ Firewall rules (ufw, iptables)
☐ Regular security updates (OS, packages)

Testing
☐ Test login/logout
☐ Test API authentication
☐ Test rate limiting
☐ Test CSRF protection
☐ Test XSS prevention
☐ Test SQL injection prevention
☐ Security penetration testing

Backup & Recovery
☐ Automated daily backups
☐ Test restore procedures
☐ Off-site backup storage
☐ Disaster recovery plan

Documentation
☐ Security policy document
☐ Incident response plan
☐ API documentation (security sections)
☐ Admin guide bảo mật
```

---

## 📚 TÀI LIỆU THAM KHẢO

- [Django Security](https://docs.djangoproject.com/en/6.0/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django REST Framework Security](https://www.django-rest-framework.org/api-guide/authentication/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

---

**Cập Nhật Lần Cuối**: Tháng 5, 2026
**Độ Ưu Tiên**: 🔴 CẦN THỰC HIỆN NGAY TRẢ KHI DEPLOY
