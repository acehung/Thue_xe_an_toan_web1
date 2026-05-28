# 🚗 AutoRent Fake Vehicle GPS Simulator

Script Python giả lập xe GPS gửi tọa độ ngẫu nhiên lên API Backend để test hệ thống theo dõi vị trí thực thời.

## 📦 Yêu cầu

```bash
pip install requests
```

## 🚀 Cách sử dụng

### Phiên bản đơn giản (Khuyến khích)

```bash
cd e:\autorent_backend
python fake_vehicle_simple.py
```

**Tùy chọn:**

```bash
# Xe ID 1, update mỗi 5 giây
python fake_vehicle_simple.py

# Xe ID 2, update mỗi 3 giây
python fake_vehicle_simple.py --vehicle-id 2 --interval 3

# Xe ID 7 (Hanoi), chạy 2 phút
python fake_vehicle_simple.py --vehicle-id 7 --duration 120

# Hiển thị danh sách xe
python fake_vehicle_simple.py --list

# Xe ID 4, update mỗi 10s, chạy 5 phút
python fake_vehicle_simple.py --vehicle-id 4 --interval 10 --duration 300
```

## 📋 Danh sách xe

```
ID 1: Toyota Vios 2023 (SG-001-AA) - HCMC District 1
ID 2: Honda City 2022 (SG-002-AA) - HCMC District 3
ID 3: Hyundai i10 2023 (SG-003-AA) - HCMC District 7
ID 4: Toyota Fortuner 2022 (SG-004-AA) - HCMC Thu Duc
ID 5: Kia Cerato 2021 (SG-005-AA) - HCMC Binh Thanh
ID 6: Mitsubishi Xpander 2023 (SG-006-AA) - HCMC District 5
ID 7: Toyota Camry 2022 (HN-001-AA) - Hanoi Hoan Kiem
ID 8: Ford Ranger 2023 (HN-002-AA) - Hanoi Cau Giay
ID 9: Honda Civic 2021 (HN-003-AA) - Hanoi Ba Dinh
ID 10: Mazda CX-5 2023 (HN-004-AA) - Hanoi Dong Da
```

## 🎯 Ví dụ

### Test 1: Xe tại HCMC

```bash
python fake_vehicle_simple.py --vehicle-id 1 --interval 5
```

Output:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔑 Đang đăng nhập...
✅ Đăng nhập thành công!

================================================================================
🚗 Xe: Toyota Vios 2023 (SG-001-AA)
📍 Khu vực: HCMC District 1
⏱️  Update: mỗi 5s
⏰ Chế độ: Chạy liên tục (Ctrl+C để dừng)
================================================================================

✅ 14:05:23 | Toyota Vios 2023 (SG-001-AA)           | (10.7769, 106.6966)
✅ 14:05:28 | Toyota Vios 2023 (SG-001-AA)           | (10.7755, 106.6980)
✅ 14:05:33 | Toyota Vios 2023 (SG-001-AA)           | (10.7741, 106.6958)
✅ 14:05:38 | Toyota Vios 2023 (SG-001-AA)           | (10.7768, 106.7005)
✅ 14:05:43 | Toyota Vios 2023 (SG-001-AA)           | (10.7722, 106.6945)

⛔ Dừng!

