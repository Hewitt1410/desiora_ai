# Desiora AI - FastAPI Backend

A FastAPI backend project with clean architecture, featuring PostgreSQL, JWT authentication, and OAuth login support.

## Features

- ✅ FastAPI with async support
- ✅ PostgreSQL with SQLAlchemy 2.0 async
- ✅ JWT authentication with access and refresh tokens
- ✅ Token refresh support
- ✅ Google OAuth login
- ✅ Apple OAuth login
- ✅ Authentication middleware for route protection
- ✅ Protected route examples (dependency injection & middleware)
- ✅ Environment-based configuration (no hardcoded secrets)
- ✅ Clean architecture (API / Services / Repositories / Models)
- ✅ Alembic migrations
- ✅ Health check endpoint

## Project Structure

```
desiora_ai/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py          # Authentication endpoints
│   │   │   └── health.py        # Health check endpoint
│   │   └── dependencies.py      # API dependencies (auth, etc.)
│   ├── core/
│   │   ├── config.py            # Configuration management
│   │   ├── database.py          # Database connection setup
│   │   └── security.py           # Security utilities (JWT, hashing)
│   ├── models/
│   │   └── user.py              # User model
│   ├── repositories/
│   │   └── user_repository.py   # User data access layer
│   ├── schemas/
│   │   ├── auth.py              # Auth request/response schemas
│   │   └── user.py              # User request/response schemas
│   ├── services/
│   │   ├── auth_service.py      # Authentication business logic
│   │   └── oauth_service.py     # OAuth authentication logic
│   └── main.py                  # FastAPI application entry point
├── alembic/                      # Database migrations
├── alembic.ini                   # Alembic configuration
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
└── README.md                     # This file
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your configuration:

```bash
cp .env.example .env
```

Edit `.env` with your actual values:
- Database connection string
- JWT secret key
- OAuth credentials (Google & Apple)

### 3. Database Setup

Create your PostgreSQL database:

```bash
createdb desiora_db
```

### 4. Run Migrations

```bash
alembic upgrade head
```

### 5. Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
- `GET /api/health` - Health check endpoint

### Authentication
- `POST /api/auth/register` - Register with email/password
- `POST /api/auth/login` - Login with email/password (returns access + refresh tokens)
- `POST /api/auth/refresh` - Refresh access token using refresh token
- `POST /api/auth/oauth/google` - Authenticate with Google OAuth
- `POST /api/auth/oauth/apple` - Authenticate with Apple OAuth
- `GET /api/auth/me` - Get current user info (requires authentication)

### Protected Routes (Examples)
- `GET /api/protected/example` - Example protected route using dependency injection
- `GET /api/protected/middleware-example` - Example protected route using middleware
- `GET /api/protected/user-profile` - Get user profile (protected route)

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Authentication

### JWT Tokens

The authentication system uses JWT tokens with the following structure:

- **Access Token**: Short-lived token (default: 30 minutes) for API requests
- **Refresh Token**: Long-lived token (default: 7 days) for obtaining new access tokens

### Token Usage

1. **Login/Register/OAuth**: Returns both `access_token` and `refresh_token`
2. **API Requests**: Include access token in `Authorization: Bearer <token>` header
3. **Token Refresh**: Use `/api/auth/refresh` endpoint with refresh token to get new tokens

### Protecting Routes

Two methods are available:

#### 1. Dependency Injection (Recommended)
```python
from app.api.dependencies import get_current_user
from app.models.user import User

@router.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"user_id": current_user.id}
```

#### 2. Middleware (Global Protection)
The `AuthenticationMiddleware` can be enabled in `app/main.py` to protect all routes except excluded paths.

### Example Request

```bash
# Login
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'

# Use access token
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer <access_token>"

# Refresh token
curl -X POST "http://localhost:8000/api/auth/refresh" \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "<refresh_token>"}'
```

## Architecture

This project follows clean architecture principles:

- **API Layer** (`app/api/`): HTTP endpoints and request/response handling
- **Services Layer** (`app/services/`): Business logic and orchestration
- **Repositories Layer** (`app/repositories/`): Data access abstraction
- **Models Layer** (`app/models/`): Database models (SQLAlchemy)
- **Schemas Layer** (`app/schemas/`): Pydantic models for validation
- **Core Layer** (`app/core/`): Configuration, database, security utilities, middleware

## OAuth Setup

### Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs
6. Copy Client ID and Client Secret to `.env`

### Apple OAuth

1. Go to [Apple Developer Portal](https://developer.apple.com/)
2. Create an App ID
3. Create a Service ID for Sign in with Apple
4. Create a Key with Sign in with Apple enabled
5. Download the private key (.p8 file)
6. Copy Team ID, Key ID, Client ID, and private key to `.env`

## Development

### Creating Migrations

```bash
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

### Running Tests

(Add your test framework setup here)

## License

MIT

