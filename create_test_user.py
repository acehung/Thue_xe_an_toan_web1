#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User

username = 'test@example.com'
email = 'test@example.com'
password = 'Test12345'

try:
    user = User.objects.get(username=username)
    print(f"User {username} already exists")
except User.DoesNotExist:
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name='Test User'
    )
    print(f"User {username} created successfully")
    print(f"Email: {email}")
    print(f"Password: {password}")
