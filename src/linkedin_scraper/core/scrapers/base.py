"""
Base scraper class for LinkedIn scrapers.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    """Abstract base class for LinkedIn scrapers."""
    
    def __init__(self):
        self.is_logged_in = False
        self.logger = logger
    
    @abstractmethod
    async def __aenter__(self):
        """Async context manager entry."""
        pass
    
    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        pass
    
    @abstractmethod
    async def start_browser(self) -> None:
        """Start the browser."""
        pass
    
    @abstractmethod
    async def close_browser(self) -> None:
        """Close the browser."""
        pass
    
    @abstractmethod
    async def login(self) -> bool:
        """Login to LinkedIn."""
        pass
    
    @abstractmethod
    async def search_profiles(
        self, 
        job_title: str, 
        location: str, 
        keywords: Optional[List[str]] = None, 
        max_results: int = 50
    ) -> List[str]:
        """Search for LinkedIn profiles."""
        pass
    
    async def search_with_retry(
        self, 
        job_title: str, 
        location: str, 
        keywords: Optional[List[str]] = None, 
        max_results: int = 50,
        max_retries: int = 3
    ) -> List[str]:
        """Search with retry logic."""
        for attempt in range(max_retries):
            try:
                return await self.search_profiles(job_title, location, keywords, max_results)
            except Exception as e:
                self.logger.warning(f"Search attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    import asyncio
                    import random
                    await asyncio.sleep(random.uniform(5, 10))
                else:
                    raise e 