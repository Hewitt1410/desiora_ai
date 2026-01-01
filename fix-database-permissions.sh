#!/bin/bash
# Script to fix database permissions and run migrations

echo "🔧 Fixing database permissions..."

# Get database connection info from .env
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    exit 1
fi

# Extract database URL
DATABASE_URL=$(grep "^DATABASE_URL=" .env | cut -d '=' -f2-)

if [ -z "$DATABASE_URL" ]; then
    echo "❌ Error: DATABASE_URL not found in .env"
    exit 1
fi

# Parse database URL to get components
# Format: postgresql+asyncpg://user:password@host:port/database
DB_USER=$(echo $DATABASE_URL | sed -n 's/.*:\/\/\([^:]*\):.*/\1/p')
DB_PASS=$(echo $DATABASE_URL | sed -n 's/.*:\/\/[^:]*:\([^@]*\)@.*/\1/p')
DB_HOST=$(echo $DATABASE_URL | sed -n 's/.*@\([^:]*\):.*/\1/p')
DB_PORT=$(echo $DATABASE_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')
DB_NAME=$(echo $DATABASE_URL | sed -n 's/.*\/\([^?]*\).*/\1/p')

echo "📋 Database info:"
echo "   Host: $DB_HOST"
echo "   Port: $DB_PORT"
echo "   Database: $DB_NAME"
echo "   User: $DB_USER"

# Connect as postgres superuser to grant permissions
echo ""
echo "🔐 Granting permissions to database user..."
echo "   (You may need to enter postgres superuser password)"

PGPASSWORD=$DB_PASS psql -h $DB_HOST -p ${DB_PORT:-5432} -U $DB_USER -d $DB_NAME <<EOF
-- Grant schema usage
GRANT USAGE ON SCHEMA public TO $DB_USER;
GRANT CREATE ON SCHEMA public TO $DB_USER;

-- Grant all privileges on all tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO $DB_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO $DB_USER;

-- If tables already exist, grant privileges
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $DB_USER;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO $DB_USER;

\q
EOF

if [ $? -eq 0 ]; then
    echo "✅ Permissions granted successfully!"
    echo ""
    echo "🚀 Running migrations..."
    source venv/bin/activate
    alembic upgrade head
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Migrations completed successfully!"
        echo ""
        echo "🔐 Creating default admin user..."
        python -m app.core.seed
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ Setup completed successfully!"
            echo ""
            echo "📝 Default admin credentials:"
            echo "   Email: admin@desiora.ai"
            echo "   Password: admin123"
        else
            echo "⚠️  Warning: Could not create admin user (may already exist)"
        fi
    else
        echo "❌ Error: Migrations failed"
        exit 1
    fi
else
    echo "❌ Error: Failed to grant permissions"
    echo ""
    echo "💡 Alternative: Connect as postgres superuser and run:"
    echo "   psql -U postgres -d $DB_NAME"
    echo "   GRANT USAGE ON SCHEMA public TO $DB_USER;"
    echo "   GRANT CREATE ON SCHEMA public TO $DB_USER;"
    exit 1
fi

