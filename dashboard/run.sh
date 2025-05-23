#!/bin/bash

# Federal Funds Rate Dashboard Startup Script

echo "🚀 Starting Federal Funds Rate Dashboard..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check if FastAPI backend is running
echo "🔍 Checking FastAPI backend availability..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ FastAPI backend is running"
else
    echo "⚠️  Warning: FastAPI backend not detected at http://localhost:8000"
    echo "   Please ensure Docker containers are running:"
    echo "   cd .. && docker-compose up -d"
fi

# Start Flask dashboard
echo "🌐 Starting Flask dashboard on http://localhost:5001"
python app.py
