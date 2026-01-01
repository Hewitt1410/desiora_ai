# 🔧 Fix Login Failed Issue

## Problem
Login failed with error: `relation "users" does not exist` or `permission denied for schema public`

## Root Cause
1. Database migrations haven't been run yet
2. Database user doesn't have permissions to create tables

## Solution

### Option 1: Use the Fix Script (Recommended)

```bash
./fix-database-permissions.sh
```

This script will:
1. Grant necessary permissions to your database user
2. Run all migrations
3. Create the default admin user

### Option 2: Manual Fix

#### Step 1: Grant Database Permissions

Connect to PostgreSQL as superuser (usually `postgres`):

```bash
sudo -u postgres psql -d your_database_name
```

Then run:

```sql
-- Replace 'your_db_user' with your actual database user from DATABASE_URL
GRANT USAGE ON SCHEMA public TO your_db_user;
GRANT CREATE ON SCHEMA public TO your_db_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO your_db_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO your_db_user;
\q
```

#### Step 2: Run Migrations

```bash
source venv/bin/activate
alembic upgrade head
```

#### Step 3: Create Admin User

```bash
python -m app.core.seed
```

### Option 3: Create Database from Scratch

If you want to start fresh:

```bash
# Drop and recreate database (WARNING: This will delete all data!)
sudo -u postgres psql -c "DROP DATABASE IF EXISTS your_database_name;"
sudo -u postgres psql -c "CREATE DATABASE your_database_name;"

# Grant permissions
sudo -u postgres psql -d your_database_name -c "GRANT ALL PRIVILEGES ON DATABASE your_database_name TO your_db_user;"

# Run migrations
source venv/bin/activate
alembic upgrade head

# Create admin user
python -m app.core.seed
```

## Verify Fix

After running the fix, test login:

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@desiora.ai","password":"admin123"}'
```

You should get a response with `access_token` and `refresh_token`.

## Default Admin Credentials

- **Email**: `admin@desiora.ai`
- **Password**: `admin123`
- **Role**: `super_admin`

⚠️ **Important**: Change the password after first login!

## Troubleshooting

### If you get "permission denied" errors:

1. Check your `.env` file has correct `DATABASE_URL`
2. Ensure the database user exists
3. Try connecting as postgres superuser to grant permissions

### If migrations fail:

1. Check PostgreSQL is running: `sudo systemctl status postgresql`
2. Verify database exists: `psql -U postgres -l | grep your_database`
3. Check connection: `psql -U your_user -d your_database`

### If admin user creation fails:

The user might already exist. Check with:

```bash
source venv/bin/activate
python -c "from app.core.seed import create_default_admin; import asyncio; asyncio.run(create_default_admin())"
```

