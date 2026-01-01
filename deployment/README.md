# Deployment Guide

This guide covers deploying the Desiora AI application using Docker and Docker Compose.

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- NVIDIA Docker (for GPU worker)
- Git

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/your-org/desiora_ai.git
cd desiora_ai
```

### 2. Configure Environment

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` and set all required variables. Generate secure secrets:

```bash
chmod +x scripts/generate-secrets.sh
./scripts/generate-secrets.sh
```

### 3. Deploy

For production:
```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh production
```

For staging:
```bash
./scripts/deploy.sh staging
```

For development:
```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

## Environment Configuration

### Production

1. Set `ENVIRONMENT=production` in `.env`
2. Use strong passwords and secrets
3. Enable SSL/TLS for PostgreSQL
4. Configure proper resource limits
5. Set up monitoring and logging

### Staging

1. Set `ENVIRONMENT=staging` in `.env`
2. Use separate AWS resources
3. Configure staging-specific OAuth credentials

### Development

1. Set `ENVIRONMENT=development` in `.env`
2. Enable debug mode
3. Use local resources

## Services

### Backend (FastAPI)

- Port: 8000
- Health check: `http://localhost:8000/api/health`
- Auto-reloads in development mode

### Worker (Celery GPU)

- Requires NVIDIA GPU
- Processes AI design jobs
- Monitored via Flower

### Database (PostgreSQL)

- Port: 5432
- Data persisted in `postgres_data` volume
- Automatic backups recommended

### Redis

- Port: 6379
- Used for Celery broker and result backend
- Data persisted in `redis_data` volume

### Flower (Monitoring)

- Port: 5555
- Access: `http://localhost:5555`
- Basic auth configured via `FLOWER_BASIC_AUTH`

## Secrets Management

### Local Development

Use `.env` file (not committed to git).

### Production

Use one of these methods:

1. **Docker Secrets** (Docker Swarm)
2. **Environment Variables** (set in CI/CD)
3. **Secret Management Service** (AWS Secrets Manager, HashiCorp Vault)

### Required Secrets

- `SECRET_KEY` - JWT signing key
- `POSTGRES_PASSWORD` - Database password
- `REDIS_PASSWORD` - Redis password
- `GOOGLE_CLIENT_SECRET` - Google OAuth secret
- `APPLE_PRIVATE_KEY` - Apple OAuth private key
- `AWS_SECRET_ACCESS_KEY` - AWS S3 access key

## CI/CD Pipeline

### GitHub Actions

The CI/CD pipeline includes:

1. **Test** - Lint, type check, and run tests
2. **Build** - Build Docker images
3. **Security Scan** - Vulnerability scanning
4. **Deploy** - Deploy to staging/production

### Manual Deployment

```bash
# Deploy to staging
./scripts/deploy.sh staging

# Deploy to production
./scripts/deploy.sh production
```

## Monitoring

### Health Checks

All services include health checks:

```bash
# Check service status
docker-compose ps

# Check logs
docker-compose logs -f backend
docker-compose logs -f worker
```

### Flower Dashboard

Access Celery monitoring at `http://localhost:5555`

## Backup and Recovery

### Backup

```bash
chmod +x scripts/backup.sh
./scripts/backup.sh
```

Backups are stored in `./backups/` directory.

### Restore

```bash
# Restore database
docker-compose exec -T postgres psql -U desiora desiora < backups/database.sql

# Restore volumes
docker run --rm \
  -v desiora_ai_postgres_data:/data \
  -v "$(pwd)/backups":/backup \
  alpine tar xzf /backup/postgres_data.tar.gz -C /data
```

## Scaling

### Horizontal Scaling

Scale backend workers:

```bash
docker-compose up -d --scale backend=4
```

Scale Celery workers:

```bash
docker-compose up -d --scale worker=2
```

### Resource Limits

Configure in `docker-compose.prod.yml`:

```yaml
deploy:
  resources:
    limits:
      cpus: '4'
      memory: 16G
```

## Troubleshooting

### Services Not Starting

1. Check logs: `docker-compose logs`
2. Verify environment variables
3. Check port conflicts
4. Verify GPU access (for worker)

### Database Connection Issues

1. Verify PostgreSQL is healthy: `docker-compose ps postgres`
2. Check connection string in `.env`
3. Verify network connectivity

### Worker GPU Issues

1. Verify NVIDIA Docker: `docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi`
2. Check GPU availability
3. Verify CUDA version compatibility

## Security Best Practices

1. **Never commit `.env` files**
2. **Use strong, unique passwords**
3. **Enable SSL/TLS in production**
4. **Regular security scans**
5. **Keep dependencies updated**
6. **Use secrets management service**
7. **Implement network policies**
8. **Regular backups**

## Support

For issues or questions, please open an issue on GitHub.



