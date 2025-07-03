#!/bin/bash

# Build script for Vercel deployment
echo "Starting build process..."

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p staticfiles
mkdir -p media

# Collect static files
python manage.py collectstatic --noinput --clear

# Run migrations (for SQLite in /tmp)
python manage.py migrate --noinput

# Load initial data if needed
if [ -f "oxalate_en.json" ]; then
    echo "Loading oxalate data..."
    python manage.py load_oxalate_data || echo "Failed to load oxalate data"
fi

echo "Build process completed!"
