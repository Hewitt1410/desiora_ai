#!/bin/bash
# Manual fix script - requires postgres superuser access

echo "🔧 Fixing database permissions..."
echo ""
echo "This script requires PostgreSQL superuser access."
echo "You may need to enter the postgres user password."
echo ""

# Connect as postgres superuser and grant permissions
sudo -u postgres psql -d desiora << 'EOF'
-- Make desiora user the owner of the database
ALTER DATABASE desiora OWNER TO desiora;

-- Make desiora user the owner of public schema
ALTER SCHEMA public OWNER TO desiora;

-- Grant all necessary privileges
GRANT ALL PRIVILEGES ON DATABASE desiora TO desiora;
GRANT ALL PRIVILEGES ON SCHEMA public TO desiora;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO desiora;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO desiora;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO desiora;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO desiora;

\q
EOF

if [ $? -eq 0 ]; then
    echo ""
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
            echo ""
            echo "🧪 Testing login..."
            curl -X POST http://localhost:8000/api/auth/login \
              -H "Content-Type: application/json" \
              -d '{"email":"admin@desiora.ai","password":"admin123"}' \
              -s | python3 -m json.tool 2>/dev/null || echo "Login test completed"
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
    echo "💡 Try running manually:"
    echo "   sudo -u postgres psql -d desiora"
    echo "   Then run the SQL commands from the script"
    exit 1
fi

