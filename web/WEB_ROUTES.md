# 🌐 Web App Routes - Desiora AI

Base URL: `http://localhost:3000`

## 📋 Tổng quan Routes

Web app sử dụng Next.js App Router với i18n support. Tất cả routes đều có locale prefix (ví dụ: `/en`, `/es`, `/pt`, etc.)

### Locales được hỗ trợ:
- `en` - English (default)
- `es` - Spanish
- `pt` - Portuguese
- `ja` - Japanese
- `ko` - Korean
- `id` - Indonesian
- `ph` - Filipino

## 🔓 Public Routes (Không cần đăng nhập)

### 1. Home/Landing Page
```
/
/en
/es
/pt
/ja
/ko
/id
/ph
```
**Mô tả:** Trang chủ, landing page với thông tin về ứng dụng
**File:** `app/page.tsx`

### 2. Login Page
```
/login
/en/login
/es/login
/pt/login
/ja/login
/ko/login
/id/login
/ph/login
```
**Mô tả:** Trang đăng nhập với Google OAuth và email/password
**File:** `app/login/page.tsx`
**Features:**
- Email/Password login
- Google OAuth login
- Link đến register page

### 3. Register Page
```
/register
/en/register
/es/register
/pt/register
/ja/register
/ko/register
/id/register
/ph/register
```
**Mô tả:** Trang đăng ký tài khoản mới
**File:** `app/register/page.tsx`

### 4. OAuth Callback
```
/auth/callback
/auth/callback?provider=google
/auth/callback?provider=apple
```
**Mô tả:** Callback page sau khi đăng nhập OAuth (Google/Apple)
**File:** `app/auth/callback/page.tsx`
**Note:** Tự động redirect đến `/dashboard` sau khi xác thực thành công

## 🔐 Protected Routes (Cần đăng nhập)

Tất cả routes sau đây yêu cầu authentication. Nếu chưa đăng nhập, sẽ tự động redirect đến `/login`.

### 5. Dashboard
```
/dashboard
/en/dashboard
/es/dashboard
/pt/dashboard
/ja/dashboard
/ko/dashboard
/id/dashboard
/ph/dashboard
```
**Mô tả:** Dashboard chính, hiển thị danh sách design jobs của user
**File:** `app/dashboard/page.tsx`
**Protected by:** `AuthGuard`
**Features:**
- Danh sách design jobs
- Link đến tạo job mới
- Navigation đến subscription và admin (nếu có quyền)

### 6. Create New Design Job
```
/design/new
/en/design/new
/es/design/new
/pt/design/new
/ja/design/new
/ko/design/new
/id/design/new
/ph/design/new
```
**Mô tả:** Tạo design job mới (upload ảnh, chọn style, submit job)
**File:** `app/design/new/page.tsx`
**Protected by:** `AuthGuard`
**Features:**
- Upload room image
- Chọn design style
- Tạo AI design job

### 7. Design Job Detail (Dynamic Route)
```
/design/[id]
/design/1
/design/2
/en/design/1
/es/design/1
...
```
**Mô tả:** Xem chi tiết và kết quả của một design job
**File:** `app/design/[id]/page.tsx`
**Protected by:** `AuthGuard`
**Parameters:**
- `id` - Design job ID
**Features:**
- Hiển thị job status (pending, processing, completed, failed)
- Xem kết quả design khi completed
- Xem error message nếu failed

### 8. Subscription Management
```
/subscription
/en/subscription
/es/subscription
/pt/subscription
/ja/subscription
/ko/subscription
/id/subscription
/ph/subscription
```
**Mô tả:** Quản lý subscription (xem status, cancel subscription)
**File:** `app/subscription/page.tsx`
**Protected by:** `AuthGuard`
**Features:**
- Xem subscription status hiện tại
- Xem quota (AI jobs remaining)
- Cancel subscription

### 9. Admin Dashboard (Admin Only)
```
/admin
/en/admin
/es/admin
/pt/admin
/ja/admin
/ko/admin
/id/admin
/ph/admin
```
**Mô tả:** Admin dashboard với thống kê và quản lý users/jobs
**File:** `app/admin/page.tsx`
**Protected by:** `AuthGuard` với `requireAdmin={true}`
**Role required:** `admin` hoặc `super_admin`
**Features:**
- Xem danh sách users
- Xem danh sách subscriptions
- Xem danh sách design jobs
- Thống kê tổng quan
- Usage statistics

## 🔄 Navigation Flow

### Chưa đăng nhập:
```
/ → /login → /register
```

### Đã đăng nhập:
```
/ → /dashboard → /design/new → /design/[id]
/ → /subscription
/ → /admin (nếu có quyền admin)
```

### OAuth Flow:
```
/login → Google OAuth → /auth/callback → /dashboard
```

## 📱 Responsive Design

Tất cả các routes đều responsive và hỗ trợ:
- Desktop
- Tablet
- Mobile

## 🎨 Dark Mode

Tất cả các routes đều hỗ trợ dark mode thông qua ThemeToggle component.

## 🔐 Authentication Guards

### AuthGuard Component
- Kiểm tra authentication token
- Redirect đến `/login` nếu chưa đăng nhập
- Kiểm tra admin role nếu `requireAdmin={true}`

### Protected Routes sử dụng AuthGuard:
- `/dashboard`
- `/design/new`
- `/design/[id]`
- `/subscription`
- `/admin` (có `requireAdmin={true}`)

## 🌍 i18n Routing

Tất cả routes đều có locale prefix. Middleware tự động thêm locale vào URL.

**Default locale:** `en` (English)

**Ví dụ:**
- `/dashboard` → `/en/dashboard` (default)
- `/es/dashboard` → Spanish version
- `/pt/dashboard` → Portuguese version

## 📝 Ví dụ URLs đầy đủ

### Development:
```
http://localhost:3000/
http://localhost:3000/en/login
http://localhost:3000/dashboard
http://localhost:3000/design/new
http://localhost:3000/design/123
http://localhost:3000/subscription
http://localhost:3000/admin
```

### Production (ví dụ):
```
https://desiora-ai.com/
https://desiora-ai.com/en/login
https://desiora-ai.com/dashboard
https://desiora-ai.com/design/new
https://desiora-ai.com/design/123
https://desiora-ai.com/subscription
https://desiora-ai.com/admin
```

## 🚀 Quick Reference

| Route | Public? | Admin? | Description |
|-------|---------|--------|-------------|
| `/` | ✅ | ❌ | Home page |
| `/login` | ✅ | ❌ | Login page |
| `/register` | ✅ | ❌ | Register page |
| `/auth/callback` | ✅ | ❌ | OAuth callback |
| `/dashboard` | ❌ | ❌ | User dashboard |
| `/design/new` | ❌ | ❌ | Create design job |
| `/design/[id]` | ❌ | ❌ | View design job |
| `/subscription` | ❌ | ❌ | Subscription management |
| `/admin` | ❌ | ✅ | Admin dashboard |

## 💡 Tips

1. **Default locale:** Bạn có thể truy cập `/dashboard` thay vì `/en/dashboard` - middleware sẽ tự động thêm locale
2. **Authentication:** Tất cả protected routes sẽ redirect đến `/login` nếu chưa đăng nhập
3. **Admin access:** Route `/admin` chỉ accessible với role `admin` hoặc `super_admin`
4. **Dynamic routes:** `/design/[id]` nhận job ID làm parameter


