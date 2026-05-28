# test_login.py
"""
Script để test & debug vấn đề đăng nhập
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

print("=" * 60)
print("DEBUG DANG NHAP - TEST SCRIPT")
print("=" * 60)

# 1. Kiểm tra users trong database
print("\n1️⃣  USERS TRONG DATABASE:")
users = User.objects.all()
print(f"   Tổng users: {len(users)}")
for u in users:
    print(f"   - Username: {u.username}, Email: {u.email}, Active: {u.is_active}")

# 2. Test tạo user mới nếu chưa có
print("\n2️⃣  TẠO TEST USER:")
test_email = "test@example.com"
test_username = test_email
test_password = "Test12345"

if not User.objects.filter(username=test_username).exists():
    new_user = User.objects.create_user(
        username=test_username,
        email=test_email,
        password=test_password,
        first_name='Test User'
    )
    print(f"   ✅ Tạo user mới: {test_username}")
    print(f"   Password: {test_password}")
else:
    existing_user = User.objects.get(username=test_username)
    print(f"   ℹ️  User đã tồn tại: {test_username}")
    # Update password
    existing_user.set_password(test_password)
    existing_user.save()
    print(f"   ✅ Cập nhật password: {test_password}")

# 3. Test Django authenticate
print("\n3️⃣  TEST AUTHENTICATE:")
print(f"   Username: {test_username}")
print(f"   Password: {test_password}")

auth_user = authenticate(username=test_username, password=test_password)

if auth_user is not None:
    print(f"   ✅ Authenticate THÀNH CÔNG!")
    print(f"   User ID: {auth_user.id}")
    print(f"   Username: {auth_user.username}")
    print(f"   Email: {auth_user.email}")
else:
    print(f"   ❌ Authenticate THẤT BẠI!")
    # Debug: Check nếu user tồn tại
    user_exists = User.objects.filter(username=test_username).exists()
    print(f"   User tồn tại: {user_exists}")
    
    if user_exists:
        db_user = User.objects.get(username=test_username)
        print(f"   User active: {db_user.is_active}")
        # Test password trực tiếp
        from django.contrib.auth.hashers import check_password
        pwd_check = check_password(test_password, db_user.password)
        print(f"   Password check: {pwd_check}")

# 4. Test JWT token creation
print("\n4️⃣  TEST JWT TOKEN:")
try:
    user = User.objects.get(username=test_username)
    refresh = RefreshToken.for_user(user)
    print(f"   ✅ Token tạo thành công!")
    print(f"   Access Token: {str(refresh.access_token)[:50]}...")
    print(f"   Refresh Token: {str(refresh)[:50]}...")
except Exception as e:
    print(f"   ❌ Lỗi tạo token: {str(e)}")

# 5. Test check password
print("\n5️⃣  TEST PASSWORD HASHING:")
from django.contrib.auth.hashers import make_password, check_password

test_pwd = "Test12345"
hashed = make_password(test_pwd)
print(f"   Original: {test_pwd}")
print(f"   Hashed: {hashed[:50]}...")
print(f"   Check: {check_password(test_pwd, hashed)}")

print("\n" + "=" * 60)
print("✅ DEBUG XONG!")
print("=" * 60)
print("\n📝 HỬ DÙNG CÁC THÔNG TIN Ở TRÊN ĐỂ TEST LOGIN!")
