#!/bin/bash

# Knowledge Base Search Engine - Setup Script
# This script automates the installation process

set -e  # Exit on error

echo "🔍 Knowledge Base Search Engine - Setup"
echo "========================================"
echo ""

# Check Python version
echo "📋 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Found Python $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv venv
echo "✅ Virtual environment created"
echo ""

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✅ pip upgraded"
echo ""

# Install dependencies
echo "📦 Installing dependencies (this may take a few minutes)..."
cd backend
pip install -r requirements.txt
cd ..
echo "✅ All dependencies installed"
echo ""

# Create docs directory if it doesn't exist
echo "📁 Setting up documents folder..."
mkdir -p backend/app/docs
echo "✅ Documents folder ready"
echo ""

# Success message
echo "🎉 Setup complete!"
echo ""
echo "📖 Next steps:"
echo "1. Add your documents (.txt or .pdf) to: backend/app/docs/"
echo "2. Start the backend: cd backend && uvicorn app.main:app --reload"
echo "3. Open frontend/index.html in your browser"
echo ""
echo "For detailed instructions, see README.md"
echo ""

