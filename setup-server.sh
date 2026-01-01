#!/bin/bash
# Script tự động setup server trên Ubuntu

set -e

echo "=== Desiora AI Server Setup ==="
echo ""

# Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 không được tìm thấy. Đang cài đặt..."
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv
fi

echo "✓ Python 3: $(python3 --version)"

# Tạo virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Đang tạo virtual environment..."
    python3 -m venv venv
fi

# Kích hoạt venv và cài dependencies
echo "📦 Đang cài đặt dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Kiểm tra PostgreSQL
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL chưa được cài đặt."
    read -p "Bạn có muốn cài đặt PostgreSQL? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo apt update
        sudo apt install -y postgresql postgresql-contrib
        sudo systemctl start postgresql
        sudo systemctl enable postgresql
        echo "✓ PostgreSQL đã được cài đặt"
    fi
else
    echo "✓ PostgreSQL đã được cài đặt"
fi

# Kiểm tra Redis
if ! command -v redis-cli &> /dev/null; then
    echo "⚠️  Redis chưa được cài đặt."
    read -p "Bạn có muốn cài đặt Redis? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo apt update
        sudo apt install -y redis-server
        sudo systemctl start redis-server
        sudo systemctl enable redis-server
        echo "✓ Redis đã được cài đặt"
    fi
else
    echo "✓ Redis đã được cài đặt"
fi

# Kiểm tra file .env
if [ ! -f ".env" ]; then
    echo "⚠️  File .env chưa tồn tại."
    echo "📝 Đang tạo file .env mẫu..."
    
    # Tạo SECRET_KEY ngẫu nhiên
    SECRET_KEY=$(openssl rand -hex 32 2>/dev/null || python3 -c "import secrets; print(secrets.token_hex(32))")
    
    cat > .env << EOF
# App Configuration
APP_NAME=Desiora AI
DEBUG=True
ENVIRONMENT=development

# Database
DATABASE_URL=postgresql+asyncpg://desiora:desiora123@localhost:5432/desiora

# JWT Secrets
SECRET_KEY=${SECRET_KEY}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Redis
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# OAuth (optional)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
APPLE_CLIENT_ID=

# AWS S3 (optional)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-east-1
S3_BUCKET_NAME=
EOF
    echo "✓ File .env đã được tạo"
    echo "⚠️  Vui lòng chỉnh sửa file .env với thông tin database thực tế của bạn!"
else
    echo "✓ File .env đã tồn tại"
fi

echo ""
echo "=== Setup hoàn tất! ==="
echo ""
echo "Các bước tiếp theo:"
echo "1. Chỉnh sửa file .env với thông tin database của bạn"
echo "2. Tạo database PostgreSQL (nếu chưa có):"
echo "   sudo -u postgres psql"
echo "   CREATE DATABASE desiora;"
echo "   CREATE USER desiora WITH PASSWORD 'your_password';"
echo "   GRANT ALL PRIVILEGES ON DATABASE desiora TO desiora;"
echo ""
echo "3. Chạy migrations:"
echo "   source venv/bin/activate"
echo "   alembic upgrade head"
echo ""
echo "4. Chạy server:"
echo "   source venv/bin/activate"
echo "   python run.py"
echo ""
