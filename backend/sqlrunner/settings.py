from pathlib import Path
from datetime import timedelta
import os
import dj_database_url # Import the dj_database_url library

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Get DJANGO_SECRET_KEY from environment variables for production
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-4#)(g)hs5^mtgfk%9a6!2_wp+5q%nwis&l@&5qmjbklqomm0@g" # Fallback for local development, USE A STRONG KEY IN PROD ENV
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False # Keep this False for production

FRONTEND_URL = "https://sql-runner-23g4.onrender.com"
LOCAL_FRONTEND = "http://localhost:3000"

ALLOWED_HOSTS = [
    "sql-runner-backend-tr4a.onrender.com",
    "sql-runner-23g4.onrender.com",
    "localhost",
    "127.0.0.1"
]

CORS_ALLOWED_ORIGINS = [
    FRONTEND_URL,
    LOCAL_FRONTEND
]

CORS_ALLOW_CREDENTIALS = True

# CSRF_TRUSTED_ORIGINS should include your frontend URL and potentially other domains if you're sending forms from them.
# Using a wildcard for subdomains of onrender.com is common for Render deployments.
CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com"
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'api',
    # Add any other apps your project uses here
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    )
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware", # Keep this at the very top
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Ensure Django correctly identifies the connection as secure when behind a proxy like Render
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True # IMPORTANT: Ensures all HTTP traffic is redirected to HTTPS

ROOT_URLCONF = 'sqlrunner.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'sqlrunner.wsgi.application'

# Database configuration: Use PostgreSQL in production (via DATABASE_URL env var)
# and SQLite for local development if DATABASE_URL is not set.
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR / 'db.sqlite3'}"), # Fallback to sqlite, using Path for robustness
        conn_max_age=600, # Optional: controls how long database connections are kept open
        conn_health_checks=True, # Optional: checks connection health before reuse
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles") # Directory where 'collectstatic' will gather static files

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email settings (ensure these are set securely via environment variables in production)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True").lower() in ("true", "1", "yes")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "") # Set this in Render env vars for production
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "") # Set this in Render env vars for production

# Logging configuration for better debugging in production
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"}, # Set root logging level to INFO
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"), # Allows overriding Django's log level via env var
            "propagate": False,
        },
        "corsheaders": {
            "handlers": ["console"],
            "level": "DEBUG", # Often useful to debug CORS issues specifically
            "propagate": False,
        }
    }
}
