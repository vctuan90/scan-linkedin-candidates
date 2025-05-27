# LinkedIn Profile Scraper API

A modern FastAPI application that automates LinkedIn search and returns matching candidate profile URLs. This API simulates human-like browsing behavior to search for profiles based on job titles, locations, and keywords with advanced anti-detection features.

## 🚀 Features

- **Automated LinkedIn Search**: Search profiles based on job title, location, and keywords
- **Human-like Browsing**: Simulates human behavior with random delays and user agents
- **Headless Mode**: Runs browser in background without visible window
- **Anti-Detection**: Advanced stealth measures to avoid LinkedIn detection
- **Rate Limiting**: Built-in throttling and retry mechanisms
- **Modern Architecture**: Clean, modular, and extensible codebase
- **Comprehensive API**: RESTful API with auto-generated documentation
- **Cross-Platform**: Supports Windows, macOS, and Linux

## 📁 Project Structure

```
ScanLinkedIn/
├── src/                          # Source code
│   ├── linkedin_scraper/         # Main package
│   │   ├── config/               # Configuration
│   │   │   ├── settings.py       # App settings
│   │   │   └── constants.py      # Constants
│   │   ├── core/                 # Business logic
│   │   │   ├── scrapers/         # Scraper implementations
│   │   │   │   ├── base.py       # Base scraper class
│   │   │   │   └── selenium_scraper.py
│   │   │   ├── services/         # Business services
│   │   │   │   └── search_service.py
│   │   │   └── utils/            # Utilities
│   │   │       └── helpers.py
│   │   ├── api/                  # API layer
│   │   │   └── v1/               # API version 1
│   │   │       ├── endpoints/    # API endpoints
│   │   │       │   ├── search.py
│   │   │       │   └── health.py
│   │   │       └── models/       # Pydantic models
│   │   │           ├── requests.py
│   │   │           └── responses.py
│   │   ├── database/             # Database (future)
│   │   └── exceptions/           # Custom exceptions
│   └── main.py                   # FastAPI app entry point
├── tests/                        # Test files
│   ├── unit/                     # Unit tests
│   ├── integration/              # Integration tests
│   ├── e2e/                      # End-to-end tests
│   └── fixtures/                 # Test fixtures
├── scripts/                      # Utility scripts
│   ├── setup.sh                  # Setup script (Linux/macOS)
│   ├── setup.bat                 # Setup script (Windows)
│   ├── start.py                  # Cross-platform startup
│   └── test_platform.py          # Platform compatibility test
├── docs/                         # Documentation
├── docker/                       # Docker files
├── requirements/                 # Requirements files
│   ├── base.txt                  # Base dependencies
│   ├── dev.txt                   # Development dependencies
│   └── prod.txt                  # Production dependencies
├── pyproject.toml               # Modern Python project config
├── start_simple.py              # Simple startup script
└── README.md                    # This file
```

## 🛠️ Setup

### Quick Setup (Recommended)

Choose the setup method for your operating system:

#### 🪟 **Windows**
```cmd
scripts\setup.bat
```

#### 🐧 **Linux / 🍎 macOS**
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### Manual Setup

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd ScanLinkedIn
```

#### 2. Create Virtual Environment

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
# Install base dependencies
pip install -r requirements/base.txt

# For development
pip install -r requirements/dev.txt

# For production
pip install -r requirements/prod.txt
```

#### 4. Install Chrome Browser

