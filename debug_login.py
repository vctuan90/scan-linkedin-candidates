#!/usr/bin/env python3
"""
Debug script to test LinkedIn login
"""

import asyncio
import logging
from app.core.linkedin_scraper import LinkedInScraper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_login():
    """Test LinkedIn login process."""
    print("🔍 Testing LinkedIn login...")
    
    async with LinkedInScraper() as scraper:
        print("✅ Browser started successfully")
        
        # Test login
        login_success = await scraper.login()
        
        if login_success:
            print("✅ Login successful!")
            
            # Test a simple navigation
            try:
                await scraper.page.goto("https://www.linkedin.com/feed/", timeout=30000)
                print("✅ Successfully navigated to feed")
                
                # Wait a bit to see the page
                await asyncio.sleep(5)
                
            except Exception as e:
                print(f"❌ Navigation failed: {e}")
        else:
            print("❌ Login failed")
            
        print("🔍 Current URL:", scraper.page.url if scraper.page else "No page")

if __name__ == "__main__":
    asyncio.run(test_login()) 