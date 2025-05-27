"""
Selenium-based LinkedIn scraper implementation.
"""

import asyncio
import logging
import random
import platform
import os
from typing import List, Optional
from urllib.parse import urlencode

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from .base import BaseScraper
from ...config.settings import settings
from ...config.constants import (
    LINKEDIN_LOGIN_URL, LINKEDIN_SEARCH_URL, USER_AGENTS, 
    CHROME_DRIVER_PATHS, LINKEDIN_SELECTORS
)
from ...core.utils.helpers import (
    random_delay, extract_profile_urls, build_search_query, clean_profile_url
)

logger = logging.getLogger(__name__)

class SeleniumScraper(BaseScraper):
    """Selenium-based LinkedIn scraper."""
    
    def __init__(self):
        super().__init__()
        self.driver: Optional[webdriver.Chrome] = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.start_browser()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close_browser()
    
    async def start_browser(self) -> None:
        """Start the Chrome browser with stealth settings."""
        try:
            chrome_options = self._get_chrome_options()
            service = self._get_chrome_service()
            
            # Create driver
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Execute script to remove webdriver property
            self.driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )
            
            # Set window size
            self.driver.set_window_size(1366, 768)
            
            self.logger.info("Browser started successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to start browser: {str(e)}")
            raise
    
    def _get_chrome_options(self) -> Options:
        """Get Chrome options with stealth settings."""
        chrome_options = Options()
        
        # Basic stealth options
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Headless mode
        if settings.HEADLESS_MODE:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1366,768")
            self.logger.info("Running in headless mode (background)")
        
        # Platform-specific settings
        system = platform.system().lower()
        if system == "linux":
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--remote-debugging-port=9222")
        
        # User agent
        user_agent = self._get_user_agent()
        chrome_options.add_argument(f"--user-agent={user_agent}")
        
        return chrome_options
    
    def _get_user_agent(self) -> str:
        """Get appropriate user agent for current platform."""
        system = platform.system().lower()
        if system == "windows":
            return USER_AGENTS['windows']
        elif system == "darwin":  # macOS
            return USER_AGENTS['macos']
        else:  # Linux
            return USER_AGENTS['linux']
    
    def _get_chrome_service(self) -> Service:
        """Get Chrome service with driver path."""
        try:
            driver_path = ChromeDriverManager().install()
            # Fix the path if it points to the wrong file
            if 'THIRD_PARTY_NOTICES.chromedriver' in driver_path:
                driver_path = driver_path.replace('THIRD_PARTY_NOTICES.chromedriver', 'chromedriver')
            return Service(driver_path)
        except Exception as e:
            self.logger.warning(f"ChromeDriverManager failed: {e}, trying system chromedriver")
            
            # Try platform-specific system paths
            system = platform.system().lower()
            system_paths = CHROME_DRIVER_PATHS.get(system, ['chromedriver'])
            
            for path in system_paths:
                if os.path.exists(path):
                    return Service(path)
            
            raise Exception(f"ChromeDriver not found for {system}. Please install Chrome and run setup script.")
    
    async def close_browser(self) -> None:
        """Close the browser."""
        try:
            if self.driver:
                self.driver.quit()
            self.logger.info("Browser closed successfully")
        except Exception as e:
            self.logger.error(f"Error closing browser: {str(e)}")
    
    def _wait_and_find_element(self, by, value, timeout=10):
        """Wait for element and return it."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            return None
    
    def _wait_and_click_element(self, by, value, timeout=10):
        """Wait for element to be clickable and click it."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            element.click()
            return True
        except TimeoutException:
            return False
    
    async def login(self) -> bool:
        """Login to LinkedIn."""
        if not settings.LINKEDIN_EMAIL or not settings.LINKEDIN_PASSWORD:
            self.logger.error("LinkedIn credentials not provided")
            return False
        
        try:
            self.logger.info("Attempting to login to LinkedIn")
            
            # Navigate to login page
            self.driver.get(LINKEDIN_LOGIN_URL)
            await asyncio.sleep(random.uniform(settings.MIN_DELAY, settings.MAX_DELAY))
            
            # Wait for login form
            email_field = self._wait_and_find_element(By.NAME, "session_key")
            password_field = self._wait_and_find_element(By.NAME, "session_password")
            
            if not email_field or not password_field:
                self.logger.error("Login form not found")
                return False
            
            # Fill login form
            email_field.clear()
            email_field.send_keys(settings.LINKEDIN_EMAIL)
            await asyncio.sleep(random.uniform(0.5, 1.5))
            
            password_field.clear()
            password_field.send_keys(settings.LINKEDIN_PASSWORD)
            await asyncio.sleep(random.uniform(0.5, 1.5))
            
            # Click login button
            login_button = self._wait_and_find_element(By.XPATH, "//button[@type='submit']")
            if login_button:
                login_button.click()
                await asyncio.sleep(random.uniform(5, 8))
            else:
                self.logger.error("Login button not found")
                return False
            
            # Check login status
            return await self._check_login_status()
            
        except Exception as e:
            self.logger.error(f"Login failed: {str(e)}")
            return False
    
    async def _check_login_status(self) -> bool:
        """Check if login was successful."""
        try:
            current_url = self.driver.current_url
            self.logger.info(f"Current URL after login attempt: {current_url}")
        except Exception as e:
            self.logger.error(f"Failed to get current URL: {e}")
            return False
        
        # Check for various success indicators
        if any(indicator in current_url for indicator in ['/feed/', '/in/', '/mynetwork/', '/jobs/']):
            self.is_logged_in = True
            self.logger.info("Successfully logged in to LinkedIn")
            return True
        
        # Check for challenge/verification pages
        if any(challenge in current_url for challenge in ['challenge', 'checkpoint', 'verify']):
            self.logger.warning("LinkedIn security challenge detected. Please complete verification manually.")
            return await self._handle_verification()
        
        # Check for login errors
        try:
            error_element = self.driver.find_element(By.CSS_SELECTOR, LINKEDIN_SELECTORS['error_message'])
            if error_element:
                error_text = error_element.text
                self.logger.error(f"Login failed: {error_text}")
                return False
        except NoSuchElementException:
            pass
        
        # If we're still on login page, login failed
        if 'login' in current_url:
            self.logger.error("Login failed - still on login page")
            return False
        
        # Default to success if we're not on login page
        self.is_logged_in = True
        self.logger.info("Login appears successful")
        return True
    
    async def _handle_verification(self) -> bool:
        """Handle LinkedIn verification challenge."""
        self.logger.info("Waiting for manual verification...")
        
        # Wait for user to complete verification (up to 2 minutes)
        for i in range(24):  # 24 * 5 seconds = 2 minutes
            await asyncio.sleep(5)
            current_url = self.driver.current_url
            if any(indicator in current_url for indicator in ['/feed/', '/in/', '/mynetwork/', '/jobs/']):
                self.is_logged_in = True
                self.logger.info("Verification completed successfully!")
                return True
            self.logger.info(f"Still waiting for verification... ({i+1}/24)")
        
        self.logger.error("Verification timeout. Please try again.")
        return False
    
    async def search_profiles(
        self, 
        job_title: str, 
        location: str, 
        keywords: Optional[List[str]] = None, 
        max_results: int = 50
    ) -> List[str]:
        """Search for LinkedIn profiles based on criteria."""
        if not self.is_logged_in:
            if not await self.login():
                raise Exception("Failed to login to LinkedIn")
        
        try:
            self.logger.info(f"Searching for profiles: {job_title} in {location}")
            
            # Build search parameters
            search_query = build_search_query(job_title, location, keywords)
            search_params = {
                'keywords': search_query,
                'origin': 'GLOBAL_SEARCH_HEADER'
            }
            
            # Construct search URL
            search_url = f"{LINKEDIN_SEARCH_URL}?{urlencode(search_params)}"
            self.logger.info(f"Navigating to search URL: {search_url}")
            
            # Navigate to search results
            self.driver.get(search_url)
            await asyncio.sleep(random.uniform(settings.MIN_DELAY, settings.MAX_DELAY))
            
            # Collect profile URLs
            profile_urls = []
            scroll_count = 0
            max_scrolls = max_results // 10  # Approximate profiles per page
            
            while len(profile_urls) < max_results and scroll_count < max_scrolls:
                # Extract current page content
                page_source = self.driver.page_source
                current_urls = extract_profile_urls(page_source)
                
                # Add new URLs
                for url in current_urls:
                    clean_url = clean_profile_url(url)
                    if clean_url not in profile_urls:
                        profile_urls.append(clean_url)
                
                self.logger.info(f"Found {len(profile_urls)} profiles so far")
                
                # Scroll to load more results
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                await asyncio.sleep(settings.SCROLL_PAUSE_TIME)
                
                # Check if "Show more results" button exists and click it
                try:
                    show_more_button = self.driver.find_element(
                        By.XPATH, "//button[contains(@aria-label, 'Show more results')]"
                    )
                    if show_more_button.is_displayed():
                        show_more_button.click()
                        await asyncio.sleep(random.uniform(2, 4))
                except NoSuchElementException:
                    pass
                
                scroll_count += 1
            
            # Limit results to max_results
            profile_urls = profile_urls[:max_results]
            
            self.logger.info(f"Search completed. Found {len(profile_urls)} profiles")
            return profile_urls
            
        except Exception as e:
            self.logger.error(f"Search failed: {str(e)}")
            raise 