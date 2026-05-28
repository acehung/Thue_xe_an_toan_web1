# 🚗 Hướng Dẫn Quản Lý An Toàn Ô Tô Cho Thuê

## 📌 Mục Đích

Đảm bảo an toàn thông tin khách hàng, bảo vệ tài sản xe, và quản lý rủi ro khi khách thuê mang xe đi xa.

---

## 1️⃣ QUẢN LÝ THÔNG TIN & DANH TÍNH

### 1.1 Xác Minh Danh Tính Khách Hàng

- ✅ Yêu cầu CCCD/CMND hợp lệ (kiểm tra ngày hết hạn)
- ✅ Lưu ảnh CCCD mặt trước & mặt sau
- ✅ Lưu ảnh chứng minh thư giao dịch (selfie + CCCD)
- ✅ Xác minh số điện thoại qua OTP
- ✅ Kiểm tra chứng minh thư qua cơ sở dữ liệu (nếu có)

### 1.2 Kiểm Tra Bằng Lái Xe

- ✅ Yêu cầu ảnh bằng lái xe hợp lệ
- ✅ Kiểm tra loại bằng lái (phải phù hợp với loại xe)
- ✅ Kiểm tra ngày hết hạn bằng
- ✅ Lưu thông tin: số bằng, ngày cấp, ngày hết hạn
- ✅ Kiểm tra lịch sử vi phạm (nếu có API)

### 1.3 Lịch Sử Tài Khoản

- ✅ Lưu trữ số lần thuê xe
- ✅ Xếp hạng tín chỉ khách hàng (0-5 sao)
- ✅ Theo dõi các lần vi phạm, cộc xe sớm
- ✅ Cảnh báo nếu khách có lịch sử xấu

---

## 2️⃣ QUẢN LÝ HỢP ĐỒNG & HỘI NHẬP

### 2.1 Hợp Đồng Thuê Xe

```
Hợp đồng phải bao gồm:
- Thông tin khách hàng (CCCD, số điện thoại)
- Thông tin xe (BKS, chủng loại, số khung, số máy)
- Thời gian thuê (ngày bắt đầu, ngày kết thúc)
- Chi phí thuê và các khoản phí phát sinh
- Điều khoản bảo hiểm, bồi thường thiệt hại
- Giới hạn quãng đường, tốc độ
- Danh sách các hành vi cấm
- Chữ ký điện tử (ngày hiện tại)
```

### 2.2 Điều Kiện Thuê Xe

- ✅ Khách tối thiểu 18 tuổi, tối đa tuổi quy định
- ✅ Bằng lái phải còn hạn ít nhất 6 tháng
- ✅ Tài khoản phải đã xác minh danh tính
- ✅ Không được thuê nếu có vấn đề pháp lý gần đây
- ✅ Yêu cầu đặt cọc (% nhất định so với giá thuê)

---

## 3️⃣ QUẢN LÝ VỊ TRÍ & THEO DÕI THỜI GIAN THỰC

### 3.1 Hệ Thống GPS Theo Dõi

```python
# Dữ liệu cần lưu:
- Vị trí hiện tại (latitude, longitude)
- Timestamp (thời gian update)
- Quãng đường đã đi
- Tốc độ hiện tại
- Lịch sử di chuyển (mỗi 5 phút)
```

### 3.2 Cảnh Báo Vị Trí

- ✅ **Geofencing**: Cảnh báo nếu xe rời khỏi vùng cho phép
- ✅ **Khoảng cách tối đa**: Khách không được mang xe vượt quá X km
- ✅ **Ngoài giờ cấm**: Cảnh báo nếu sử dụng xe ngoài giờ quy định
- ✅ **Di chuyển bất thường**: Cảnh báo nếu xe chuyển động đột ngột

### 3.3 Các Vùng Bị Cấm

- ❌ Vùng núi, rừng sâu
- ❌ Biên giới quốc gia
- ❌ Vùng chiến sự/động loạn
- ❌ Đường xấu, không có bảo hiểm

---

## 4️⃣ QUẢN LÝ TÌNH TRẠNG XE

### 4.1 Kiểm Tra Trước Khi Giao Xe

