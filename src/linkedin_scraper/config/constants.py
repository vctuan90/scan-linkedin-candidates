"""
Application constants.
"""

# LinkedIn URLs
LINKEDIN_BASE_URL = "https://www.linkedin.com"
LINKEDIN_LOGIN_URL = f"{LINKEDIN_BASE_URL}/login"
LINKEDIN_SEARCH_URL = f"{LINKEDIN_BASE_URL}/search/results/people/"
LINKEDIN_FEED_URL = f"{LINKEDIN_BASE_URL}/feed/"

# User agents for different platforms
USER_AGENTS = {
    'windows': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    'macos': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    'linux': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
}

# Chrome driver paths for different platforms
CHROME_DRIVER_PATHS = {
    'darwin': ['/opt/homebrew/bin/chromedriver', '/usr/local/bin/chromedriver'],
    'linux': ['/usr/bin/chromedriver', '/usr/local/bin/chromedriver'],
    'windows': ['chromedriver.exe']
}

# Search result selectors
LINKEDIN_SELECTORS = {
    'profile_links': 'a[href*="/in/"]',
    'search_results': '.search-result__wrapper',
    'show_more_button': 'button[aria-label*="Show more results"]',
    'login_email': 'input[name="session_key"]',
    'login_password': 'input[name="session_password"]',
    'login_submit': 'button[type="submit"]',
    'error_message': '.form__label--error'
}

# HTTP status codes
HTTP_STATUS = {
    'OK': 200,
    'BAD_REQUEST': 400,
    'UNAUTHORIZED': 401,
    'FORBIDDEN': 403,
    'NOT_FOUND': 404,
    'TOO_MANY_REQUESTS': 429,
    'INTERNAL_SERVER_ERROR': 500
}

# API response messages
API_MESSAGES = {
    'SEARCH_SUCCESS': 'Search completed successfully',
    'SEARCH_FAILED': 'Search failed',
    'LOGIN_FAILED': 'LinkedIn login failed',
    'INVALID_CREDENTIALS': 'Invalid LinkedIn credentials',
    'RATE_LIMITED': 'Rate limit exceeded',
    'HEALTH_OK': 'LinkedIn Scraper API is running'
} 