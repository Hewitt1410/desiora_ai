#!/bin/bash

# Deployment script
# Usage: ./scripts/deploy.sh [environment]

set -e

ENVIRONMENT=${1:-production}

if [ "$ENVIRONMENT" != "production" ] && [ "$ENVIRONMENT" != "staging" ] && [ "$ENVIRONMENT" != "development" ]; then
    echo "Error: Environment must be 'production', 'staging', or 'development'"
    exit 1
fi

echo "Deploying to $ENVIRONMENT environment..."

# Load environment variables
if [ -f ".env.$ENVIRONMENT" ]; then
    export $(cat .env.$ENVIRONMENT | grep -v '^#' | xargs)
elif [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "Warning: No .env file found"
fi

# Pull latest images
echo "Pulling latest images..."
docker-compose -f docker-compose.yml -f docker-compose.$ENVIRONMENT.yml pull

# Build images if needed
echo "Building images..."
docker-compose -f docker-compose.yml -f docker-compose.$ENVIRONMENT.yml build

# Run database migrations
echo "Running database migrations..."
docker-compose -f docker-compose.yml -f docker-compose.$ENVIRONMENT.yml run --rm backend alembic upgrade head

# Start services
echo "Starting services..."
docker-compose -f docker-compose.yml -f docker-compose.$ENVIRONMENT.yml up -d

# Wait for services to be healthy
echo "Waiting for services to be healthy..."
sleep 10

# Check service health
echo "Checking service health..."
docker-compose -f docker-compose.yml -f docker-compose.$ENVIRONMENT.yml ps

echo "Deployment completed!"


