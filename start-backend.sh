#!/bin/bash
# Start backend server

cd "$(dirname "$0")"
source venv/bin/activate

echo "🚀 Starting backend server..."
echo "   API will be available at: http://localhost:8000"
echo "   API docs: http://localhost:8000/docs"
echo ""

python run.py
