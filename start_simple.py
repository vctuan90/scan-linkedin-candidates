#!/usr/bin/env python3
"""
Simple startup script for LinkedIn Profile Scraper API
"""

import sys
import os

# Add src to Python path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting LinkedIn Profile Scraper API")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔍 Search endpoint: http://localhost:8000/api/v1/search")
    print("🏥 Health check: http://localhost:8000/api/v1/health")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 