# API Endpoints - Desiora AI

Base URL: `http://localhost:8000`

## 📚 Documentation (Truy cập từ Browser)

| URL | Mô tả |
|-----|-------|
| `/docs` | Swagger UI - Tài liệu API tương tác (Recommended) |
| `/redoc` | ReDoc - Tài liệu API dạng HTML |
| `/openapi.json` | OpenAPI schema (JSON format) |

## 🔓 Public Endpoints (Không cần authentication)

### Health Check

| Method | URL | Mô tả |
|--------|-----|-------|
| `GET` | `/api/health` | Kiểm tra trạng thái server |

**Ví dụ:**
```
http://localhost:8000/api/health
```

Response:
```json
{
  "status": "healthy",
  "message": "Service is running"
}
```

## 🔐 Authentication Endpoints

### Đăng ký / Đăng nhập

| Method | URL | Mô tả | Cần Auth |
|--------|-----|-------|----------|
| `POST` | `/api/auth/register` | Đăng ký tài khoản mới | ❌ |
| `POST` | `/api/auth/login` | Đăng nhập với email/password | ❌ |
| `POST` | `/api/auth/oauth/google` | Đăng nhập với Google OAuth | ❌ |
| `POST` | `/api/auth/oauth/apple` | Đăng nhập với Apple OAuth | ❌ |
| `POST` | `/api/auth/refresh` | Làm mới access token | ❌ |
| `GET` | `/api/auth/me` | Lấy thông tin user hiện tại | ✅ |

**Ví dụ truy cập `/api/auth/me` từ browser:**
- Cần gửi header: `Authorization: Bearer <access_token>`
- Hoặc sử dụng Swagger UI tại `/docs` để test

## 🖼️ Image Endpoints (Cần Authentication)

| Method | URL | Mô tả | Cần Auth |
|--------|-----|-------|----------|
| `POST` | `/api/images/presign-upload` | Lấy presigned URL để upload ảnh | ✅ |
| `POST` | `/api/images` | Tạo record ảnh sau khi upload | ✅ |
| `POST` | `/api/images/confirm-upload` | Xác nhận upload thành công | ✅ |

## 💳 Subscription Endpoints (Cần Authentication)

| Method | URL | Mô tả | Cần Auth |
|--------|-----|-------|----------|
| `GET` | `/api/subscriptions/status` | Lấy trạng thái subscription hiện tại | ✅ |
| `POST` | `/api/subscriptions/cancel` | Hủy subscription | ✅ |

**Ví dụ truy cập `/api/subscriptions/status` từ browser:**
```
http://localhost:8000/api/subscriptions/status
```
(Với header: `Authorization: Bearer <token>`)

## 🎨 Design Job Endpoints (Cần Authentication)

| Method | URL | Mô tả | Cần Auth |
|--------|-----|-------|----------|
| `POST` | `/api/designs` | Tạo job thiết kế mới | ✅ |
| `GET` | `/api/designs` | Lấy danh sách jobs (có query params) | ✅ |
| `GET` | `/api/designs/{job_id}` | Lấy chi tiết job theo ID | ✅ |

**Ví dụ truy cập từ browser:**

1. Lấy danh sách jobs:
```
http://localhost:8000/api/designs?page=1&page_size=20
```

2. Lấy job theo ID:
```
http://localhost:8000/api/designs/1
```

## 👤 Protected Endpoints (Cần Authentication)

| Method | URL | Mô tả | Cần Auth |
|--------|-----|-------|----------|
| `GET` | `/api/protected/example` | Endpoint ví dụ protected | ✅ |
| `GET` | `/api/protected/middleware-example` | Endpoint ví dụ với middleware | ✅ |
| `GET` | `/api/protected/user-profile` | Lấy profile của user hiện tại | ✅ |

**Ví dụ:**
```
http://localhost:8000/api/protected/user-profile
```

## 👨‍💼 Admin Endpoints (Cần Admin Role)