📊 Kết quả: 5 updates trong 20.1s
```

### Test 2: Multiple Xe (chạy nhiều terminal)

Terminal 1:
```bash
python fake_vehicle_simple.py --vehicle-id 1
```

Terminal 2:
```bash
python fake_vehicle_simple.py --vehicle-id 7 --interval 3
```

Terminal 3:
```bash
python fake_vehicle_simple.py --vehicle-id 4 --interval 7
```

Lúc này 3 xe sẽ gửi tọa độ đồng thời lên server!

### Test 3: Chạy 5 phút rồi dừng

```bash
python fake_vehicle_simple.py --vehicle-id 2 --duration 300
```

## 🔍 Xem kết quả

### 1. Trên bản đồ (Real-time)
```
http://127.0.0.1:8000/api/
```

Bạn sẽ thấy xe di chuyển trên bản đồ!

### 2. API (JSON)
```bash
curl http://127.0.0.1:8000/api/vehicles/
```

### 3. Admin Panel
```
http://127.0.0.1:8000/admin/
```

Admin → API → Vehicle → Xem danh sách xe với tọa độ mới nhất

## 🏗️ Cách hoạt động

```
┌──────────────────────────────────────────────────┐
│ 1. Script login                                  │
│    → Gửi: username + password                    │
│    ← Nhận: JWT access token                      │
└──────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────┐
│ 2. Loop vô tận (hoặc duration)                   │
│    Mỗi lần:                                      │
│    - Tạo tọa độ ngẫu nhiên/di chuyển nhỏ       │
│    - Gửi POST /api/vehicles/{id}/location/      │
│    - Header: Authorization: Bearer {token}      │
│    - Body: {"latitude": ..., "longitude": ...}  │
│    - Delay interval giây                        │
└──────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────┐
│ 3. Backend API                                   │
│    - Xác thực token                              │
│    - Cập nhật tọa độ trong database               │
│    - Ghi audit log                               │
│    - Return: HTTP 200 + vehicle data             │
└──────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────┐
│ 4. Frontend (Bản đồ)                             │
│    - GET /api/vehicles/                          │
│    - Vẽ marker trên Leaflet map                  │
│    - Auto-refresh                                │
└──────────────────────────────────────────────────┘
```

## 📊 Test Scenarios

### Scenario 1: Single Vehicle Test
```bash
python fake_vehicle_simple.py --vehicle-id 1 --interval 5 --duration 60
```
- Kiểm tra 1 xe gửi tọa độ liên tục 1 phút
- Xem bản đồ cập nhật

### Scenario 2: Load Test
```bash
# Terminal 1
python fake_vehicle_simple.py --vehicle-id 1 --interval 3

# Terminal 2
python fake_vehicle_simple.py --vehicle-id 2 --interval 3

# Terminal 3
python fake_vehicle_simple.py --vehicle-id 3 --interval 3

# Terminal 4
python fake_vehicle_simple.py --vehicle-id 7 --interval 3

# Terminal 5
python fake_vehicle_simple.py --vehicle-id 8 --interval 3
```
- 5 xe gửi tọa độ cùng lúc mỗi 3s
- Kiểm tra server có xử lý được không

### Scenario 3: Real-time Tracking
```bash
# Terminal 1
python fake_vehicle_simple.py --vehicle-id 1

# Terminal 2 - Watch updates
watch -n 2 'curl -s http://127.0.0.1:8000/api/vehicles/1/ | jq .vehicle'
```
- Chạy xe ngẫu nhiên
- Watch API để thấy tọa độ thay đổi real-time

### Scenario 4: Geo-distributed Test
```bash
# HCMC xe
python fake_vehicle_simple.py --vehicle-id 1 --interval 5

# Hanoi xe
python fake_vehicle_simple.py --vehicle-id 7 --interval 5
```
- Xe ở 2 thành phố khác nhau gửi tọa độ
- Xem bản đồ show 2 khu vực địa lý

## 🐛 Troubleshooting

**Q: Lỗi "Connection refused"**
```
A: Kiểm tra server Django đang chạy
   python manage.py runserver 127.0.0.1:8000
```

**Q: Lỗi "Authentication failed"**
```
A: Kiểm tra tài khoản:
   - Email: testuser@example.com
   - Password: TestPass123
   
   Hoặc tạo user mới:
   python manage.py createsuperuser
```

**Q: Lỗi "Vehicle not found"**
```
A: Chạy setup_vehicle_tracking.py trước:
   python setup_vehicle_tracking.py
```

**Q: Bản đồ không cập nhật**
```
A: Reload trang bản đồ: http://127.0.0.1:8000/api/
   Xem browser console (F12) kiểm tra lỗi
```

## 📈 Hiệu suất

- **Throughput:** ~2-3 requests/giây (1 xe mỗi 5s = 0.2 req/s)
- **Load test:** 10 xe × 0.2 req/s = 2 req/s
- **Latency:** ~100-200ms per request
- **Memory:** ~30MB per instance

## 🔐 Bảo mật

- ✅ Sử dụng JWT token
- ✅ Requires authentication
- ✅ Logs tất cả updates
- ✅ Only update owned vehicle locations

## 🚀 Mở rộng

Bạn có thể:
- Thêm real GPS coordinates
- Integrate với GPS device thực
- Simulate traffic/delays
- Create custom routes
- Test stress với 1000+ vehicles

---

**Hãy chạy thử!** 🎉
