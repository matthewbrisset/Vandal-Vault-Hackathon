#!/bin/bash
# Vandal Vault - Setup Script for macOS/Linux
# Run this script after cloning the repo to set up the project

echo "🚀 Vandal Vault - Setup Script"
echo "================================"
echo ""

# Check if Python is installed
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "✗ Python not found. Please install Python 3.9+ first."
    exit 1
fi
python_version=$(python3 --version)
echo "✓ $python_version found"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Verify pytest installation
echo ""
echo "Verifying pytest installation..."
if ! pytest --version &> /dev/null; then
    echo "Installing pytest explicitly..."
    pip install pytest
fi
echo "✓ pytest is ready"

# Create .env file if it doesn't exist
echo ""
echo "Setting up environment variables..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ .env file created (add your GROQ_API_KEY)"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "================================"
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Add GROQ_API_KEY to .env"
echo "  2. Run tests: pytest tests/ -v"
echo "  3. Start Flask server: python -m src.Backend.app"
echo "  4. Open http://localhost:5000 in your browser"
echo ""
