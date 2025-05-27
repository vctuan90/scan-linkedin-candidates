"""
Health check endpoints for LinkedIn Scraper API.
"""

import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException, status

from ..models.responses import HealthResponse
from ....config.constants import API_MESSAGES

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Check if the API is running and healthy"
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.
    
    Returns the current status of the API service.
    """
    try:
        return HealthResponse(
            status="healthy",
            message=API_MESSAGES["HEALTH_OK"],
            version="1.0.0",
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
        
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Health check failed: {str(e)}"
        ) 