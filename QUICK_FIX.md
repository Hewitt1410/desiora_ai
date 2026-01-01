# 🔧 Quick Fix for Login Issue

## Problem
Login failed because database tables don't exist (migrations haven't run).

## Quick Fix (Run this command)

```bash
./fix-db-manual.sh
```

This will:
1. Grant database permissions (requires sudo/postgres password)
2. Run all migrations
3. Create default admin user
4. Test login

## Manual Steps (if script doesn't work)

### Step 1: Grant Permissions
```bash
sudo -u postgres psql -d desiora
```

Then run:
```sql
ALTER DATABASE desiora OWNER TO desiora;
ALTER SCHEMA public OWNER TO desiora;
GRANT ALL PRIVILEGES ON DATABASE desiora TO desiora;
\q
```

### Step 2: Run Migrations
```bash
source venv/bin/activate
alembic upgrade head
```

### Step 3: Create Admin User
```bash
python -m app.core.seed
```

## Test Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@desiora.ai","password":"admin123"}'
```

## Default Admin Credentials
- Email: `admin@desiora.ai`
- Password: `admin123`
