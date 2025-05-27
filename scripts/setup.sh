#!/bin/bash

echo "🚀 LinkedIn Profile Scraper API Setup"
echo "====================================="

# Detect operating system
OS="unknown"
case "$(uname -s)" in
    Linux*)     OS=Linux;;
    Darwin*)    OS=Mac;;
    CYGWIN*)    OS=Cygwin;;
    MINGW*)     OS=MinGw;;
    MSYS*)      OS=Windows;;
    *)          OS="UNKNOWN:$(uname -s)"
esac

echo "🖥️  Detected OS: $OS"

# Check if Python is installed
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    if command -v python &> /dev/null; then
        PYTHON_CMD="python"
        echo "⚠️  Using 'python' command instead of 'python3'"
    else
        echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
        echo "📖 Installation guides:"
        echo "   - Windows: https://www.python.org/downloads/windows/"
        echo "   - macOS: brew install python3 or https://www.python.org/downloads/mac-osx/"
        echo "   - Linux: sudo apt-get install python3 python3-pip (Ubuntu/Debian)"
        exit 1
    fi
fi

echo "✅ Python found: $($PYTHON_CMD --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment based on OS
echo "🔄 Activating virtual environment..."
if [[ "$OS" == "Windows" || "$OS" == "Cygwin" || "$OS" == "MinGw" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Install ChromeDriver based on OS
echo "🌐 Setting up ChromeDriver..."
if [[ "$OS" == "Mac" ]]; then
    if command -v brew &> /dev/null; then
        echo "🍺 Installing ChromeDriver via Homebrew..."
        brew install --cask chromedriver 2>/dev/null || echo "ChromeDriver may already be installed"
    else
        echo "⚠️  Homebrew not found. ChromeDriver will be downloaded automatically."
    fi
elif [[ "$OS" == "Linux" ]]; then
    echo "🐧 ChromeDriver will be downloaded automatically for Linux"
elif [[ "$OS" == "Windows" || "$OS" == "Cygwin" || "$OS" == "MinGw" ]]; then
    echo "🪟 ChromeDriver will be downloaded automatically for Windows"
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please edit .env file with your LinkedIn credentials"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your LinkedIn credentials:"
if [[ "$OS" == "Windows" || "$OS" == "Cygwin" || "$OS" == "MinGw" ]]; then
    echo "   notepad .env"
else
    echo "   nano .env  # or vim .env, code .env"
fi
echo ""
echo "2. Start the API:"
if [[ "$OS" == "Windows" || "$OS" == "Cygwin" || "$OS" == "MinGw" ]]; then
    echo "   python start.py"
else
    echo "   python start.py  # or ./start.py"
fi
echo ""
echo "3. Visit: http://localhost:8000/docs"
echo ""
echo "For testing, run: python test_api.py"
echo ""
echo "📚 Platform-specific notes:"
echo "   - Windows: Make sure Chrome browser is installed"
echo "   - macOS: Chrome will be detected automatically"
echo "   - Linux: Install google-chrome or chromium-browser" 