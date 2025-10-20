"""
Django settings for plananything project.
"""

from pathlib import Path
import os
import sys
from dotenv import load_dotenv
import dj_database_url  # ✅ for Render PostgreSQL integration

# Load environment variables early
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------
# 🔐 SECURITY SETTINGS
# ------------------------------------------------
SECRET_KEY = os.environ.get('SESSION_SECRET', 'django-insecure-development-key-only')

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# ✅ Add your Render domain + localhost
ALLOWED_HOSTS = [
    'plananything.onrender.com',
    'localhost',
    '127.0.0.1',
]

# ✅ CSRF trusted origins (required for login & POST requests)
CSRF_TRUSTED_ORIGINS = [
    'https://plananything.onrender.com',
]

# ------------------------------------------------
# 🧩 APPLICATIONS
# ------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'planner',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'plananything.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'plananything.wsgi.application'

# ------------------------------------------------
# 🗄️ DATABASE
# ------------------------------------------------
# ✅ Use SQLite locally, PostgreSQL on Render
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}

# ------------------------------------------------
# 🔐 PASSWORD VALIDATION
# ------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ------------------------------------------------
# 🌍 INTERNATIONALIZATION
# ------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ------------------------------------------------
# 🗂️ STATIC & MEDIA FILES
# ------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ------------------------------------------------
# 🔑 AUTH REDIRECTS
# ------------------------------------------------
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

# ------------------------------------------------
# ✅ PRODUCTION CHECKS
# ------------------------------------------------
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
