#!/usr/bin/env python3
"""
Platform compatibility test script
Tests the LinkedIn Profile Scraper API on different platforms
"""

import platform
import sys
import os
import subprocess
import requests
import time

def get_platform_info():
    """Get detailed platform information."""
    return {
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'python_version': platform.python_version(),
        'architecture': platform.architecture()
    }

def test_python_environment():
    """Test Python environment."""
    print("🐍 Testing Python Environment...")
    
    info = get_platform_info()
    print(f"   System: {info['system']} {info['release']}")
    print(f"   Python: {info['python_version']}")
    print(f"   Architecture: {info['architecture'][0]}")
    
    # Check Python version
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print("   ✅ Python version is compatible")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor} is too old. Need 3.8+")
        return False

def test_dependencies():
    """Test if all dependencies are installed."""
    print("📦 Testing Dependencies...")
    
    required_packages = [
        'fastapi',
        'uvicorn', 
        'selenium',
        'webdriver_manager',
        'pydantic',
        'requests'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package}")
            missing.append(package)
    
    return len(missing) == 0

def test_chrome_browser():
    """Test if Chrome browser is available."""
    print("🌐 Testing Chrome Browser...")
    
    system = platform.system()
    
    if system == "Windows":
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
        ]
        for path in chrome_paths:
            if os.path.exists(path):
                print("   ✅ Chrome browser found")
                return True
        print("   ❌ Chrome browser not found")
        return False
        
    elif system == "Darwin":  # macOS
        chrome_path = "/Applications/Google Chrome.app"
        if os.path.exists(chrome_path):
            print("   ✅ Chrome browser found")
            return True
        print("   ❌ Chrome browser not found")
        return False
        
    elif system == "Linux":
        try:
            result = subprocess.run(['which', 'google-chrome'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("   ✅ Chrome browser found")
                return True
            
            result = subprocess.run(['which', 'chromium-browser'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("   ✅ Chromium browser found")
                return True
                
            print("   ❌ Chrome/Chromium browser not found")
            return False
        except:
            print("   ⚠️  Could not check Chrome installation")
            return True
    
    return True

def test_virtual_environment():
    """Test if running in virtual environment."""
    print("🔧 Testing Virtual Environment...")
    
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("   ✅ Running in virtual environment")
        return True
    else:
        print("   ⚠️  Not running in virtual environment (recommended)")
        return True

def test_env_file():
    """Test if .env file exists and is configured."""
    print("⚙️  Testing Environment Configuration...")
    
    if os.path.exists('.env'):
        print("   ✅ .env file exists")
        
        # Check if it has LinkedIn credentials
        try:
            with open('.env', 'r') as f:
                content = f.read()
                if 'LINKEDIN_EMAIL=' in content and 'LINKEDIN_PASSWORD=' in content:
                    if 'your_email@example.com' not in content:
                        print("   ✅ LinkedIn credentials configured")
                        return True
                    else:
                        print("   ⚠️  LinkedIn credentials need to be updated")
                        return False
                else:
                    print("   ❌ LinkedIn credentials not found in .env")
                    return False
        except Exception as e:
            print(f"   ❌ Error reading .env file: {e}")
            return False
    else:
        print("   ❌ .env file not found")
        return False

def test_api_startup():
    """Test if API can start (basic import test)."""
    print("🚀 Testing API Startup...")
    
    try:
        # Test basic imports
        from app.main import app
        from app.core.linkedin_scraper_selenium import LinkedInScraperSelenium
        print("   ✅ API imports successful")
        return True
    except Exception as e:
        print(f"   ❌ API import failed: {e}")
        return False

def main():
    """Run all platform tests."""
    print("🧪 LinkedIn Profile Scraper API - Platform Compatibility Test")
    print("=" * 70)
    
    info = get_platform_info()
    print(f"🖥️  Platform: {info['system']} {info['release']} ({info['machine']})")
    print(f"🐍 Python: {info['python_version']}")
    print("=" * 70)
    
    tests = [
        ("Python Environment", test_python_environment),
        ("Dependencies", test_dependencies),
        ("Chrome Browser", test_chrome_browser),
        ("Virtual Environment", test_virtual_environment),
        ("Environment Configuration", test_env_file),
        ("API Startup", test_api_startup)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   ❌ Test failed with error: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 70)
    print("📊 Test Results Summary:")
    print("=" * 70)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:8} {test_name}")
        if result:
            passed += 1
    
    print("=" * 70)
    print(f"📈 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Your platform is fully compatible.")
        print("\n🚀 You can now run:")
        system = platform.system()
        if system == "Windows":
            print("   setup.bat")
            print("   start.bat")
        else:
            print("   ./setup.sh")
            print("   python start.py")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        print("\n📚 Setup instructions:")
        system = platform.system()
        if system == "Windows":
            print("   Run: setup.bat")
        else:
            print("   Run: ./setup.sh")

if __name__ == "__main__":
    main() 