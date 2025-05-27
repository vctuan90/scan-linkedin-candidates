#!/bin/bash
# Script to activate virtual environment
# Usage: source scripts/activate_env.sh

echo "🔄 Activating virtual environment..."

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
VENV_PATH="$PROJECT_ROOT/venv"

if [ -d "$VENV_PATH" ]; then
    source "$VENV_PATH/bin/activate"
    echo "✅ Virtual environment activated"
    echo "📁 Project root: $PROJECT_ROOT"
    echo "🐍 Python: $(which python)"
    echo ""
    echo "🚀 You can now run:"
    echo "   python start_simple.py"
    echo "   python scripts/start.py"
    echo "   python scripts/test_platform.py"
else
    echo "❌ Virtual environment not found at: $VENV_PATH"
    echo "Please run setup first: ./scripts/setup.sh"
fi 