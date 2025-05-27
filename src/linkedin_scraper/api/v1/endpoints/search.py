"""
Search endpoints for LinkedIn Scraper API.
"""

import logging
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from ..models.requests import SearchRequest
from ..models.responses import SearchResponse, CredentialValidationResponse, SearchLimitsResponse
from ....core.services.search_service import SearchService

logger = logging.getLogger(__name__)
router = APIRouter()
search_service = SearchService()

@router.post(
    "/search",
    response_model=SearchResponse,
    summary="Search LinkedIn profiles",
    description="Search for LinkedIn profiles based on job title, location, and optional keywords"
)
async def search_profiles(request: SearchRequest) -> JSONResponse:
    """
    Search for LinkedIn profiles.
    
    - **job_title**: Job title to search for (required)
    - **location**: Location to search in (required)
    - **keywords**: Optional list of keywords for filtering
    - **max_results**: Maximum number of results (1-100, default: 50)
    """
    try:
        logger.info(f"Received search request: {request.job_title} in {request.location}")
        
        result = await search_service.search_profiles(
            job_title=request.job_title,
            location=request.location,
            keywords=request.keywords,
            max_results=request.max_results
        )
        
        if result["success"]:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=result
            )
        else:
            # Return appropriate error status based on error code
            status_code = status.HTTP_400_BAD_REQUEST
            if result.get("error_code") == "SEARCH_ERROR":
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            elif result.get("error_code") == "INVALID_PARAMS":
                status_code = status.HTTP_400_BAD_REQUEST
            
            return JSONResponse(
                status_code=status_code,
                content=result
            )
            
    except Exception as e:
        logger.error(f"Search endpoint error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.get(
    "/validate-credentials",
    response_model=CredentialValidationResponse,
    summary="Validate LinkedIn credentials",
    description="Validate LinkedIn credentials by attempting to login"
)
async def validate_credentials() -> JSONResponse:
    """
    Validate LinkedIn credentials.
    
    This endpoint attempts to login to LinkedIn using the configured credentials
    to verify they are valid.
    """
    try:
        result = await search_service.validate_credentials()
        
        status_code = status.HTTP_200_OK if result["valid"] else status.HTTP_401_UNAUTHORIZED
        
        return JSONResponse(
            status_code=status_code,
            content=result
        )
        
    except Exception as e:
        logger.error(f"Credential validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Credential validation failed: {str(e)}"
        )

@router.get(
    "/limits",
    response_model=SearchLimitsResponse,
    summary="Get search limits",
    description="Get current search limits and configuration"
)
async def get_search_limits() -> SearchLimitsResponse:
    """
    Get search limits and configuration.
    
    Returns the current search limits and timing configuration.
    """
    try:
        limits = search_service.get_search_limits()
        return SearchLimitsResponse(**limits)
        
    except Exception as e:
        logger.error(f"Get limits error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get search limits: {str(e)}"
        ) 