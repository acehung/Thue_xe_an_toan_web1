#!/usr/bin/env python
"""
Install requests library
"""

import subprocess
import sys

print("Installing requests library...")
print()

try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    print()
    print("✅ Installation successful!")
    print()
    print("Now you can run:")
    print("  python fake_vehicle_simple.py")
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
