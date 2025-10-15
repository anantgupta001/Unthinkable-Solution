#!/bin/bash

# Quick start script for Knowledge Base Search Engine

set -e

echo "🚀 Starting Knowledge Base Search Engine..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Start backend
echo "🔧 Starting backend server..."
echo "📍 API will be available at: http://127.0.0.1:8000"
echo "📖 API docs: http://127.0.0.1:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd backend
uvicorn app.main:app --reload