```
Bảng Kiểm Tra (Checklist):
☐ Kiểm tra ngoại thất (vết cát, vết trầy, dent)
☐ Kiểm tra nội thất (ghế, kính, khoá khóa)
☐ Kiểm tra dầu nhớt, nước làm mát
☐ Kiểm tra lốp xe, áp suất
☐ Kiểm tra phanh, vô lăng
☐ Kiểm tra các thiết bị: đèn, gạt mưa, máy lạnh
☐ Chụp ảnh 360° xe từ 4 góc
☐ Chụp ảnh giàn hàng, nội thất
☐ Ghi lại mô-đô (km) hiện tại
```

### 4.2 Kiểm Tra Sau Khi Nhận Lại Xe

```
So sánh với trạng thái ban đầu:
☐ Ngoại thất có thêm vết trầy, cát, cấn gì không?
☐ Nội thất có vết bẩn, xé rách không?
☐ Mô-đô tăng bao nhiêu km?
☐ Dầu nhớt, nước làm mát có bình thường?
☐ Lốp xe còn tốt không?
☐ Có mùi lạ, mùi thuốc lá không?
☐ Thiết bị có hoạt động bình thường?
```

### 4.3 Hệ Thống Đánh Giá Tình Trạng

- ⭐ **Tuyệt vời** (0-5%): Xe đẹp như mới
- ⭐⭐ **Tốt** (5-15%): Có vết nhỏ, không ảnh hưởng an toàn
- ⭐⭐⭐ **Bình thường** (15-30%): Có vết trầy, nhỏ xước
- ⭐⭐⭐⭐ **Cần sửa** (30-50%): Cấn, nứt kính
- ⭐⭐⭐⭐⭐ **Hỏng nặng** (>50%): Không thể sử dụng

---

## 5️⃣ QUẢN LÝ NHIÊN LIỆU & KHÍ THẢI

### 5.1 Kiểm Tra Nhiên Liệu

```
- Lúc giao xe: Ghi lại mức xăng (% hoặc lít)
- Lúc nhận lại: Kiểm tra mức xăng
- Yêu cầu: Khách phải trả xe với mức xăng tương tự
- Phí phụ: Nếu thiếu xăng, tính phí x1.5 giá thị trường
```

### 5.2 Giới Hạn Quãng Đường

```
- Thuê hàng ngày: Max 100 km/ngày
- Thuê tuần: Max 500 km/tuần
- Thuê tháng: Max 2000 km/tháng
- Vượt quá: Tính phí thêm 5.000 đ/km
```

### 5.3 Cảnh Báo Tiêu Hao Nhiên Liệu

- ⚠️ Nếu tiêu hao > 150% bình thường → cảnh báo lái xe xạo (kiểng chân ga)
- ⚠️ Nếu vận tốc trung bình > 80 km/h → tiêu hao cao

---

## 6️⃣ QUẢN LÝ HÀNH VI & AN TOÀN GIAO THÔNG

### 6.1 Giới Hạn Tốc Độ

```
- Trong thành phố: Max 50 km/h
- Đường cao tốc: Max 100 km/h
- Đường phố nhỏ: Max 30 km/h
- Cảnh báo: SMS/App khi vượt quá 10% giới hạn
- Phạt: 2.000 - 5.000 đ/lần vượt quá 20%
```

### 6.2 Hành Vi Nguy Hiểm

- ⚠️ Phanh gấp đột ngột
- ⚠️ Quay cuộn vô lăng nhanh
- ⚠️ Sử dụng điện thoại khi lái xe (qua camera)
- ⚠️ Lái xe ban đêm (22:00 - 06:00) - nếu cấm

### 6.3 Theo Dõi Bằng Camera

- 📹 Lắp camera hành trình trên xe
- 📹 Ghi hình 24/7, lưu khoảng 48 giờ
- 📹 Xem lại video khi có va chạm/tai nạn
- 📹 Bảo vệ quyền lợi cả 2 bên (chủ xe vs khách)

---

## 7️⃣ QUẢN LÝ BẢO HIỂM & BỒI THƯỜNG

### 7.1 Loại Bảo Hiểm