| Method | URL | Mô tả | Cần Auth | Role Required |
|--------|-----|-------|----------|---------------|
| `GET` | `/api/admin/users` | Lấy danh sách users | ✅ | Admin/Super Admin |
| `GET` | `/api/admin/subscriptions` | Lấy danh sách subscriptions | ✅ | Admin/Super Admin |
| `GET` | `/api/admin/jobs` | Lấy danh sách design jobs | ✅ | Admin/Super Admin |
| `GET` | `/api/admin/stats` | Lấy thống kê tổng quan | ✅ | Admin/Super Admin |
| `GET` | `/api/admin/stats/usage` | Lấy thống kê sử dụng | ✅ | Admin/Super Admin |

**Ví dụ truy cập từ browser:**

1. Lấy danh sách users:
```
http://localhost:8000/api/admin/users?page=1&page_size=20
```

2. Lấy thống kê:
```
http://localhost:8000/api/admin/stats
```

## 🔔 Webhook Endpoints (Public, nhưng cần signature verification)

| Method | URL | Mô tả |
|--------|-----|-------|
| `POST` | `/api/webhooks/stripe` | Webhook từ Stripe |
| `POST` | `/api/webhooks/app-store` | Webhook từ Apple App Store |
| `POST` | `/api/webhooks/google-play` | Webhook từ Google Play |

## 📝 Cách sử dụng từ Browser

### 1. Sử dụng Swagger UI (Recommended)

Truy cập: `http://localhost:8000/docs`

- Tự động có UI để test các endpoints
- Có thể nhập token để test các endpoint cần authentication
- Xem request/response examples

### 2. Sử dụng ReDoc

Truy cập: `http://localhost:8000/redoc`

- Xem tài liệu API dạng HTML đẹp
- Không thể test trực tiếp, chỉ xem documentation

### 3. Sử dụng Browser trực tiếp (chỉ cho GET requests)

**Với các endpoint không cần auth:**
```bash
# Health check
curl http://localhost:8000/api/health
```

**Với các endpoint cần auth:**
```bash
# Sử dụng Bearer token
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     http://localhost:8000/api/auth/me
```

Hoặc trong browser, bạn có thể dùng extension như:
- **ModHeader** (Chrome/Edge)
- **Requestly** (Chrome/Firefox)
- **REST Client** (VS Code extension)

### 4. Ví dụ với query parameters

```
http://localhost:8000/api/designs?page=1&page_size=10&status=completed
http://localhost:8000/api/admin/users?page=1&page_size=20&role=user&is_active=true
```

## 🔑 Authentication

Hầu hết các endpoints (trừ `/api/health` và `/api/auth/*`) cần authentication.

### Cách lấy token:

1. **Đăng ký/Đăng nhập:**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

Response:
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

2. **Sử dụng token:**
```bash
curl -H "Authorization: Bearer eyJhbGc..." \
     http://localhost:8000/api/auth/me
```

## 📋 Tổng kết nhanh

### Endpoints có thể truy cập trực tiếp từ browser (GET):

✅ **Public:**
- `/api/health`

✅ **Cần token trong header:**
- `/api/auth/me`
- `/api/subscriptions/status`
- `/api/designs` (với query params)
- `/api/designs/{job_id}`
- `/api/protected/*`
- `/api/admin/*` (cần admin role)

✅ **Documentation:**
- `/docs` (Swagger UI - Best choice!)
- `/redoc` (ReDoc)
- `/openapi.json`

### Endpoints cần POST/PUT/DELETE (dùng Swagger UI hoặc tools):

- `/api/auth/*` (register, login, oauth)
- `/api/images/*` (upload)
- `/api/subscriptions/cancel`
- `/api/designs` (POST - create job)
- `/api/webhooks/*`

## 💡 Recommendation

**Cách tốt nhất để test API:**
1. Mở browser, truy cập `http://localhost:8000/docs`
2. Click vào "Authorize" button (🔓 icon)
3. Nhập: `Bearer YOUR_ACCESS_TOKEN`
4. Test tất cả endpoints từ UI!



