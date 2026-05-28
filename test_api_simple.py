import requests
import json

url = "http://127.0.0.1:8000/api/login/"
data = {"username": "testuser@example.com", "password": "TestPass123"}

print("Testing API login endpoint...")
print(f"URL: {url}")
print(f"Data: {data}")
print()

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    print()
    if response.status_code == 200:
        result = response.json()
        print("SUCCESS! Login worked!")
        print(f"Access Token: {result.get('access', 'N/A')[:50]}...")
        print(f"Refresh Token: {result.get('refresh', 'N/A')[:50]}...")
    else:
        print(f"Login failed: {response.text}")
except Exception as e:
    print(f"ERROR: {e}")