```
1. Bảo hiểm bắt buộc (TNDS - Trách Nhiệm Dân Sự)
   - Bảo vệ bên thứ 3
   - Bắt buộc khi đăng ký xe

2. Bảo hiểm toàn bộ (Comprehensive)
   - Bảo vệ chính xe
   - Bao gồm: Cháy, cạnh, trộm, tai nạn

3. Bảo hiểm khách hàng (Passenger Insurance)
   - Bảo hiểm cho hành khách
   - Bảo vệ y tế, bồi thường tử vong
```

### 7.2 Mức Bồi Thường

```
- Vết nhỏ (< 500.000 đ): Khách trả 100%
- Vết vừa (500.000 - 2.000.000 đ): Khách trả 80%, BH trả 20%
- Vết lớn (> 2.000.000 đ): BH xử lý, Khách đặt cọc
- Toàn bộ xe hỏng: BH xử lý, Khách không chịu trách nhiệm
```

### 7.3 Quy Trình Khiếu Nại

1. Khách báo cáo sự cố trong vòng 24 giờ
2. Chụp ảnh bằng chứng, lấy biên bản cảnh sát (nếu cần)
3. Công ty gửi kỹ sư thẩm định
4. Lập báo cáo thẩm định + dự toán
5. Khách/BH thỏa thuận chi phí
6. Sửa chữa tại garage ủy quyền
7. Thanh toán và giải quyết

---

## 8️⃣ QUẢN LÝ THANH TOÁN & ĐẶT CỌC

### 8.1 Hình Thức Thanh Toán

- 💳 Thẻ tín dụng/ghi nợ
- 💸 Ví điện tử (Momo, Zalopay, etc.)
- 🏦 Chuyển khoản ngân hàng
- 💰 Tiền mặt (tùy chọn)

### 8.2 Đặt Cọc

```
Mức cọc tối thiểu:
- Thuê hàng ngày: 50% giá thuê
- Thuê tuần: 30% giá thuê
- Thuê tháng: 20% giá thuê
- Tối thiểu: 2.000.000 đ

Hoàn lại cọc:
- Không có vấn đề → Hoàn 100% trong 3 ngày
- Có vết nhỏ → Giữ lại 10-20%
- Có vết lớn → Giữ lại thêm để sửa chữa
```

### 8.3 Phí Phụ

```
- Giao/Nhận xe ngoài giờ: +500k
- Giao/Nhận ngoài khu vực: +100k/km
- Chưởng thêm người lái: +300k/người
- Chươngthêm trẻ em: Yêu cầu ghế an toàn
- Muộn hôm: 500k/giờ (từ giờ thứ 1)
```

---

## 9️⃣ QUẢN LÝ LIÊN LẠC & HỖ TRỢ KHÁCH HÀNG

### 9.1 Các Kênh Liên Lạc

- 📱 **24/7 Hotline**: 1900-xxxx (có tư vấn viên)
- 📲 **Chat App**: In-app messaging (trả lời < 15 phút)
- 📧 **Email**: support@autorent.vn (trả lời < 24 giờ)
- 📍 **Văn phòng**: Hỗ trợ trực tiếp

### 9.2 Tình Huống Khẩn Cấp

```
1. Tai nạn giao thông:
   - Gọi 113 (cảnh sát giao thông)
   - Gọi 112 (cấp cứu)
   - Báo cho AutoRent trong vòng 30 phút

2. Xe bị trộm:
   - Gọi 110 (cảnh sát)
   - Báo cho AutoRent trong vòng 1 giờ

3. Xe hỏng giữa đường:
   - Gọi dịch vụ cứu hộ (AutoRent cấp số)
   - Đợi tại xe an toàn
```

### 9.3 Đánh Giá & Phản Hồi

- ⭐ Yêu cầu đánh giá sau mỗi lần thuê
- 💬 Thu thập nhận xét, góp ý từ khách
- 🔧 Giải quyết khiếu nại trong 48 giờ
- 🎁 Thưởng khách tốt: Điểm tích lũy, giảm giá tiếp theo

---

## 🔟 QUẢN LÝ CÁC TÌNH HUỐNG ĐẶC BIỆT

### 10.1 Khách Là Công Ty/Tổ Chức

