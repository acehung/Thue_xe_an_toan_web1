# 🎯 Quick Start - Vehicle Tracking System

## Bước 1: Chạy Setup

Mở terminal và chạy:

```bash
cd e:\autorent_backend
python setup_vehicle_tracking.py
```

Điều này sẽ:
✓ Tạo migration cho Vehicle model
✓ Áp dụng migration vào database  
✓ Tạo 10 xe mẫu (5 ở HCMC, 5 ở Hà Nội)
✓ Kiểm tra thiết lập

## Bước 2: Khởi động Server (nếu chưa chạy)

```bash
python manage.py runserver 127.0.0.1:8000
```

## Bước 3: Truy cập

### 🗺️ Bản đồ xe (Frontend chính)
http://127.0.0.1:8000/api/

Xem:
- Bản đồ tương tác với tất cả xe
- Marker theo trạng thái (xanh/cam/đỏ)
- Danh sách xe bên phải
- Thống kê số lượng xe
- Chi tiết xe khi click marker

### 📡 API Vehicles (JSON)
http://127.0.0.1:8000/api/vehicles/

Xem danh sách xe dạng JSON

### 🛠️ Admin Panel
http://127.0.0.1:8000/admin/

Đăng nhập với:
- Username: acehung
- Password: (superuser password)

Quản lý xe trong admin

## 📦 Files Được Tạo

### Models & Database
- `api/models.py` - Thêm Vehicle model
- Migration files - Cho Vehicle table

### Serializers & Views
- `api/serializers.py` - VehicleSerializer
- `api/views.py` - 4 API endpoints mới
- `api/urls.py` - URL routing
- `api/admin.py` - Vehicle admin interface

### Frontend
- `templates/vehicle_map.html` - Bản đồ Leaflet.js

### Scripts
- `setup_vehicle_tracking.py` - Setup chính
- `create_fake_vehicles.py` - Tạo dữ liệu mẫu
- `run_migrations.py` - Chạy migrations

### Documentation
- `VEHICLE_TRACKING_README.md` - Tài liệu chi tiết

## 🎮 Demo

### 1. Xem bản đồ
- Truy cập http://127.0.0.1:8000/api/
- Xem 10 xe trên bản đồ (5 ở HCMC, 5 ở Hà Nội)
- Click marker để xem chi tiết
- Click xe trong danh sách để zoom tới

### 2. Lấy dữ liệu qua API
```bash
curl http://127.0.0.1:8000/api/vehicles/
```

### 3. Cập nhật vị trí xe (cần JWT)
```bash
# Trước tiên login để lấy token
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser@example.com","password":"TestPass123"}'

# Dùng access token để cập nhật vị trí
curl -X POST http://127.0.0.1:8000/api/vehicles/1/location/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"latitude":10.777,"longitude":106.697,"location_name":"New Location"}'
```

## 🎨 Giao diện

```
┌─────────────────────────────────────────────────────────┐
│           🗺️ Bản đồ vị trí xe thuê                     │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────────────────────┬──────────────────┐ │
│  │                                  │  📊 Thống kê     │ │
│  │                                  │  ┌────────────┐  │ │
│  │         Leaflet Map              │  │ Tổng: 10   │  │ │
│  │    (OpenStreetMap + Markers)     │  │ Có sẵn: 8  │  │ │
│  │                                  │  │ Cho thuê:1 │  │ │
│  │    🟢 🟠 🔴                        │  │ Bảo trì: 1│  │ │
│  │    (Markers theo status)         │  └────────────┘  │ │
│  │                                  │                  │ │
│  │                                  │  🚗 Danh sách    │ │
│  │                                  │  ┌────────────┐  │ │
│  │                                  │  │ SG-001-AA  │  │ │
│  │                                  │  │ SG-002-AA  │  │ │
│  │                                  │  │ ...        │  │ │
│  │                                  │  └────────────┘  │ │
│  └──────────────────────────────────┴──────────────────┘ │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

## 🔑 API Endpoints

```
GET  /api/vehicles/              - Lấy danh sách xe
GET  /api/vehicles/<id>/         - Lấy chi tiết xe
POST /api/vehicles/<id>/location/ - Cập nhật vị trí (cần auth)
```

## 📍 Dữ liệu mẫu

**HCMC (5 xe):**
- SG-001-AA: Toyota Vios (District 1)
- SG-002-AA: Honda City (District 3)
- SG-003-AA: Hyundai i10 (District 7)
- SG-004-AA: Toyota Fortuner (Thu Duc)
- SG-005-AA: Kia Cerato (Binh Thanh)

**Hanoi (5 xe):**
- HN-001-AA: Toyota Camry (Hoan Kiem)
- HN-002-AA: Ford Ranger (Cau Giay)
- HN-003-AA: Honda Civic (Ba Dinh)
- HN-004-AA: Mazda CX-5 (Dong Da)

## ✅ Checklist

- [ ] Chạy `python setup_vehicle_tracking.py`
- [ ] Server đang chạy trên port 8000
- [ ] Truy cập http://127.0.0.1:8000/api/ thấy bản đồ
- [ ] Xem được 10 xe trên bản đồ
- [ ] Click marker có popup chi tiết
- [ ] Admin panel có Vehicle management
- [ ] API /api/vehicles/ trả về JSON

## 🐛 Troubleshooting

**Q: Bản đồ không load?**
A: Kiểm tra internet (cần OpenStreetMap), check browser console

**Q: Xe không hiển thị?**
A: Chạy `python setup_vehicle_tracking.py` lại

**Q: Lỗi API?**
A: Kiểm tra logs: `logs/django.log`

**Q: Cập nhật vị trí không được?**
A: Cần JWT token từ login, dùng POST endpoint

## 🚀 Mở rộng

Bạn có thể:
- Thêm real-time updates (WebSocket)
- Tracking history cho mỗi xe
- Route optimization
- Heatmap xe tập trung
- Driver alerts
- Integration GPS device thực

---

**Hãy vui lòi! Hệ thống tracking xe thực thời đã sẵn sàng! 🎉**
