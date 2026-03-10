"""
Django settings for project-tracker - Docker development environment.

This settings file is designed for use in docker-compose development. It provides
a development-like environment but with proper Redis broker for Celery and other
containerized services.
"""

# Import all base settings first
from .base import *  # noqa: F403, F401

import environ
import os

env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'), overwrite=True)  # noqa: F405

print("Loading docker settings - using Redis broker for Celery")

# Override settings for docker environment
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-7awm!p=&@h44!ur2r-mo1j&8u!k&k!bfd8++%=37zlm@u-$_&7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=True)
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ["*"]

# Database - allow override via DATABASE_URL
DATABASE_URL = env('DATABASE_URL', default=None)
if DATABASE_URL:
    print(f"Using DATABASE_URL: {DATABASE_URL}")
    DATABASES = {
        'default': env.db('DATABASE_URL'),
        }
else:
    print("No DATABASE_URL found, using SQLite")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',  # noqa: F405
            'TEST': {
                'NAME': 'test_db.sqlite3',
                },
            }
        }

# Celery configuration for Docker environment with Redis
# Explicitly set broker and result backend for containerized environment
CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TASK_ALWAYS_EAGER = False
CELERY_TASK_EAGER_PROPAGATES = False

# Additional Celery settings to ensure proper Redis connection
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
