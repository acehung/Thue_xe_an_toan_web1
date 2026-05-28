#!/usr/bin/env python
"""
AutoRent - Fake Vehicle GPS Simulator

Script này giả lập một xe GPS gửi tọa độ ngẫu nhiên lên API backend.
Hữu ích để test hệ thống theo dõi vị trí thực thời.

Cách sử dụng:
    python fake_vehicle_gps.py
"""

import requests
import json
import time
import random
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
sys.path.insert(0, 'e:\\autorent_backend')

BASE_URL = "http://127.0.0.1:8000/api"
LOGIN_EMAIL = "testuser@example.com"
LOGIN_PASSWORD = "TestPass123"

# Khu vực địa lý để tạo tọa độ ngẫu nhiên
ZONES = {
    'HCMC': {
        'center': (10.7769, 106.6966),
        'radius': 0.03,  # ~3km
        'name': 'Ho Chi Minh City'
    },
    'Hanoi': {
        'center': (21.0285, 105.8542),
        'radius': 0.03,  # ~3km
        'name': 'Hanoi'
    },
    'Da Nang': {
        'center': (16.0544, 108.2022),
        'radius': 0.02,  # ~2km
        'name': 'Da Nang'
    }
}

class FakeVehicleGPS:
    def __init__(self, vehicle_id, vehicle_name, zone='HCMC'):
        self.vehicle_id = vehicle_id
        self.vehicle_name = vehicle_name
        self.zone = ZONES.get(zone, ZONES['HCMC'])
        self.access_token = None
        self.current_lat, self.current_lng = self.zone['center']
        
    def login(self):
        """Đăng nhập để lấy JWT token"""
        print(f"\n🔑 Đang đăng nhập...")
        try:
            response = requests.post(
                f"{BASE_URL}/login/",
                json={
                    "username": LOGIN_EMAIL,
                    "password": LOGIN_PASSWORD
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get('access')
                print(f"✅ Đăng nhập thành công!")
                print(f"   Token: {self.access_token[:50]}...")
                return True
            else:
                print(f"❌ Đăng nhập thất bại: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Lỗi kết nối: {e}")
            return False
    
    def generate_random_location(self):
        """Tạo tọa độ ngẫu nhiên trong khu vực"""
        center_lat, center_lng = self.zone['center']
        radius = self.zone['radius']
        
        # Tạo offset ngẫu nhiên
        lat_offset = random.uniform(-radius, radius)
        lng_offset = random.uniform(-radius, radius)
        
        new_lat = center_lat + lat_offset
        new_lng = center_lng + lng_offset
        
        return new_lat, new_lng
    
    def get_location_name(self, lat, lng):
        """Tạo tên địa điểm (giả lập)"""
        zone_name = self.zone['name']
        streets = ['Đường A', 'Đường B', 'Đường C', 'Phố D', 'Hẻm E']
        street = random.choice(streets)
        return f"{street}, {zone_name}"
    
    def update_location(self):
        """Cập nhật vị trí lên API"""
        if not self.access_token:
            print("❌ Chưa đăng nhập!")
            return False
        
        # Tạo vị trí ngẫu nhiên mới hoặc di chuyển nhỏ từ vị trí cũ
        if random.random() > 0.3:  # 70% di chuyển nhỏ từ vị trí cũ
            # Di chuyển nhỏ (giả lập xe đang chạy)
            self.current_lat += random.uniform(-0.003, 0.003)
            self.current_lng += random.uniform(-0.003, 0.003)
        else:
            # Teleport ngẫu nhiên (giả lập xe dừng ở chỗ khác)
            self.current_lat, self.current_lng = self.generate_random_location()
        
        location_name = self.get_location_name(self.current_lat, self.current_lng)
        
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "latitude": self.current_lat,
                "longitude": self.current_lng,
                "location_name": location_name
            }
            
            response = requests.post(
                f"{BASE_URL}/vehicles/{self.vehicle_id}/location/",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                print(f"✅ [{timestamp}] {self.vehicle_name} - "
                      f"Tọa độ: ({self.current_lat:.4f}, {self.current_lng:.4f}) - "
                      f"{location_name}")
                return True
            else:
                print(f"⚠️  Cập nhật thất bại (HTTP {response.status_code}): {response.text}")
                return False
        except Exception as e:
            print(f"❌ Lỗi gửi tọa độ: {e}")
            return False
    
    def run(self, interval=10, duration=None):
        """
        Chạy liên tục gửi tọa độ
        
        Args:
            interval: Khoảng thời gian giữa các lần update (giây)
            duration: Thời gian chạy tổng cộng (giây), None = chạy vô tận
        """
        if not self.login():
            print("❌ Không thể khởi động, lỗi đăng nhập!")
            return
        
        print(f"\n🚗 Bắt đầu giả lập xe: {self.vehicle_name}")
        print(f"   ID xe: {self.vehicle_id}")
        print(f"   Khu vực: {self.zone['name']}")
        print(f"   Khoảng update: {interval}s")
        if duration:
            print(f"   Thời gian chạy: {duration}s ({duration/60:.1f} phút)")
        else:
            print(f"   Chế độ: Chạy vô tận (Ctrl+C để dừng)")
        print()
        
        start_time = time.time()
        update_count = 0
        
        try:
            while True:
                # Kiểm tra nếu vượt quá duration
                if duration and (time.time() - start_time) > duration:
                    print(f"\n⏱️  Hết thời gian chạy ({duration}s)")
                    break
                
                # Cập nhật vị trí
                self.update_location()
                update_count += 1
                
                # Chờ trước update tiếp theo
                time.sleep(interval)
        
        except KeyboardInterrupt:
            print(f"\n\n⛔ Dừng bởi người dùng")
        finally:
            elapsed = time.time() - start_time
            print(f"\n📊 Thống kê:")
            print(f"   Tổng lần update: {update_count}")
            print(f"   Thời gian chạy: {elapsed:.1f}s ({elapsed/60:.1f} phút)")
            print(f"   Trung bình: {update_count/elapsed:.2f} update/s")


def print_banner():
    """In banner"""
    print("\n" + "="*60)
    print("  🚗 AutoRent - Fake Vehicle GPS Simulator")
    print("="*60)


def test_single_vehicle():
    """Test với 1 xe"""
    print_banner()
    
    vehicle = FakeVehicleGPS(
        vehicle_id=1,
        vehicle_name="Toyota Vios 2023 (SG-001-AA)",
        zone='HCMC'
    )
    
    # Chạy 30 lần update, mỗi lần 5 giây
    vehicle.run(interval=5, duration=150)  # 150s = 2.5 phút


def test_multiple_vehicles():
    """Test với nhiều xe cùng lúc (multi-threading)"""
    print_banner()
    print("⚠️  Chế độ nhiều xe (cần multiprocessing)")
    print("   Để test, hãy chạy multiple instances của script\n")
    
    from multiprocessing import Process
    
    vehicles_config = [
        (1, "Toyota Vios 2023 (SG-001-AA)", 'HCMC'),
        (2, "Honda City 2022 (SG-002-AA)", 'HCMC'),
        (7, "Toyota Camry 2022 (HN-001-AA)", 'Hanoi'),
    ]
    
    processes = []
    
    for vehicle_id, name, zone in vehicles_config:
        vehicle = FakeVehicleGPS(vehicle_id, name, zone)
        p = Process(target=vehicle.run, kwargs={'interval': 8, 'duration': 120})
        p.start()
        processes.append(p)
        time.sleep(1)  # Stagger the starts
    
    # Chờ tất cả process hoàn thành
    for p in processes:
        p.join()


def interactive_mode():
    """Chế độ tương tác - người dùng chọn xe"""
    print_banner()
    
    vehicles = {
        '1': (1, 'Toyota Vios (SG-001-AA)', 'HCMC'),
        '2': (2, 'Honda City (SG-002-AA)', 'HCMC'),
        '3': (3, 'Hyundai i10 (SG-003-AA)', 'HCMC'),
        '7': (7, 'Toyota Camry (HN-001-AA)', 'Hanoi'),
        '8': (8, 'Ford Ranger (HN-002-AA)', 'Hanoi'),
    }
    
    print("\n🚗 Chọn xe để giả lập:\n")
    for key, (vid, name, zone) in vehicles.items():
        print(f"  {key}: {name} ({zone})")
    print("  0: Thoát")
    
    choice = input("\nNhập lựa chọn: ").strip()
    
    if choice == '0':
        print("👋 Tạm biệt!")
        return
    
    if choice not in vehicles:
        print("❌ Lựa chọn không hợp lệ!")
        return
    
    vehicle_id, name, zone = vehicles[choice]
    
    interval = input("\nKhoảng update (giây) [default=5]: ").strip() or "5"
    try:
        interval = int(interval)
    except:
        interval = 5
    
    duration = input("Thời gian chạy (giây) [0=vô tận] [default=60]: ").strip() or "60"
    try:
        duration = int(duration) if int(duration) > 0 else None
    except:
        duration = 60
    
    vehicle = FakeVehicleGPS(vehicle_id, name, zone)
    vehicle.run(interval=interval, duration=duration)


if __name__ == '__main__':
    print("\n")
    print("╔════════════════════════════════════════════════════════╗")
    print("║       🚗 AutoRent Fake Vehicle GPS Simulator           ║")
    print("╚════════════════════════════════════════════════════════╝")
    print("\nChế độ:")
    print("  1. Single vehicle test (1 xe)")
    print("  2. Interactive mode (chọn xe)")
    print("  3. Test multiple vehicles (nhiều xe)")
    print()
    
    mode = input("Chọn chế độ [1-3] [default=1]: ").strip() or "1"
    
    if mode == "1":
        test_single_vehicle()
    elif mode == "2":
        interactive_mode()
    elif mode == "3":
        test_multiple_vehicles()
    else:
        print("❌ Chế độ không hợp lệ!")
