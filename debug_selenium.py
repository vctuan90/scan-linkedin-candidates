#!/usr/bin/env python3
"""
Debug script to test LinkedIn login with Selenium
"""

import asyncio
import logging
from app.core.linkedin_scraper_selenium import LinkedInScraperSelenium

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_selenium_login():
    """Test LinkedIn login process with Selenium."""
    print("🔍 Testing LinkedIn login with Selenium...")
    
    try:
        async with LinkedInScraperSelenium() as scraper:
            print("✅ Browser started successfully")
            
            # Test login
            login_success = await scraper.login()
            
            if login_success:
                print("✅ Login successful!")
                
                # Test a simple navigation
                try:
                    scraper.driver.get("https://www.linkedin.com/feed/")
                    await asyncio.sleep(3)
                    print("✅ Successfully navigated to feed")
                    
                    # Wait a bit to see the page
                    await asyncio.sleep(5)
                    
                except Exception as e:
                    print(f"❌ Navigation failed: {e}")
            else:
                print("❌ Login failed")
                
            print("🔍 Current URL:", scraper.driver.current_url if scraper.driver else "No driver")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_selenium_login()) 
 