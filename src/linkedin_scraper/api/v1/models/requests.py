"""
Request models for LinkedIn Scraper API.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, validator

class SearchRequest(BaseModel):
    """Request model for profile search."""
    
    job_title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Job title to search for",
        example="Country Manager"
    )
    
    location: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Location to search in",
        example="Saudi Arabia"
    )
    
    keywords: Optional[List[str]] = Field(
        None,
        description="Additional keywords for filtering",
        example=["FMCG", "Tobacco"]
    )
    
    max_results: int = Field(
        50,
        ge=1,
        le=100,
        description="Maximum number of results to return",
        example=50
    )
    
    @validator('job_title', 'location')
    def validate_non_empty_strings(cls, v):
        """Validate that strings are not empty or whitespace only."""
        if not v or not v.strip():
            raise ValueError('Field cannot be empty or whitespace only')
        return v.strip()
    
    @validator('keywords')
    def validate_keywords(cls, v):
        """Validate keywords list."""
        if v is not None:
            # Filter out empty or whitespace-only keywords
            valid_keywords = [k.strip() for k in v if k and k.strip()]
            return valid_keywords if valid_keywords else None
        return v
    
    class Config:
        """Pydantic config."""
        schema_extra = {
            "example": {
                "job_title": "Country Manager",
                "location": "Saudi Arabia",
                "keywords": ["FMCG", "Tobacco"],
                "max_results": 50
            }
        } 