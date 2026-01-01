#!/bin/bash

# Generate secure secrets for deployment
# Usage: ./scripts/generate-secrets.sh

echo "Generating secure secrets..."

# Generate SECRET_KEY
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
echo "SECRET_KEY=$SECRET_KEY"

# Generate POSTGRES_PASSWORD
POSTGRES_PASSWORD=$(python3 -c "import secrets; print(secrets.token_urlsafe(24))")
echo "POSTGRES_PASSWORD=$POSTGRES_PASSWORD"

# Generate REDIS_PASSWORD
REDIS_PASSWORD=$(python3 -c "import secrets; print(secrets.token_urlsafe(24))")
echo "REDIS_PASSWORD=$REDIS_PASSWORD"

# Generate FLOWER_BASIC_AUTH
FLOWER_USER="admin"
FLOWER_PASSWORD=$(python3 -c "import secrets; print(secrets.token_urlsafe(16))")
echo "FLOWER_BASIC_AUTH=$FLOWER_USER:$FLOWER_PASSWORD"

echo ""
echo "Add these to your .env file or secrets management system"


