"""
Django settings for AI-Based Social Media Sentiment and Reputation Analysis System.
"""

from pathlib import Path
import os
import sys
from dotenv import load_dotenv
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Add apps directory to Python path
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / 'apps'))

# Load environment variables from .env if present
load_dotenv(BASE_DIR / '.env')

# Security settings
SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'django-insecure-ai-sentiment-reputation-analyser-academic-project-key-2026'
)

DEBUG = os.getenv('DEBUG', 'True').strip().lower() in ('true', '1', 'yes')

raw_hosts = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,0.0.0.0,.railway.app').split(',')
ALLOWED_HOSTS = []
for host in raw_hosts:
    h = host.strip()
    if not h:
        continue
    # Django syntax for subdomain wildcards requires a leading dot (.railway.app), not an asterisk
    if h.startswith('*.'):
        h = h[1:]
    ALLOWED_HOSTS.append(h)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'corsheaders',
    'rest_framework',

    # Local apps
    'apps.sentiment.apps.SentimentConfig',
    'apps.social_media.apps.SocialMediaConfig',
    'apps.analytics.apps.AnalyticsConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# Database configuration: defaults to SQLite for local dev, PostgreSQL ready for production
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise for production static-file serving and compression
try:
    import whitenoise  # noqa: F401
    MIDDLEWARE.insert(
        MIDDLEWARE.index('django.middleware.security.SecurityMiddleware') + 1,
        'whitenoise.middleware.WhiteNoiseMiddleware',
    )
    STORAGES = {
        'default': {
            'BACKEND': 'django.core.files.storage.FileSystemStorage',
        },
        'staticfiles': {
            'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
        },
    }
except ImportError:
    pass

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
}

# CORS configuration
CORS_ALLOW_ALL_ORIGINS = os.getenv('CORS_ALLOW_ALL', 'True').strip().lower() in ('true', '1')
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        'CORS_ALLOWED_ORIGINS',
        'http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173'
    ).split(',')
    if origin.strip()
]

# CSRF Trusted Origins for cross-origin deployment (e.g. Vercel frontend calling Railway backend)
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        'CSRF_TRUSTED_ORIGINS',
        'http://localhost:5173,http://127.0.0.1:5173,https://*.vercel.app,https://*.railway.app'
    ).split(',')
    if origin.strip()
]

# ML Model Paths
MODEL_DIRECTORY = Path(os.getenv('MODEL_DIRECTORY', BASE_DIR / 'ml_models'))
TWITTER_MODEL_DIR = MODEL_DIRECTORY / 'twitter'
INSTAGRAM_MODEL_DIR = MODEL_DIRECTORY / 'instagram'

# Social Media Integration Credentials
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY', '')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET', '')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN', '')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET', '')
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN', '')

META_ACCESS_TOKEN = os.getenv('META_ACCESS_TOKEN', '')
INSTAGRAM_BUSINESS_ACCOUNT_ID = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID', '')
INSTAGRAM_APP_ID = os.getenv('INSTAGRAM_APP_ID', '')
INSTAGRAM_APP_SECRET = os.getenv('INSTAGRAM_APP_SECRET', '')
