#!/bin/bash
# Quick local development server using SQLite (much faster than Docker)

cd "$(dirname "$0")"

echo "=== Quick Local Server Setup ==="
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
echo "Checking dependencies..."
if ! python -c "import django" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt --quiet
fi

# Set environment variables
export USE_SQLITE=True
export DEBUG=True

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Create superuser if doesn't exist (optional)
if ! python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists()" 2>/dev/null | grep -q True; then
    echo ""
    echo "To create a superuser, run:"
    echo "  source venv/bin/activate"
    echo "  export USE_SQLITE=True"
    echo "  python manage.py createsuperuser"
    echo ""
fi

# Start server
echo ""
echo "=== Starting Django server ==="
echo "Server will be available at: http://127.0.0.1:8000"
echo "Press Ctrl+C to stop"
echo ""
python manage.py runserver 127.0.0.1:8000

