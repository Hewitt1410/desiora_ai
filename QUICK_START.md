# 🚀 Quick Start Guide

## Start Backend Server

```bash
# Option 1: Use the script
./start-backend.sh

# Option 2: Manual start
source venv/bin/activate
python run.py
```

Backend will be available at: `http://localhost:8000`
API docs: `http://localhost:8000/docs`

## Start Web App

```bash
cd web
npm run dev
```

Web app will be available at: `http://localhost:3000`

## Default Admin Credentials

- **Email**: `admin@desiora.ai`
- **Password**: `admin123`

## Troubleshooting

### Login Failed

1. **Check if backend is running:**
   ```bash
   curl http://localhost:8000/api/health
   ```

2. **If backend is not running, start it:**
   ```bash
   ./start-backend.sh
   ```

3. **Check backend logs for errors**

4. **Verify admin user exists:**
   ```bash
   source venv/bin/activate
   python -m app.core.seed
   ```

### Connection Refused

- Make sure backend server is running on port 8000
- Check firewall settings
- Verify `NEXT_PUBLIC_API_URL` in `web/.env` is `http://localhost:8000`
