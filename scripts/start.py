#!/usr/bin/env python3
"""
Startup script for LinkedIn Profile Scraper API
Cross-platform support for Windows, macOS, and Linux
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def get_platform_info():
    """Get platform information."""
    system = platform.system()
    if system == "Windows":
        return "Windows"
    elif system == "Darwin":
        return "macOS"
    elif system == "Linux":
        return "Linux"
    else:
        return f"Unknown ({system})"

def check_requirements():
    """Check if all requirements are installed."""
    try:
        import fastapi
        import selenium
        import uvicorn
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please run the setup script first:")
        
        system = platform.system()
        if system == "Windows":
            print("  scripts\\setup.bat")
        else:
            print("  ./scripts/setup.sh")
        return False

def check_chrome_browser():
    """Check if Chrome browser is installed."""
    system = platform.system()
    
    if system == "Windows":
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
        ]
        for path in chrome_paths:
            if os.path.exists(path):
                print("✅ Chrome browser found")
                return True
        print("❌ Chrome browser not found")
        print("Please install Google Chrome from: https://www.google.com/chrome/")
        return False
        
    elif system == "Darwin":  # macOS
        chrome_path = "/Applications/Google Chrome.app"
        if os.path.exists(chrome_path):
            print("✅ Chrome browser found")
            return True
        print("❌ Chrome browser not found")
        print("Please install Google Chrome from: https://www.google.com/chrome/")
        return False
        
    elif system == "Linux":
        try:
            result = subprocess.run(['which', 'google-chrome'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Chrome browser found")
                return True
            
            result = subprocess.run(['which', 'chromium-browser'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Chromium browser found")
                return True
                
            print("❌ Chrome/Chromium browser not found")
            print("Please install: sudo apt-get install google-chrome-stable")
            print("Or: sudo apt-get install chromium-browser")
            return False
        except:
            print("⚠️  Could not check Chrome installation")
            return True  # Assume it's okay
    
    return True

def check_env_file():
    """Check if .env file exists."""
    env_file = Path('.env')
    if env_file.exists():
        print("✅ Environment file found")
        return True
    else:
        print("❌ .env file not found")
        print("Please create a .env file with your LinkedIn credentials")
        print("You can copy from env.example and modify it")
        return False

def main():
    """Main startup function."""
    platform_name = get_platform_info()
    print(f"🚀 Starting LinkedIn Profile Scraper API ({platform_name})")
    print("=" * 60)
    
    # Check all requirements
    checks = [
        check_requirements(),
        check_chrome_browser(),
        check_env_file()
    ]
    
    if not all(checks):
        print("\n❌ Some requirements are not met. Please fix the issues above.")
        print("\n📚 Setup instructions:")
        system = platform.system()
        if system == "Windows":
            print("  Run: scripts\\setup.bat")
        else:
            print("  Run: ./scripts/setup.sh")
        sys.exit(1)
    
    print("\n✅ All checks passed! Starting the API server...")
    print("📖 API Documentation will be available at: http://localhost:8000/docs")
    print("🔍 Search endpoint: http://localhost:8000/api/v1/search")
    print("🏥 Health check: http://localhost:8000/api/v1/health")
    print(f"\n🖥️  Platform: {platform_name}")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    
    # Start the server
    try:
        import sys
        import os
        
        # Add src to Python path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        src_path = os.path.join(project_root, 'src')
        
        if src_path not in sys.path:
            sys.path.insert(0, src_path)
        
        print(f"📁 Project root: {project_root}")
        print(f"📁 Source path: {src_path}")
        
        import uvicorn
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure all dependencies are installed")
        print("2. Check if port 8000 is available")
        print("3. Verify .env file configuration")
        sys.exit(1)

if __name__ == "__main__":
    main()