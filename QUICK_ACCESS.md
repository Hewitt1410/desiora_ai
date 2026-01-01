# 🚀 Quick Access Guide - Desiora AI API

## Base URL
```
http://localhost:8000
```

## 📖 Documentation (Mở ngay trong Browser)

| Link | Mô tả |
|------|-------|
| [http://localhost:8000/docs](http://localhost:8000/docs) | **Swagger UI** - Tài liệu và test API tương tác |
| [http://localhost:8000/redoc](http://localhost:8000/redoc) | **ReDoc** - Tài liệu API dạng HTML |
| [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json) | OpenAPI Schema (JSON) |

## ✅ Các endpoint có thể mở trực tiếp trong Browser

### 1. Health Check (Public)
```
http://localhost:8000/api/health
```
Không cần đăng nhập, dùng để kiểm tra server có chạy không.

### 2. User Profile (Cần đăng nhập)
```
http://localhost:8000/api/auth/me
```
⚠️ Cần gửi header: `Authorization: Bearer <your_token>`

### 3. Subscription Status (Cần đăng nhập)
```
http://localhost:8000/api/subscriptions/status
```
⚠️ Cần gửi header: `Authorization: Bearer <your_token>`

### 4. Design Jobs List (Cần đăng nhập)
```
http://localhost:8000/api/designs
http://localhost:8000/api/designs?page=1&page_size=20
http://localhost:8000/api/designs?status=completed
```

### 5. Design Job Detail (Cần đăng nhập)
```
http://localhost:8000/api/designs/1
```
Thay `1` bằng ID của job bạn muốn xem.

### 6. Admin Endpoints (Cần Admin role)

**Danh sách users:**
```
http://localhost:8000/api/admin/users
http://localhost:8000/api/admin/users?page=1&page_size=20
```

**Thống kê:**
```
http://localhost:8000/api/admin/stats
http://localhost:8000/api/admin/stats/usage
```

**Danh sách subscriptions:**
```
http://localhost:8000/api/admin/subscriptions
```

**Danh sách jobs:**
```
http://localhost:8000/api/admin/jobs
```

## 🔑 Cách lấy Token để test

### Bước 1: Đăng nhập
Mở Swagger UI: http://localhost:8000/docs

Tìm endpoint `/api/auth/login`, click "Try it out", nhập:
```json
{
  "email": "your-email@example.com",
  "password": "your-password"
}
```

### Bước 2: Copy access_token từ response

### Bước 3: Authorize trong Swagger UI
Click nút "Authorize" (🔓) ở trên cùng, nhập:
```
Bearer YOUR_ACCESS_TOKEN_HERE
```

### Bước 4: Test các endpoints
Bây giờ bạn có thể test tất cả endpoints từ Swagger UI!

## 📱 Sử dụng Browser Extension

Nếu muốn test trực tiếp trong browser (không dùng Swagger):

### Chrome/Edge: ModHeader Extension
1. Cài extension "ModHeader"
2. Thêm header: `Authorization: Bearer YOUR_TOKEN`
3. Mở các URL trên trong browser

### Firefox: Modify Headers Extension
Tương tự như ModHeader cho Firefox.

## 🎯 Quick Test

**Test server có chạy:**
```bash
curl http://localhost:8000/api/health
```

**Test với token:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:8000/api/auth/me
```

## 📝 Lưu ý

- Tất cả endpoints (trừ `/api/health` và `/api/auth/*`) cần authentication
- Token có thời hạn (mặc định 30 phút)
- Dùng `/api/auth/refresh` để làm mới token
- Admin endpoints cần user có role `admin` hoặc `super_admin`

