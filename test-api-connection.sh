#!/bin/bash
echo "🔍 Testing API Connection..."
echo ""

echo "1. Testing backend health endpoint:"
curl -s http://localhost:8000/api/health || echo "❌ Backend not running on port 8000"
echo ""
echo ""

echo "2. Testing login API:"
curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@desiora.ai","password":"admin123"}' | python3 -m json.tool 2>/dev/null || echo "❌ Login API failed"
echo ""
echo ""

echo "3. Checking web app .env:"
if [ -f web/.env ]; then
  echo "✅ .env file exists"
  grep "NEXT_PUBLIC_API_URL" web/.env || echo "⚠️  NEXT_PUBLIC_API_URL not set"
else
  echo "❌ .env file not found in web directory"
fi
