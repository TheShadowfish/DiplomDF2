"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

import os
from datetime import timedelta
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

# SECRET_KEY = os.getenv("SECRET_KEY")
SECRET_KEY = "django-insecure-3n!sjx3h4tbnt68^!-@ak9rw$-_=p)zd)hr_)t=*$94p*%8a2t"

# SECURITY WARNING: don't run with debug turned on in production!

# DEBUG = os.getenv('DEBUG') == 'True'
DEBUG = True

# change when hosting!
ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "phonenumber_field",
    "corsheaders",
    "users",

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]
# Чтобы кешировать весь сайт
# MIDDLEWARE = [
#     'django.middleware.cache.UpdateCacheMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.cache.FetchFromCacheMiddleware',
# ]
# не забыть в .env CACHE_ENABLED=False установить после этого

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "PectopaH",
        "USER": "postgres",
        "HOST": "localhost",
        "PORT": 5432,
        "PASSWORD": 12345,
        # "NAME": os.getenv("DB_POSTRESQL_NAME"),
        # "USER": os.getenv("DB_POSTRESQL_USER"),
        # "HOST": os.getenv("DB_POSTRESQL_HOST"),
        # "PORT": os.getenv("DB_POSTRESQL_PORT"),
        # "PASSWORD": os.getenv("DB_POSTRESQL_PASSWORD"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "static"

# ENV_TYPE = os.getenv("ENV_TYPE")

# if ENV_TYPE == "local":
#     STATICFILES_DIRS = (
#         BASE_DIR / "static"
#     )
# else:
#     STATIC_ROOT = BASE_DIR / "static"


MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

REDIRECT_FIELD_NAME = "users/login.html"



CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",  # Замените на адрес вашего фронтенд-сервера
]

CSRF_TRUSTED_ORIGINS = [
    "https://read-and-write.example.com",
    # Замените на адрес вашего фронтенд-сервера
    # и добавьте адрес бэкенд-сервера
]

CORS_ALLOW_ALL_ORIGINS = False
#
# # Celery Configuration Options
# CELERY_TIMEZONE = TIME_ZONE
# CELERY_TASK_TRACK_STARTED = True
# CELERY_TASK_TIME_LIMIT = 30 * 60
# CELERY_ENABLE_UTC = False
#
# # set the celery broker url
# CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
#
# # set the celery result backend
# CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
#
# CELERY_BEAT_SCHEDULE = {
#     "habits.tasks.find_all_habits": {
#         "task": "habits.tasks.find_all_habits",
#         "schedule": timedelta(minutes=1),  # Run every day at 00:00
#     }
# }
# # CELERY_BEAT_SCHEDULE = "django_celery_beat.schedulers:DatabaseScheduler"

# TELEGRAM_URL = "https://api.telegram.org/bot"
# TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


# CACHE_ENABLED = os.getenv('CACHE_ENABLED') == 'True'

CACHE_ENABLED = True

if CACHE_ENABLED:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            # "LOCATION": os.getenv('LOCATION'),
            "LOCATION": "redis://127.0.0.1:6379",
            "TIMEOUT": 1200  # Ручная регулировка времени жизни кеша в секундах, по умолчанию 300
        }
    }