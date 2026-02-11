#!/bin/bash

echo "========================================="
echo "   SGA-Lite - Quick Start Setup"
echo "========================================="
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.10 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt --quiet

# Setup .env if not exists
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')" >> .env
else
    echo "✓ .env file already exists"
fi

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Seed database
echo "🌱 Seeding database with initial data..."
python manage.py seed_data

echo ""
echo "========================================="
echo "   ✅ Setup Complete!"
echo "========================================="
echo ""
echo "To start the server, run:"
echo "  python manage.py runserver"
echo ""
echo "Then visit: http://localhost:8000"
echo ""
echo "Default credentials:"
echo "  Admin:    admin / admin123"
echo "  Employee: employee1 / password123"
echo ""
