# 🗺️ AutoRent Vehicle Tracking System

## Tổng quan

Hệ thống theo dõi vị trí xe thuê thực thời với bản đồ tương tác sử dụng **Leaflet.js** và **OpenStreetMap**. Cho phép quan sát vị trí GPS của tất cả xe trong hệ thống AutoRent.

## 🎯 Tính năng

- ✅ **Bản đồ tương tác** - Hiển thị tất cả xe trên bản đồ OpenStreetMap
- ✅ **Vị trí GPS thực thời** - Tọa độ lat/lng cho mỗi xe
- ✅ **Trạng thái xe** - Available, Rented, Maintenance, Inactive
- ✅ **Danh sách xe động** - Danh sách có thể click để định vị
- ✅ **Thống kê** - Tổng số xe, xe có sẵn, đang cho thuê, bảo trì
- ✅ **Chi tiết xe** - Tên, biển số, loại xe, giá, v.v.
- ✅ **Cập nhật vị trí** - API endpoint để cập nhật tọa độ GPS
- ✅ **Responsive Design** - Hoạt động tốt trên desktop và mobile
- ✅ **Admin Panel** - Quản lý xe trong Django admin

## 📦 Cài đặt & Thiết lập

### 1. Chạy Setup Script

```bash
cd e:\autorent_backend
python setup_vehicle_tracking.py
```

Script sẽ:
- Tạo migration cho model Vehicle
- Áp dụng migration vào database
- Tạo 10 xe mẫu tại các địa điểm ở HCMC và Hà Nội
- Kiểm tra thiết lập

### 2. Khởi động Server

```bash
python manage.py runserver 127.0.0.1:8000
```

### 3. Truy cập

- **Bản đồ xe:** http://127.0.0.1:8000/api/
- **API Vehicles:** http://127.0.0.1:8000/api/vehicles/
- **Admin Panel:** http://127.0.0.1:8000/admin/

## 🏗️ Kiến trúc

### Model: Vehicle

```python
class Vehicle(models.Model):
    name = CharField()              # Tên xe
    license_plate = CharField()     # Biển số (unique)
    vehicle_type = CharField()      # Loại: Sedan, SUV, Van, etc
    latitude = FloatField()         # Vĩ độ
    longitude = FloatField()        # Kinh độ
    location_name = CharField()     # Tên địa điểm
    status = CharField(choices=[    # Trạng thái
        'available',                # Có sẵn
        'rented',                   # Đang cho thuê
        'maintenance',              # Bảo trì
        'inactive'                  # Không hoạt động
    ])
    color = CharField()             # Màu sắc
    year = IntegerField()           # Năm sản xuất
    price_per_day = DecimalField()  # Giá thuê/ngày
    last_location_update = DateTime # Cập nhật lần cuối
    created_at = DateTime()         # Tạo
    updated_at = DateTime()         # Cập nhật
```

### API Endpoints

#### 1. Lấy danh sách xe
```
GET /api/vehicles/
Content-Type: application/json

Response:
{
    "success": true,
    "count": 10,
    "vehicles": [
        {
            "id": 1,
            "name": "Toyota Vios 2023",
            "license_plate": "SG-001-AA",
            "vehicle_type": "Sedan",
            "latitude": 10.7769,
            "longitude": 106.6966,
            "location_name": "District 1, HCMC",
            "status": "available",
            "color": "White",
            "year": 2023,
            "price_per_day": "500000.00",
            "last_location_update": "2026-05-28T14:00:00Z"
        },
        ...
    ]
}
```

#### 2. Lấy chi tiết xe
```
GET /api/vehicles/{vehicle_id}/
Content-Type: application/json

Response:
{
    "success": true,
    "vehicle": { ... }
}
```

#### 3. Cập nhật vị trí GPS (Yêu cầu xác thực)
```
POST /api/vehicles/{vehicle_id}/location/
Authorization: Bearer {access_token}
Content-Type: application/json

Request:
{
    "latitude": 10.7769,
    "longitude": 106.6966,
    "location_name": "New Location"
}

Response:
{
    "success": true,
    "message": "Cập nhật vị trí thành công",
    "vehicle": { ... }
}
```

## 🗺️ Frontend (Leaflet.js)

### Trang bản đồ tương tác

**URL:** http://127.0.0.1:8000/api/

**Tính năng:**
- Bản đồ tương tác với OpenStreetMap
- Marker cho mỗi xe với icon theo trạng thái
  - 🟢 Green: Có sẵn
  - 🟠 Orange: Đang cho thuê
  - 🔴 Red: Bảo trì
- Click marker để xem chi tiết xe
- Danh sách xe bên phải với tìm kiếm nhanh
- Thống kê số xe theo trạng thái
- Nút "Làm mới" để reload dữ liệu
- Nút "Đặt lại bản đồ" để reset view

### Responsive Design
- Desktop: Bản đồ + Sidebar
- Mobile: Bản đồ full width với bottom sheet

## 🔧 Script giả backend (Fake Backend)

