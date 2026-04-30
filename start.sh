#!/bin/bash
# Production startup script for Interview Tracker

echo "🚀 Starting Interview Tracker Production Server..."
echo "=========================================="

# Set environment variables
export FLASK_ENV=production
export FLASK_APP=app.py

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Initialize database (creates auth table if not exists)
echo "🗄️ Initializing database..."
python -c "from auth_db import auth_db; print('Database initialized')"

# Start with Gunicorn
echo "🌐 Starting server with Gunicorn..."
gunicorn -c gunicorn.conf.py app:app

echo "✅ Server started on http://0.0.0.0:2699"
