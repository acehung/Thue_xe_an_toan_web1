#!/usr/bin/env python
"""
AutoRent - Fake Vehicle GPS Simulator (Simple Version)

Script giả lập xe GPS gửi tọa độ ngẫu nhiên lên API backend.
Không cần Django setup, chỉ dùng requests library.

Cách sử dụng:
    python fake_vehicle_simple.py

Hoặc với tùy chọn:
    python fake_vehicle_simple.py --vehicle-id 1 --interval 5 --duration 120
"""

import requests
import json
import time
import random
import argparse
import sys

BASE_URL = "http://127.0.0.1:8000/api"
LOGIN_EMAIL = "testuser@example.com"
LOGIN_PASSWORD = "TestPass123"

# Các khu vực địa lý
ZONES = {
    1: {'name': 'HCMC District 1', 'lat': 10.7769, 'lng': 106.6966, 'radius': 0.02},
    2: {'name': 'HCMC District 3', 'lat': 10.8017, 'lng': 106.7171, 'radius': 0.02},
    3: {'name': 'HCMC District 7', 'lat': 10.7538, 'lng': 106.6262, 'radius': 0.02},
    4: {'name': 'HCMC Thu Duc', 'lat': 10.8447, 'lng': 106.7604, 'radius': 0.02},
    5: {'name': 'HCMC Binh Thanh', 'lat': 10.9268, 'lng': 106.8408, 'radius': 0.02},
    7: {'name': 'Hanoi Hoan Kiem', 'lat': 21.0285, 'lng': 105.8542, 'radius': 0.02},
    8: {'name': 'Hanoi Cau Giay', 'lat': 21.0549, 'lng': 105.8581, 'radius': 0.02},
    9: {'name': 'Hanoi Ba Dinh', 'lat': 20.9927, 'lng': 105.7893, 'radius': 0.02},
    10: {'name': 'Hanoi Dong Da', 'lat': 21.0069, 'lng': 105.8471, 'radius': 0.02},
}

VEHICLE_INFO = {
    1: 'Toyota Vios 2023 (SG-001-AA)',
    2: 'Honda City 2022 (SG-002-AA)',
    3: 'Hyundai i10 2023 (SG-003-AA)',
    4: 'Toyota Fortuner 2022 (SG-004-AA)',
    5: 'Kia Cerato 2021 (SG-005-AA)',
    6: 'Mitsubishi Xpander 2023 (SG-006-AA)',
    7: 'Toyota Camry 2022 (HN-001-AA)',
    8: 'Ford Ranger 2023 (HN-002-AA)',
    9: 'Honda Civic 2021 (HN-003-AA)',
    10: 'Mazda CX-5 2023 (HN-004-AA)',
}


class FakeVehicle:
    def __init__(self, vehicle_id):
        self.vehicle_id = vehicle_id
        self.vehicle_name = VEHICLE_INFO.get(vehicle_id, f"Vehicle {vehicle_id}")
        self.zone = ZONES.get(vehicle_id, ZONES[1])
        self.current_lat = self.zone['lat']
        self.current_lng = self.zone['lng']
        self.access_token = None
    
    def login(self):
        """Đăng nhập lấy JWT token"""
        try:
            print(f"🔑 Đang đăng nhập...")
            response = requests.post(
                f"{BASE_URL}/login/",
                json={"username": LOGIN_EMAIL, "password": LOGIN_PASSWORD},
                timeout=5
            )
            
            if response.status_code == 200:
                self.access_token = response.json().get('access')
                print(f"✅ Đăng nhập thành công!\n")
                return True
            else:
                print(f"❌ Đăng nhập thất bại: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Lỗi kết nối: {e}")
            return False
    
    def get_random_location(self):
        """Tạo tọa độ ngẫu nhiên"""
        lat_offset = random.uniform(-self.zone['radius'], self.zone['radius'])
        lng_offset = random.uniform(-self.zone['radius'], self.zone['radius'])
        
        new_lat = self.zone['lat'] + lat_offset
        new_lng = self.zone['lng'] + lng_offset
        
        return new_lat, new_lng
    
    def move_location(self):
        """Di chuyển xe (thay đổi nhỏ tọa độ)"""
        # 80% di chuyển nhỏ, 20% teleport
        if random.random() > 0.2:
            self.current_lat += random.uniform(-0.004, 0.004)
            self.current_lng += random.uniform(-0.004, 0.004)
        else:
            self.current_lat, self.current_lng = self.get_random_location()
    
    def update_gps(self):
        """Cập nhật vị trí lên API"""
        if not self.access_token:
            return False
        
        self.move_location()
        
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                f"{BASE_URL}/vehicles/{self.vehicle_id}/location/",
                headers=headers,
                json={
                    "latitude": self.current_lat,
                    "longitude": self.current_lng,
                    "location_name": self.zone['name']
                },
                timeout=5
            )
            
            if response.status_code == 200:
                ts = time.strftime("%H:%M:%S")
                print(f"✅ {ts} | {self.vehicle_name:35} | "
                      f"({self.current_lat:.4f}, {self.current_lng:.4f})")
                return True
            else:
                print(f"⚠️  {self.vehicle_name} - HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ {self.vehicle_name} - {str(e)[:50]}")
            return False
    
    def run(self, interval=5, duration=None):
        """Chạy giả lập"""
        if not self.login():
            return
        
        print("="*80)
        print(f"🚗 Xe: {self.vehicle_name}")
        print(f"📍 Khu vực: {self.zone['name']}")
        print(f"⏱️  Update: mỗi {interval}s")
        if duration:
            print(f"⏰ Thời gian: {duration//60}m {duration%60}s")
        else:
            print(f"⏰ Chế độ: Chạy liên tục (Ctrl+C để dừng)")
        print("="*80)
        print()
        
        start = time.time()
        count = 0
        
        try:
            while True:
                if duration and (time.time() - start) > duration:
                    break
                
                self.update_gps()
                count += 1
                time.sleep(interval)
        
        except KeyboardInterrupt:
            print("\n\n⛔ Dừng!")
        finally:
            elapsed = time.time() - start
            print(f"\n📊 Kết quả: {count} updates trong {elapsed:.1f}s")


def print_vehicles():
    """In danh sách xe"""
    print("\n📋 Danh sách xe có thể giả lập:\n")
    for vid, name in VEHICLE_INFO.items():
        print(f"  ID {vid}: {name}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description='🚗 AutoRent Fake Vehicle GPS Simulator'
    )
    parser.add_argument(
        '--vehicle-id',
        type=int,
        default=1,
        help='ID xe (1-10, default=1)'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=5,
        help='Khoảng update (giây, default=5)'
    )
    parser.add_argument(
        '--duration',
        type=int,
        default=0,
        help='Thời gian chạy (giây, 0=vô tận)'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='Hiển thị danh sách xe'
    )
    
    args = parser.parse_args()
    
    if args.list:
        print_vehicles()
        return
    
    if args.vehicle_id not in VEHICLE_INFO:
        print(f"❌ ID xe không hợp lệ (1-10)")
        print_vehicles()
        return
    
    vehicle = FakeVehicle(args.vehicle_id)
    vehicle.run(
        interval=args.interval,
        duration=args.duration if args.duration > 0 else None
    )


if __name__ == '__main__':
    print("\n")
    print("┌" + "─"*78 + "┐")
    print("│" + " "*78 + "│")
    print("│" + "  🚗 AutoRent - Fake Vehicle GPS Simulator  ".center(78) + "│")
    print("│" + " "*78 + "│")
    print("└" + "─"*78 + "┘")
    print()
    
    main()
