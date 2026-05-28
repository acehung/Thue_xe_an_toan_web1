#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password, check_password

print("=" * 60)
print("DEBUG LOGIN - TEST SCRIPT")
print("=" * 60)

# 1. Check users
print("\n1. USERS IN DATABASE:")
users = User.objects.all()
print("   Total users: {}".format(len(users)))
for u in users:
    print("   - {}: {} (Active: {})".format(u.username, u.email, u.is_active))

# 2. Create test user
print("\n2. CREATE TEST USER:")
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
    print("   Created: {}".format(test_username))
else:
    existing_user = User.objects.get(username=test_username)
    print("   User exists: {}".format(test_username))
    existing_user.set_password(test_password)
    existing_user.save()
    print("   Updated password")

# 3. Test authenticate
print("\n3. TEST AUTHENTICATE:")
print("   Username: {}".format(test_username))
print("   Password: {}".format(test_password))

auth_user = authenticate(username=test_username, password=test_password)

if auth_user is not None:
    print("   SUCCESS! User authenticated")
    print("   User ID: {}".format(auth_user.id))
    print("   Email: {}".format(auth_user.email))
else:
    print("   FAILED! Authentication failed")
    user_exists = User.objects.filter(username=test_username).exists()
    print("   User exists: {}".format(user_exists))
    
    if user_exists:
        db_user = User.objects.get(username=test_username)
        print("   User active: {}".format(db_user.is_active))
        pwd_check = check_password(test_password, db_user.password)
        print("   Password match: {}".format(pwd_check))

# 4. Test JWT
print("\n4. TEST JWT TOKEN:")
try:
    user = User.objects.get(username=test_username)
    refresh = RefreshToken.for_user(user)
    print("   Token created successfully!")
    print("   Access: {}...".format(str(refresh.access_token)[:30]))
    print("   Refresh: {}...".format(str(refresh)[:30]))
except Exception as e:
    print("   Error: {}".format(str(e)))

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
print("\nUSE THIS INFO TO TEST LOGIN")
print("Username: {}".format(test_username))
print("Password: {}".format(test_password))
