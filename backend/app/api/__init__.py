"""
API package initialization.
"""

from app.api.routes import router
from app.api.middleware import setup_middleware

__all__ = ["router", "setup_middleware"]
