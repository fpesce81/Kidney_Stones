#!/bin/bash

# Exit on any error
set -e

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Set environment variables
export PYTHONUNBUFFERED=1
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build completed successfully!"
