"""
LinkedIn Profile Scraper API - Main Application
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from linkedin_scraper.config.settings import settings
from linkedin_scraper.api.v1.endpoints.search import router as search_router
from linkedin_scraper.api.v1.endpoints.health import router as health_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("Starting LinkedIn Profile Scraper API")
    yield
    logger.info("Shutting down LinkedIn Profile Scraper API")

# Create FastAPI application
app = FastAPI(
    title="LinkedIn Profile Scraper API",
    description="API for automated LinkedIn profile search and extraction",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    search_router,
    prefix=settings.API_PREFIX,
    tags=["search"]
)

app.include_router(
    health_router,
    prefix=settings.API_PREFIX,
    tags=["health"]
)

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "LinkedIn Profile Scraper API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": f"{settings.API_PREFIX}/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    ) 