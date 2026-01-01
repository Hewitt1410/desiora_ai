# Hướng dẫn chạy server trên Ubuntu

## Yêu cầu hệ thống

- Ubuntu 18.04 trở lên
- Python 3.11+ (hiện tại: Python 3.12.3 ✓)
- PostgreSQL 12+ (hoặc Docker)
- Redis 6+ (hoặc Docker)
- pip và venv

## Cách 1: Chạy trực tiếp trên Ubuntu (Development)

### Bước 1: Cài đặt các dependencies hệ thống

```bash
# Cập nhật package list
sudo apt update

# Cài đặt PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Cài đặt Redis
sudo apt install -y redis-server

# Cài đặt Python dependencies
sudo apt install -y python3-pip python3-venv python3-dev build-essential libpq-dev

# Khởi động services
sudo systemctl start postgresql
sudo systemctl enable postgresql
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

### Bước 2: Tạo database PostgreSQL

```bash
# Chuyển sang user postgres
sudo -u postgres psql

# Trong PostgreSQL prompt, chạy:
CREATE DATABASE desiora;
CREATE USER desiora WITH PASSWORD '3adde443';
GRANT ALL PRIVILEGES ON DATABASE desiora TO desiora;
ALTER USER desiora CREATEDB;
\q
```

### Bước 3: Tạo môi trường ảo Python

```bash
cd /home/zunke/projects/desiora_ai

# Tạo virtual environment
python3 -m venv venv

# Kích hoạt virtual environment
source venv/bin/activate

# Cài đặt dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Bước 4: Tạo file .env

Tạo file `.env` trong thư mục gốc của project:

```bash
cat > .env << 'EOF'
# App Configuration
APP_NAME=Desiora AI
DEBUG=True
ENVIRONMENT=development

# Database
DATABASE_URL=postgresql+asyncpg://desiora:3adde443@localhost:5432/desiora

# JWT Secrets (tạo secret key ngẫu nhiên)
SECRET_KEY=
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Google OAuth (optional - có thể bỏ qua nếu chưa có)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback

# Apple OAuth (optional)
APPLE_CLIENT_ID=
APPLE_TEAM_ID=
APPLE_KEY_ID=
APPLE_PRIVATE_KEY=
APPLE_REDIRECT_URI=http://localhost:8000/api/auth/apple/callback

# AWS S3 (optional - có thể dùng local storage)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-east-1
S3_BUCKET_NAME=
S3_ENDPOINT_URL=

# Redis (nếu Redis có password)
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
EOF
```

**Quan trọng**: Thay đổi các giá trị sau trong file `.env`:
- `your_password_here` → mật khẩu PostgreSQL của bạn
- `your-secret-key-here-change-in-production` → một chuỗi ngẫu nhiên (có thể dùng lệnh `openssl rand -hex 32` để tạo)

### Bước 5: Chạy migrations

```bash
# Đảm bảo virtual environment đã được kích hoạt
source venv/bin/activate

# Chạy migrations
alembic upgrade head
```

### Bước 6: Chạy server

```bash
# Đảm bảo virtual environment đã được kích hoạt
source venv/bin/activate

# Chạy server
python run.py
```

Server sẽ chạy tại: `http://localhost:8000`

API docs có thể truy cập tại: `http://localhost:8000/docs`

### Bước 7: Test server

Mở terminal mới và chạy:

```bash
curl http://localhost:8000/api/health
```

Nếu thấy response JSON, server đã chạy thành công!

## Cách 2: Chạy bằng Docker (Recommended)

Nếu bạn muốn chạy tất cả services (PostgreSQL, Redis, Backend) trong Docker:

### Bước 1: Cài đặt Docker và Docker Compose

```bash
# Cài đặt Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Thêm user vào docker group (để chạy docker không cần sudo)
sudo usermod -aG docker $USER

# Cài đặt Docker Compose
sudo apt install -y docker-compose

# Đăng xuất và đăng nhập lại để áp dụng group changes
```

### Bước 2: Tạo file .env cho Docker

Tạo file `.env` với các biến môi trường cần thiết (xem hướng dẫn ở trên).

### Bước 3: Chạy với Docker Compose

```bash
cd /home/zunke/projects/desiora_ai

# Chạy tất cả services
docker-compose up -d

# Xem logs
docker-compose logs -f backend

# Dừng services
docker-compose down
```

## Troubleshooting

### Lỗi kết nối database

```bash
# Kiểm tra PostgreSQL đang chạy
sudo systemctl status postgresql

# Kiểm tra kết nối
psql -U desiora -d desiora -h localhost
```

### Lỗi kết nối Redis

```bash
# Kiểm tra Redis đang chạy
sudo systemctl status redis-server

# Test kết nối
redis-cli ping
```

### Port 8000 đã được sử dụng

Thay đổi port trong `run.py` hoặc kill process đang dùng port 8000:

```bash
# Tìm process đang dùng port 8000
sudo lsof -i :8000

# Kill process
sudo kill -9 <PID>
```

### Lỗi permission

Nếu gặp lỗi permission khi chạy PostgreSQL:

```bash
sudo chmod 755 /var/lib/postgresql
sudo chmod 700 /var/lib/postgresql/*/main
```

## Script tiện ích

Tạo script để dễ dàng start/stop server:

```bash
# Tạo file start-server.sh
cat > start-server.sh << 'EOF'
#!/bin/bash
cd /home/zunke/projects/desiora_ai
source venv/bin/activate
python run.py
EOF

chmod +x start-server.sh
```

Chạy: `./start-server.sh`


