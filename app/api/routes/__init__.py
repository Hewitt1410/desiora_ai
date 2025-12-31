# Routes are imported directly in main.py
from app.api.routes import auth
from app.api.routes import health
from app.api.routes import protected
from app.api.routes import images

__all__ = ["auth", "health", "protected", "images"]

