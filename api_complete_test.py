#!/usr/bin/env python
"""
AutoRent Backend API - Complete Testing Script

This script tests all three API endpoints:
1. Register - Create new user
2. Login - Authenticate and get JWT tokens
3. Logout - Logout with JWT token

Usage:
    python api_complete_test.py
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_register():
    """Test user registration endpoint"""
    print("\n" + "="*60)
    print("TEST 1: User Registration")
    print("="*60)
    
    url = f"{BASE_URL}/api/register/"
    data = {
        "name": f"Test User {int(time.time())}",
        "email": f"testuser{int(time.time())}@example.com",
        "phone": "0987654321",
        "password": "TestPassword123",
        "cccd": "123456789012"
    }
    
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data)
        print(f"\n✓ Status: {response.status_code}")
        result = response.json()
        print(f"✓ Response: {json.dumps(result, indent=2)}")
        
        if response.status_code == 201:
            print("✅ REGISTRATION SUCCESSFUL")
            return result.get('user', {}).get('email')
        else:
            print("❌ REGISTRATION FAILED")
            return None
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return None

def test_login(email="testuser@example.com", password="TestPass123"):
    """Test user login endpoint"""
    print("\n" + "="*60)
    print("TEST 2: User Login")
    print("="*60)
    
    url = f"{BASE_URL}/api/login/"
    data = {
        "username": email,
        "password": password
    }
    
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data)
        print(f"\n✓ Status: {response.status_code}")
        result = response.json()
        
        # Don't print full tokens (they're long)
        safe_result = result.copy()
        if 'access' in safe_result:
            safe_result['access'] = safe_result['access'][:50] + "..."
        if 'refresh' in safe_result:
            safe_result['refresh'] = safe_result['refresh'][:50] + "..."
        
        print(f"✓ Response: {json.dumps(safe_result, indent=2)}")
        
        if response.status_code == 200:
            print("✅ LOGIN SUCCESSFUL")
            return result.get('access'), result.get('refresh')
        else:
            print("❌ LOGIN FAILED")
            return None, None
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return None, None

def test_logout(access_token):
    """Test user logout endpoint"""
    print("\n" + "="*60)
    print("TEST 3: User Logout")
    print("="*60)
    
    url = f"{BASE_URL}/api/logout/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    print(f"URL: {url}")
    print(f"Headers: Authorization: Bearer {access_token[:50]}...")
    
    try:
        response = requests.post(url, headers=headers)
        print(f"\n✓ Status: {response.status_code}")
        result = response.json()
        print(f"✓ Response: {json.dumps(result, indent=2)}")
        
        if response.status_code == 200:
            print("✅ LOGOUT SUCCESSFUL")
            return True
        else:
            print("❌ LOGOUT FAILED")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("AutoRent Backend API - Complete Testing")
    print("="*60)
    
    # Test 1: Register
    email = test_register()
    
    # Test 2: Login with existing user
    print("\n" + "-"*60)
    print("Testing login with existing test user...")
    print("-"*60)
    access_token, refresh_token = test_login()
    
    # Test 3: Logout
    if access_token:
        print("\n" + "-"*60)
        print("Testing logout with JWT token...")
        print("-"*60)
        test_logout(access_token)
    
    print("\n" + "="*60)
    print("Testing Complete!")
    print("="*60)

if __name__ == "__main__":
    main()
