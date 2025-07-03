"""
Production settings for Vercel deployment
"""
from .settings import *
import os

# Security settings for production
DEBUG = False
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-your-secret-key-here-change-in-production')

# Add Vercel domains to allowed hosts
ALLOWED_HOSTS = [
    '.vercel.app',
    '.now.sh',
    'localhost',
    '127.0.0.1',
    '*',  # Be careful with this in production
]

# Add your custom domain if you have one
CUSTOM_DOMAIN = os.environ.get('CUSTOM_DOMAIN')
if CUSTOM_DOMAIN:
    ALLOWED_HOSTS.append(CUSTOM_DOMAIN)

# Database configuration for Vercel
# Using SQLite for simplicity, but you should use PostgreSQL for production
import dj_database_url

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.parse(DATABASE_URL)
else:
    # Use a temporary SQLite database for Vercel
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '/tmp/db.sqlite3',
        }
    }

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Disable collectstatic on Vercel
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# CORS settings if needed
CORS_ALLOWED_ORIGINS = [
    "https://*.vercel.app",
    "https://*.now.sh",
]

if CUSTOM_DOMAIN:
    CORS_ALLOWED_ORIGINS.append(f"https://{CUSTOM_DOMAIN}")

# Add CORS middleware
MIDDLEWARE.insert(2, 'corsheaders.middleware.CorsMiddleware')

# Also add CORS to installed apps
if 'corsheaders' not in INSTALLED_APPS:
    INSTALLED_APPS.append('corsheaders')

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
