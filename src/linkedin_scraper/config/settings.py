"""
Application settings and configuration.
"""

import os
from typing import Optional
from decouple import config

class Settings:
    """Application settings."""
    
    # LinkedIn credentials
    LINKEDIN_EMAIL: str = config('LINKEDIN_EMAIL', default='')
    LINKEDIN_PASSWORD: str = config('LINKEDIN_PASSWORD', default='')
    
    # Scraping settings
    MIN_DELAY: int = config('MIN_DELAY', default=2, cast=int)
    MAX_DELAY: int = config('MAX_DELAY', default=5, cast=int)
    MAX_RETRIES: int = config('MAX_RETRIES', default=3, cast=int)
    SCROLL_PAUSE_TIME: int = config('SCROLL_PAUSE_TIME', default=2, cast=int)
    MAX_RESULTS: int = config('MAX_RESULTS', default=100, cast=int)
    PAGE_LOAD_TIMEOUT: int = config('PAGE_LOAD_TIMEOUT', default=30000, cast=int)
    
    # Browser settings
    HEADLESS_MODE: bool = config('HEADLESS_MODE', default=True, cast=bool)
    BROWSER_TYPE: str = config('BROWSER_TYPE', default='chrome')
    
    # API settings
    API_VERSION: str = "v1"
    API_PREFIX: str = f"/api/{API_VERSION}"
    API_HOST: str = config('API_HOST', default='0.0.0.0')
    API_PORT: int = config('API_PORT', default=8000, cast=int)
    
    # Debug and logging
    DEBUG: bool = config('DEBUG', default=False, cast=bool)
    LOG_LEVEL: str = config('LOG_LEVEL', default='INFO')
    
    # Rate limiting
    RATE_LIMIT_REQUESTS: int = config('RATE_LIMIT_REQUESTS', default=100, cast=int)
    RATE_LIMIT_WINDOW: int = config('RATE_LIMIT_WINDOW', default=3600, cast=int)  # 1 hour
    
    # Security
    SECRET_KEY: str = config('SECRET_KEY', default='your-secret-key-change-in-production')
    ALLOWED_HOSTS: list = config('ALLOWED_HOSTS', default='*', cast=lambda v: [s.strip() for s in v.split(',')])

# Global settings instance
settings = Settings() 