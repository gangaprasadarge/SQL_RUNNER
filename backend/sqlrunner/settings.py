from pathlib import Path
from datetime import timedelta
import os
import dj_database_url 


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-4#)(g)hs5^mtgfk%9a6!2_wp+5q%nwis&l@&5qmjbklqomm0@g" 
)


DEBUG = False 

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


CSRF_TRUSTED_ORIGINS = [
    "https://sql-runner-backend-tr4a.onrender.com",
    "https://sql-runner-23g4.onrender.com",
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
    "corsheaders.middleware.CorsMiddleware", 
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True 

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
FRONTEND_URL = os.environ.get("FRONTEND_URL")  
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")


DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        conn_health_checks=True
    )
}



DATABASES["default"]["URL"] = os.environ.get("DATABASE_URL")

DATABASE_URL = os.environ.get("DATABASE_URL")

DATABASES = {
    "default": dj_database_url.parse(DATABASE_URL)
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
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles") 

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# # Email settings (ensure these are set securely via environment variables in production)
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
# EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
# EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True").lower() in ("true", "1", "yes")
# EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "") # Set this in Render env vars for production
# EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "") # Set this in Render env vars for production


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = "argegangaprasad9515@gmail.com"
EMAIL_HOST_PASSWORD = "niaj igkl pqgj ozuf"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER



LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"), 
            "propagate": False,
        },
        "corsheaders": {
            "handlers": ["console"],
            "level": "DEBUG", 
            "propagate": False,
        }
    }
}
