"""
ProcBench Backend - FastAPI Application Entry Point
"""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api import router, setup_middleware
from app.config import settings


# Load environment variables
env_path = Path(__file__).parent.parent.parent / "env"
if env_path.exists():
    load_dotenv(env_path)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    app = FastAPI(
        title="ProcBench API",
        description="AI-powered Process Monitor log analysis platform",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    
    # Setup middleware
    setup_middleware(app)
    
    # Include API routes
    app.include_router(router)
    
    # Root endpoint
    @app.get("/")
    async def root():
        return {
            "name": "ProcBench API",
            "version": "1.0.0",
            "description": "AI-powered Process Monitor log analysis platform",
            "docs": "/docs",
        }
    
    logger.info("ProcBench API initialized")
    logger.info(f"AI enabled: {bool(settings.openai_api_key)}")
    
    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.environment == "development"
    )