- **Windows**: Download from [Google Chrome](https://www.google.com/chrome/)
- **macOS**: Download from [Google Chrome](https://www.google.com/chrome/) or `brew install --cask google-chrome`
- **Linux**: `sudo apt-get install google-chrome-stable` or `sudo apt-get install chromium-browser`

#### 5. Environment Configuration

Create a `.env` file in the root directory:

**Windows:**
```cmd
copy env.example .env
notepad .env
```

**Linux/macOS:**
```bash
cp env.example .env
nano .env  # or vim .env, code .env
```

Edit the `.env` file with your configuration:

```env
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
DEBUG=True
HEADLESS_MODE=True
LOG_LEVEL=INFO
API_HOST=0.0.0.0
API_PORT=8000
```

⚠️ **Important**: Use a dedicated LinkedIn account for scraping to avoid issues with your main account.

## 🚀 Running the Application

### Quick Start

#### Simple Method (Recommended)
```bash
python start_simple.py
```

#### Using Scripts
**Windows:**
```cmd
python scripts\start.py
```

**Linux/macOS:**
```bash
python scripts/start.py
```

#### Direct Method
```bash
cd src
python main.py
```

### Development Mode

```bash
cd src
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
cd src
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: `http://localhost:8000`
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 📖 API Documentation

### Endpoints Overview

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root endpoint with API info |
| `/api/v1/health` | GET | Health check |
| `/api/v1/search` | POST | Search LinkedIn profiles |
| `/api/v1/validate-credentials` | GET | Validate LinkedIn credentials |
| `/api/v1/limits` | GET | Get search limits |

### Search Endpoint

**POST** `/api/v1/search`

Search for LinkedIn profiles based on criteria.

#### Request Body

```json
{
    "job_title": "Country Manager",
    "location": "Saudi Arabia",
    "keywords": ["FMCG", "Tobacco"],
    "max_results": 50
}
```

#### Parameters

- `job_title` (string, required): Job title to search for
- `location` (string, required): Location to search in
- `keywords` (array, optional): Additional keywords for filtering
- `max_results` (integer, optional): Maximum number of results (1-100, default: 50)

#### Response

```json
{
    "success": true,
    "profiles": [
        "https://www.linkedin.com/in/john-doe/",
        "https://www.linkedin.com/in/jane-smith/"
    ],
    "total_found": 2,
    "message": "Search completed successfully"
}
```

### Health Check

**GET** `/api/v1/health`

Check if the API is running.

#### Response

```json
{
    "status": "healthy",
    "message": "LinkedIn Scraper API is running",
    "version": "1.0.0",
    "timestamp": "2024-01-01T12:00:00Z"
}
```

### Credential Validation

**GET** `/api/v1/validate-credentials`

Validate LinkedIn credentials.

#### Response

```json
{
    "valid": true,
    "message": "LinkedIn credentials are valid"
}
```

### Search Limits

**GET** `/api/v1/limits`

Get current search limits and configuration.

#### Response

```json
{
    "max_results_per_search": 100,
    "min_delay_seconds": 2,
    "max_delay_seconds": 5,
    "max_retries": 3,
    "scroll_pause_time": 2
}
```

## 🔧 Usage Examples

### Using cURL

**Linux/macOS:**
```bash
curl -X POST "http://localhost:8000/api/v1/search" \
     -H "Content-Type: application/json" \
     -d '{
       "job_title": "Country Manager",
       "location": "Saudi Arabia",
       "keywords": ["FMCG", "Tobacco"],
       "max_results": 20
     }'
```

**Windows (PowerShell):**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/search" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{
    "job_title": "Country Manager",
    "location": "Saudi Arabia", 
    "keywords": ["FMCG", "Tobacco"],
    "max_results": 20
  }'
```

### Using Python requests

```python
import requests

url = "http://localhost:8000/api/v1/search"
data = {
    "job_title": "Country Manager",
    "location": "Saudi Arabia",
    "keywords": ["FMCG", "Tobacco"],
    "max_results": 20
}

response = requests.post(url, json=data)
result = response.json()

if result["success"]:
    print(f"Found {result['total_found']} profiles:")
    for profile in result["profiles"]:
        print(f"- {profile}")
else:
    print(f"Search failed: {result['message']}")
```

### Using JavaScript/Node.js

```javascript
const axios = require('axios');

const searchProfiles = async () => {
    try {
        const response = await axios.post('http://localhost:8000/api/v1/search', {
            job_title: 'Country Manager',
            location: 'Saudi Arabia',
            keywords: ['FMCG', 'Tobacco'],
            max_results: 20
        });

        if (response.data.success) {
            console.log(`Found ${response.data.total_found} profiles:`);
            response.data.profiles.forEach(profile => {
                console.log(`- ${profile}`);
            });
        } else {
            console.log(`Search failed: ${response.data.message}`);
        }
    } catch (error) {
        console.error('Error:', error.message);
    }
};

searchProfiles();
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LINKEDIN_EMAIL` | Your LinkedIn email address | - |
| `LINKEDIN_PASSWORD` | Your LinkedIn password | - |
| `DEBUG` | Enable debug mode | `False` |
| `HEADLESS_MODE` | Run browser in background | `True` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `API_HOST` | API host | `0.0.0.0` |
| `API_PORT` | API port | `8000` |

### Scraping Settings

You can modify these in `src/linkedin_scraper/config/settings.py`:

- `MIN_DELAY`: Minimum delay between actions (default: 2 seconds)
- `MAX_DELAY`: Maximum delay between actions (default: 5 seconds)
- `MAX_RETRIES`: Maximum number of retries (default: 3)
- `SCROLL_PAUSE_TIME`: Time to pause between scrolls (default: 2 seconds)
- `MAX_RESULTS`: Maximum number of results (default: 100)

## 🛡️ Anti-Detection Features

The scraper includes several anti-detection measures:

1. **Random User Agents**: Platform-specific user agents
2. **Human-like Delays**: Random delays between actions
3. **Stealth Browser Settings**: Disables automation detection
4. **Scroll Simulation**: Mimics human scrolling behavior
5. **Retry Logic**: Handles temporary failures gracefully
6. **Headless Mode**: Runs browser in background without visible window

## 🧪 Testing

### Run Platform Compatibility Test

```bash
python scripts/test_platform.py
```

### Run Unit Tests

```bash
pytest tests/unit/
```

### Run Integration Tests

```bash
pytest tests/integration/
```

### Run All Tests

```bash
pytest
```

## 🐳 Docker Support

### Build Docker Image

```bash
docker build -t linkedin-scraper .
```

### Run with Docker Compose

```bash
docker-compose up -d
```

## 📊 Development

### Install Development Dependencies

```bash
pip install -r requirements/dev.txt
```

### Code Formatting

```bash
black src/
```

### Type Checking

```bash
mypy src/
```

### Linting

```bash
flake8 src/
```

## ⚠️ Important Notes

1. **Rate Limiting**: LinkedIn has rate limits. The API includes built-in delays to respect these limits.

2. **Account Safety**: Use a dedicated LinkedIn account for scraping to avoid issues with your main account.

3. **Legal Compliance**: Ensure your use case complies with LinkedIn's Terms of Service and applicable laws.

4. **Captcha Handling**: The scraper may encounter captchas or security challenges. Monitor logs for such issues.

5. **IP Blocking**: Consider using proxies or VPNs if you encounter IP-based blocking.

## 🖥️ Platform Support

This API is fully tested and supported on:

### ✅ **Windows**
- Windows 10/11
- Python 3.8+
- Google Chrome browser
- PowerShell or Command Prompt

### ✅ **macOS**
- macOS 10.15+ (Catalina and later)
- Python 3.8+
- Google Chrome browser
- Terminal with bash/zsh

### ✅ **Linux**
- Ubuntu 18.04+, Debian 10+, CentOS 7+
- Python 3.8+
- Google Chrome or Chromium browser
- bash shell

## 🔮 Future Enhancements

- [ ] Profile data extraction (not just URLs)
- [ ] Batch processing for multiple searches
- [ ] Database integration for storing results
- [ ] Advanced filtering options
- [ ] Export to CSV/Excel
- [ ] Webhook notifications
- [ ] Proxy rotation support
- [ ] Kubernetes deployment support
- [ ] Real-time search monitoring
- [ ] Search analytics and reporting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Run tests and ensure they pass
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Submit a pull request

## 📄 License

This project is for educational and research purposes. Please ensure compliance with LinkedIn's Terms of Service and applicable laws.

## 📞 Support

If you encounter any issues or have questions:

1. Check the [troubleshooting section](#-important-notes)
2. Run the platform compatibility test: `python scripts/test_platform.py`
3. Check the logs for error messages
4. Create an issue in the repository with detailed information

---

**Made with ❤️ for the developer community** 