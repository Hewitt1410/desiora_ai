#!/bin/bash
# Script để chạy server

cd "$(dirname "$0")"

# Kích hoạt virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Virtual environment chưa được tạo. Chạy: ./setup-server.sh"
    exit 1
fi

# Kiểm tra file .env
if [ ! -f ".env" ]; then
    echo "❌ File .env không tồn tại. Vui lòng tạo file .env trước."
    exit 1
fi

echo "🚀 Đang khởi động Desiora AI server..."
echo "📍 Server sẽ chạy tại: http://localhost:8000"
echo "📚 API docs: http://localhost:8000/docs"
echo ""
echo "Nhấn Ctrl+C để dừng server"
echo ""

# Chạy server
python run.py