### Tạo dữ liệu giả

```python
# create_fake_vehicles.py
from api.models import Vehicle
from decimal import Decimal

vehicles_data = [
    {
        'name': 'Toyota Vios 2023',
        'license_plate': 'SG-001-AA',
        'vehicle_type': 'Sedan',
        'latitude': 10.7769,
        'longitude': 106.6966,
        'location_name': 'District 1, HCMC',
        'status': 'available',
        'color': 'White',
        'year': 2023,
        'price_per_day': Decimal('500000'),
    },
    # ... more vehicles
]

for vehicle_data in vehicles_data:
    Vehicle.objects.create(**vehicle_data)
```

### Cập nhật vị trí động

Bạn có thể dùng script Python để cập nhật vị trí xe định kỳ:

```python
import requests
import json
import time
import random

BASE_URL = "http://127.0.0.1:8000/api"
TOKEN = "your_jwt_access_token"

while True:
    vehicles = requests.get(f"{BASE_URL}/vehicles/").json()['vehicles']
    
    for vehicle in vehicles:
        # Thay đổi tọa độ ngẫu nhiên (delta nhỏ)
        new_lat = vehicle['latitude'] + random.uniform(-0.01, 0.01)
        new_lng = vehicle['longitude'] + random.uniform(-0.01, 0.01)
        
        # Cập nhật vị trí
        requests.post(
            f"{BASE_URL}/vehicles/{vehicle['id']}/location/",
            headers={"Authorization": f"Bearer {TOKEN}"},
            json={"latitude": new_lat, "longitude": new_lng}
        )
    
    time.sleep(30)  # Update every 30 seconds
```

## 📊 Admin Panel

### Quản lý xe

**URL:** http://127.0.0.1:8000/admin/api/vehicle/

**Tính năng:**
- Danh sách tất cả xe với lọc theo trạng thái, loại, năm
- Tìm kiếm theo tên, biển số, địa điểm
- Hiển thị trạng thái với màu sắc
- Chỉnh sửa thông tin xe
- Cập nhật tọa độ GPS
- Quản lý giá thuê

## 🔐 Bảo mật

- ✅ API cập nhật vị trí yêu cầu JWT authentication
- ✅ Chỉ superuser có thể cập nhật vị trí
- ✅ Audit logging tất cả thay đổi
- ✅ CORS được cấu hình cho API

## 📝 Dữ liệu mẫu

### Xe tại HCMC
1. **Toyota Vios 2023** (SG-001-AA) - Sedantrắng - 500k/ngày - District 1
2. **Honda City 2022** (SG-002-AA) - Sedan bạc - 450k/ngày - District 3
3. **Hyundai i10 2023** (SG-003-AA) - Hatchback đỏ - 350k/ngày - District 7
4. **Toyota Fortuner 2022** (SG-004-AA) - SUV đen - 900k/ngày - Thu Duc
5. **Kia Cerato 2021** (SG-005-AA) - Sedan xanh - 550k/ngày - Binh Thanh
6. **Mitsubishi Xpander 2023** (SG-006-AA) - MPV đỏ - 700k/ngày - District 5

### Xe tại Hà Nội
7. **Toyota Camry 2022** (HN-001-AA) - Sedan trắng - 800k/ngày - Hoan Kiem
8. **Ford Ranger 2023** (HN-002-AA) - Pickup xám - 750k/ngày - Cau Giay
9. **Honda Civic 2021** (HN-003-AA) - Sedan đen - 650k/ngày - Ba Dinh
10. **Mazda CX-5 2023** (HN-004-AA) - SUV bạc - 900k/ngày - Dong Da

## 🎨 Công nghệ sử dụng

- **Backend:**
  - Django 6.0.5
  - Django REST Framework
  - SQLite Database
  - Python 3.x

- **Frontend:**
  - Leaflet.js (Bản đồ)
  - OpenStreetMap (Dữ liệu bản đồ)
  - Font Awesome (Icon)
  - Vanilla JavaScript
  - CSS3 (Responsive)

- **Khác:**
  - JWT Authentication
  - RESTful API
  - JSON Data Format

## 📱 Responsive

- ✅ Desktop (1400px+)
- ✅ Tablet (768px - 1024px)
- ✅ Mobile (< 768px)

## 🚀 Tối ưu hóa tương lai

- [ ] Real-time GPS updates với WebSocket
- [ ] Lịch sử vị trí (tracking history)
- [ ] Heatmap xe tập trung
- [ ] Route planning & optimization
- [ ] Geofencing alerts
- [ ] Driver behavior analytics
- [ ] Predictive maintenance
- [ ] Integration với GPS device

## 📞 Support

Nếu gặp vấn đề:
1. Kiểm tra logs: `logs/django.log`, `logs/audit.log`
2. Xem admin panel để kiểm tra dữ liệu
3. Test API endpoints với Postman
4. Xem browser console cho lỗi frontend

## 📄 License

Phần của dự án AutoRent Vehicle Rental System
