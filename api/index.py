"""
Vercel serverless function handler for Django
"""
import os
import sys
from pathlib import Path

# Add parent directory to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kidney_stones_django.settings_production')

# Import Django WSGI application
from kidney_stones_django.wsgi import application

# Handler for Vercel
app = application
