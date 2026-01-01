from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.middleware import AuthenticationMiddleware
from app.api.routes import auth, health, protected, images, subscriptions, webhooks, designs, admin, plans

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    version="1.0.0"
)

# CORS middleware (must be first)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication middleware (optional - uncomment to enable global protection)
# app.add_middleware(
#     AuthenticationMiddleware,
#     exclude_paths=[
#         "/api/health",
#         "/api/auth",
#         "/docs",
#         "/redoc",
#         "/openapi.json",
#     ]
# )

# Include routers
app.include_router(health.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(protected.router, prefix="/api")
app.include_router(images.router, prefix="/api")
app.include_router(subscriptions.router, prefix="/api")
app.include_router(webhooks.router, prefix="/api")
app.include_router(designs.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(plans.router, prefix="/api")


@app.on_event("startup")
async def startup():
    """Startup event handler."""
    # Create default admin user if it doesn't exist
    try:
        from app.core.seed import create_default_admin
        await create_default_admin()
    except Exception as e:
        # Log error but don't fail startup
        print(f"Warning: Could not create default admin user: {e}")


@app.on_event("shutdown")
async def shutdown():
    """Shutdown event handler."""
    pass

