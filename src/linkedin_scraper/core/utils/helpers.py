"""
Helper utility functions for LinkedIn scraping.
"""

import asyncio
import random
import re
from typing import List, Optional
from urllib.parse import urlparse, parse_qs

async def random_delay(min_seconds: float = 1, max_seconds: float = 3) -> None:
    """Add a random delay to simulate human behavior."""
    delay = random.uniform(min_seconds, max_seconds)
    await asyncio.sleep(delay)

def extract_profile_urls(html_content: str) -> List[str]:
    """Extract LinkedIn profile URLs from HTML content."""
    # Pattern to match LinkedIn profile URLs
    patterns = [
        r'https://www\.linkedin\.com/in/[a-zA-Z0-9\-]+/?',
        r'https://[a-z]{2}\.linkedin\.com/in/[a-zA-Z0-9\-]+/?',  # International domains
        r'/in/[a-zA-Z0-9\-]+/?'  # Relative URLs
    ]
    
    urls = []
    for pattern in patterns:
        found_urls = re.findall(pattern, html_content)
        urls.extend(found_urls)
    
    # Normalize relative URLs
    normalized_urls = []
    for url in urls:
        if url.startswith('/in/'):
            url = f"https://www.linkedin.com{url}"
        normalized_urls.append(url)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_urls = []
    for url in normalized_urls:
        clean_url = clean_profile_url(url)
        if clean_url not in seen:
            seen.add(clean_url)
            unique_urls.append(clean_url)
    
    return unique_urls

def build_search_query(job_title: str, location: str, keywords: Optional[List[str]] = None) -> str:
    """Build LinkedIn search query string."""
    query_parts = []
    
    if job_title:
        query_parts.append(f'"{job_title}"')
    
    if location:
        query_parts.append(f'"{location}"')
    
    if keywords:
        for keyword in keywords:
            if keyword.strip():  # Only add non-empty keywords
                query_parts.append(f'"{keyword.strip()}"')
    
    return " ".join(query_parts)

def clean_profile_url(url: str) -> str:
    """Clean and normalize LinkedIn profile URL."""
    if not url:
        return ""
    
    # Remove query parameters and fragments
    clean_url = url.split('?')[0].split('#')[0]
    
    # Ensure it's a valid LinkedIn profile URL
    if '/in/' not in clean_url:
        return ""
    
    # Normalize domain to www.linkedin.com
    if 'linkedin.com/in/' in clean_url:
        profile_id = clean_url.split('/in/')[-1].rstrip('/')
        clean_url = f"https://www.linkedin.com/in/{profile_id}"
    
    # Ensure it ends with a slash
    if not clean_url.endswith('/'):
        clean_url += '/'
    
    return clean_url

def validate_search_params(job_title: str, location: str, keywords: Optional[List[str]] = None) -> bool:
    """Validate search parameters."""
    if not job_title or not job_title.strip():
        return False
    
    if not location or not location.strip():
        return False
    
    if keywords:
        # Check if at least one keyword is valid
        valid_keywords = [k for k in keywords if k and k.strip()]
        if not valid_keywords:
            return False
    
    return True

def extract_profile_id(profile_url: str) -> Optional[str]:
    """Extract profile ID from LinkedIn URL."""
    if not profile_url or '/in/' not in profile_url:
        return None
    
    try:
        profile_id = profile_url.split('/in/')[-1].rstrip('/')
        # Remove any additional path segments
        profile_id = profile_id.split('/')[0]
        return profile_id if profile_id else None
    except:
        return None

def is_valid_linkedin_url(url: str) -> bool:
    """Check if URL is a valid LinkedIn profile URL."""
    if not url:
        return False
    
    try:
        parsed = urlparse(url)
        return (
            'linkedin.com' in parsed.netloc and
            '/in/' in parsed.path and
            len(parsed.path.split('/in/')[-1].strip('/')) > 0
        )
    except:
        return False

def format_search_results(profile_urls: List[str], total_found: int) -> dict:
    """Format search results for API response."""
    return {
        "success": True,
        "profiles": profile_urls,
        "total_found": total_found,
        "message": "Search completed successfully"
    }

def format_error_response(message: str, error_code: str = "SEARCH_FAILED") -> dict:
    """Format error response for API."""
    return {
        "success": False,
        "profiles": [],
        "total_found": 0,
        "message": message,
        "error_code": error_code
    } 