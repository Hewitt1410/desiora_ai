# 🚀 Quick Routes Reference - Desiora AI Web App

Base URL: `http://localhost:3000`

## ✅ Public Routes (Không cần đăng nhập)

```
/                    → Home/Landing page
/login               → Đăng nhập (Email/Password hoặc Google OAuth)
/register            → Đăng ký tài khoản mới
/auth/callback       → OAuth callback (tự động redirect)
```

## 🔐 Protected Routes (Cần đăng nhập)

```
/dashboard           → Dashboard - Danh sách design jobs
/design/new          → Tạo design job mới
/design/[id]         → Xem chi tiết design job (ví dụ: /design/1)
/subscription        → Quản lý subscription
/admin               → Admin dashboard (cần admin role)
```

## 🌍 i18n Support

Tất cả routes đều hỗ trợ locale prefix:
- `/en/dashboard` (English - default)
- `/es/dashboard` (Spanish)
- `/pt/dashboard` (Portuguese)
- `/ja/dashboard` (Japanese)
- `/ko/dashboard` (Korean)
- `/id/dashboard` (Indonesian)
- `/ph/dashboard` (Filipino)

## 📋 Chi tiết từng Route

### `/` - Home
- Landing page với thông tin về app
- Có link đến login/register
- Nếu đã login, hiển thị link đến dashboard

### `/login` - Login
- Email/Password form
- Google OAuth button
- Link đến register page

### `/register` - Register
- Đăng ký tài khoản mới với email/password

### `/dashboard` - Dashboard
- Danh sách design jobs của user
- Link đến "Create New Design"
- Navigation bar với links đến subscription, admin (nếu có quyền)

### `/design/new` - Create Design
- Upload room image
- Chọn design style
- Submit AI design job

### `/design/[id]` - Design Detail
- Xem status của job (pending, processing, completed, failed)
- Xem kết quả khi completed
- Xem error nếu failed

### `/subscription` - Subscription
- Xem subscription status
- Xem quota (AI jobs remaining)
- Cancel subscription

### `/admin` - Admin Dashboard
- **Yêu cầu:** Admin hoặc Super Admin role
- Xem danh sách users
- Xem danh sách subscriptions
- Xem danh sách jobs
- Thống kê tổng quan

## 🔄 Redirect Flow

**Chưa login → Truy cập protected route:**
```
/dashboard → /login
```

**Login thành công:**
```
/login → /dashboard
/auth/callback → /dashboard
```

**Không có admin role → Truy cập /admin:**
```
/admin → /
```
