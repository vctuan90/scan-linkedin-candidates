"""
Search service for LinkedIn profile searches.
"""

import logging
from typing import List, Optional, Dict, Any

from ..scrapers.selenium_scraper import SeleniumScraper
from ..utils.helpers import validate_search_params, format_search_results, format_error_response
from ...config.settings import settings
from ...config.constants import API_MESSAGES

logger = logging.getLogger(__name__)

class SearchService:
    """Service for handling LinkedIn profile searches."""
    
    def __init__(self):
        self.logger = logger
    
    async def search_profiles(
        self,
        job_title: str,
        location: str,
        keywords: Optional[List[str]] = None,
        max_results: int = 50
    ) -> Dict[str, Any]:
        """
        Search for LinkedIn profiles based on criteria.
        
        Args:
            job_title: Job title to search for
            location: Location to search in
            keywords: Optional list of keywords
            max_results: Maximum number of results to return
            
        Returns:
            Dictionary containing search results or error information
        """
        try:
            # Validate input parameters
            if not validate_search_params(job_title, location, keywords):
                return format_error_response(
                    "Invalid search parameters. Job title and location are required.",
                    "INVALID_PARAMS"
                )
            
            # Limit max_results to prevent abuse
            max_results = min(max_results, settings.MAX_RESULTS)
            
            self.logger.info(f"Starting search: {job_title} in {location}")
            
            # Perform the search using Selenium scraper
            async with SeleniumScraper() as scraper:
                profile_urls = await scraper.search_with_retry(
                    job_title=job_title,
                    location=location,
                    keywords=keywords,
                    max_results=max_results,
                    max_retries=settings.MAX_RETRIES
                )
            
            self.logger.info(f"Search completed. Found {len(profile_urls)} profiles")
            
            return format_search_results(profile_urls, len(profile_urls))
            
        except Exception as e:
            error_msg = f"Search failed: {str(e)}"
            self.logger.error(error_msg)
            return format_error_response(error_msg, "SEARCH_ERROR")
    
    async def validate_credentials(self) -> Dict[str, Any]:
        """
        Validate LinkedIn credentials by attempting to login.
        
        Returns:
            Dictionary containing validation results
        """
        try:
            if not settings.LINKEDIN_EMAIL or not settings.LINKEDIN_PASSWORD:
                return {
                    "valid": False,
                    "message": "LinkedIn credentials not configured"
                }
            
            async with SeleniumScraper() as scraper:
                login_success = await scraper.login()
                
                if login_success:
                    return {
                        "valid": True,
                        "message": "LinkedIn credentials are valid"
                    }
                else:
                    return {
                        "valid": False,
                        "message": "LinkedIn login failed. Please check your credentials."
                    }
                    
        except Exception as e:
            self.logger.error(f"Credential validation failed: {str(e)}")
            return {
                "valid": False,
                "message": f"Credential validation error: {str(e)}"
            }
    
    def get_search_limits(self) -> Dict[str, int]:
        """
        Get current search limits and settings.
        
        Returns:
            Dictionary containing search limits
        """
        return {
            "max_results_per_search": settings.MAX_RESULTS,
            "min_delay_seconds": settings.MIN_DELAY,
            "max_delay_seconds": settings.MAX_DELAY,
            "max_retries": settings.MAX_RETRIES,
            "scroll_pause_time": settings.SCROLL_PAUSE_TIME
        } 