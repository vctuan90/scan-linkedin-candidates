"""
Response models for LinkedIn Scraper API.
"""

from typing import List, Optional
from pydantic import BaseModel, Field

class SearchResponse(BaseModel):
    """Response model for profile search."""
    
    success: bool = Field(
        ...,
        description="Whether the search was successful"
    )
    
    profiles: List[str] = Field(
        ...,
        description="List of LinkedIn profile URLs"
    )
    
    total_found: int = Field(
        ...,
        description="Total number of profiles found"
    )
    
    message: str = Field(
        ...,
        description="Status message"
    )
    
    error_code: Optional[str] = Field(
        None,
        description="Error code if search failed"
    )
    
    class Config:
        """Pydantic config."""
        schema_extra = {
            "example": {
                "success": True,
                "profiles": [
                    "https://www.linkedin.com/in/john-doe/",
                    "https://www.linkedin.com/in/jane-smith/"
                ],
                "total_found": 2,
                "message": "Search completed successfully"
            }
        }

class HealthResponse(BaseModel):
    """Response model for health check."""
    
    status: str = Field(
        ...,
        description="Health status"
    )
    
    message: str = Field(
        ...,
        description="Health message"
    )
    
    version: str = Field(
        "1.0.0",
        description="API version"
    )
    
    timestamp: str = Field(
        ...,
        description="Current timestamp"
    )
    
    class Config:
        """Pydantic config."""
        schema_extra = {
            "example": {
                "status": "healthy",
                "message": "LinkedIn Scraper API is running",
                "version": "1.0.0",
                "timestamp": "2024-01-01T12:00:00Z"
            }
        }

class CredentialValidationResponse(BaseModel):
    """Response model for credential validation."""
    
    valid: bool = Field(
        ...,
        description="Whether credentials are valid"
    )
    
    message: str = Field(
        ...,
        description="Validation message"
    )
    
    class Config:
        """Pydantic config."""
        schema_extra = {
            "example": {
                "valid": True,
                "message": "LinkedIn credentials are valid"
            }
        }

class SearchLimitsResponse(BaseModel):
    """Response model for search limits."""
    
    max_results_per_search: int = Field(
        ...,
        description="Maximum results per search"
    )
    
    min_delay_seconds: int = Field(
        ...,
        description="Minimum delay between actions"
    )
    
    max_delay_seconds: int = Field(
        ...,
        description="Maximum delay between actions"
    )
    
    max_retries: int = Field(
        ...,
        description="Maximum number of retries"
    )
    
    scroll_pause_time: int = Field(
        ...,
        description="Scroll pause time in seconds"
    )
    
    class Config:
        """Pydantic config."""
        schema_extra = {
            "example": {
                "max_results_per_search": 100,
                "min_delay_seconds": 2,
                "max_delay_seconds": 5,
                "max_retries": 3,
                "scroll_pause_time": 2
            }
        } 