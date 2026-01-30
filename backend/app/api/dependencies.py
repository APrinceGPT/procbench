"""
Dependency injection for API routes.
"""

from functools import lru_cache
from typing import Generator

from app.config import Settings, get_settings
from app.analysis import Analyzer


def get_analyzer() -> Analyzer:
    """Get an analyzer instance."""
    return Analyzer(use_ai=True)


@lru_cache
def get_cached_settings() -> Settings:
    """Get cached settings."""
    return get_settings()