- ✅ Yêu cầu hợp đồng B2B
- ✅ Kiểm tra tình hình tài chính công ty
- ✅ Yêu cầu thêm đặt cọc
- ✅ Giao/Nhận theo yêu cầu đặc biệt

### 10.2 Khách Du Lịch Nước Ngoài

- 🌍 Yêu cầu hộ chiếu + visa hợp lệ
- 🌍 Yêu cầu Quốc tế Bằng lái (IDP - International Driving Permit)
- 🌍 Bằng lái nước ngoài phải được công chứng
- 🌍 Yêu cầu đặt cọc cao hơn (tối thiểu 5.000.000 đ)

### 10.3 Các Trường Hợp Từ Chối

- ❌ Khách dưới 18 tuổi
- ❌ Bằng lái hết hạn hoặc sắp hết hạn (< 3 tháng)
- ❌ Khách có lịch sử lái xe nguy hiểm
- ❌ Khách bị tình nghi giả mạo danh tính
- ❌ Khách không có phương tiện thanh toán hợp lệ
- ❌ Khách có lịch sử vi phạm với AutoRent

---

## 🛡️ QUẢN LÝ DỮ LIỆU & BẢO MẬT

### 11.1 Bảo Vệ Dữ Liệu Cá Nhân

```
GDPR & Luật Bảo Vệ Thông Tin:
- Mã hóa mật khẩu (bcrypt, Argon2)
- Mã hóa HTTPS/TLS cho tất cả kết nối
- Không lưu toàn bộ số CCCD (chỉ lưu mã băm)
- Không lưu toàn bộ số thẻ tín dụng (chỉ 4 số cuối)
- Xóa dữ liệu sau 90 ngày không hoạt động
- Tuân thủ quy định bảo vệ dữ liệu cá nhân VN
```

### 11.2 Bảo Mật Tài Khoản

- 🔐 Xác thực 2 yếu tố (2FA) bắt buộc
- 🔐 Mã OTP hết hạn sau 10 phút
- 🔐 Khóa tài khoản sau 5 lần nhập sai mật khẩu
- 🔐 Thông báo đăng nhập mới từ thiết bị/IP lạ

### 11.3 Audit Log

```
Lưu trữ:
- Ai truy cập thông tin nào
- Lúc nào truy cập
- IP address truy cập từ đâu
- Hành động thực hiện
- Kết quả (thành công/thất bại)
```

---

## 📋 BẢNG KIỂM TRA CUỐI CÙNG

```
✅ TRƯỚC KHI GIAO XE:
☐ Khách đã xác minh danh tính?
☐ Bằng lái còn hạn?
☐ Đã ký hợp đồng?
☐ Đã đặt cọc?
☐ Đã kiểm tra tình trạng xe?
☐ Đã chụp ảnh 360°?
☐ GPS, camera đã bật?
☐ Ghi lại mô-đô xe?
☐ Ghi lại mức xăng?

✅ TRONG QUÁ TRÌNH THUÊ:
☐ Theo dõi vị trí xe thường xuyên?
☐ Cảnh báo vượt quá giới hạn?
☐ Cảnh báo vượt tốc độ?
☐ Kiểm tra lịch sử di chuyển?
☐ Sẵn sàng xử lý khẩn cấp?

✅ LÚC NHẬN LẠI XE:
☐ Kiểm tra tình trạng xe?
☐ Ghi lại mô-đô mới?
☐ Ghi lại mức xăng?
☐ So sánh với tình trạng ban đầu?
☐ Tính toán phí phụ (nếu có)?
☐ Hoàn lại/giữ lại cọc?
☐ Yêu cầu đánh giá từ khách?
☐ Tạo báo cáo chi tiết?
```

---

## 📞 THÔNG TIN LIÊN LẠC LIÊN QUAN

- **Cảnh sát giao thông**: 113
- **Cấp cứu**: 112
- **Cảnh sát**: 110
- **Dịch vụ cứu hộ đường bộ**: 18001811
- **Bảo hiểm**: Liên hệ công ty bảo hiểm hợp tác

---

**Tài liệu này cần được cập nhật thường xuyên dựa trên các thay đổi pháp luật và kinh nghiệm thực tế.**

_Cập nhật lần cuối: Tháng 5, 2026_
