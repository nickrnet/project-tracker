"""
Django settings for tracker project - Production environment.

This settings file is designed for production deployments with proper security,
OpenTelemetry instrumentation, and production-ready configurations.
"""

# Import all base settings first
from .base import *  # noqa: F403, F401

import environ
import os

from opentelemetry import trace
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
from opentelemetry.instrumentation.sqlite3 import SQLite3Instrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    )
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased

print("Loading production settings from environment (and .env if present)")
env = environ.Env()
# Read a local .env if present (useful for testing). In production the
# environment provided by the container/orchestration should be authoritative.
env.read_env(os.path.join(BASE_DIR, '.env'), overwrite=False)  # noqa: F405

# Override settings from base.py for production

# SECURITY WARNING: keep the secret key used in production secret!
# Prefer reading the key from a Docker secret file if provided. The
# docker-compose file sets `SECRET_KEY_FILE=/run/secrets/secret_key`.
secret_key_file = env('SECRET_KEY_FILE', default=None)
if secret_key_file and os.path.exists(secret_key_file):
    with open(secret_key_file, 'r') as f:
        SECRET_KEY = f.read().strip()
else:
    # Fall back to environ variable DJANGO_SECRET_KEY (not recommended).
    SECRET_KEY = env('DJANGO_SECRET_KEY', default=None)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
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


# Static file serving.
# `web` writes static files into the named volume mounted at `/app/staticfiles`.
# NGINX (or the proxy) will serve files from the same volume.
STATIC_URL = '/static/'
STATIC_ROOT = env('STATIC_ROOT', default='/app/staticfiles')

# Media files (user uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = env('MEDIA_ROOT', default='/app/media')

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

# Celery broker
CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='redis://redis:6379/0')


# Opentelemetry configuration

# Create resource with service information
resource = Resource(attributes={
    SERVICE_NAME: "project-tracker"
    })

# Create and configure the tracer provider
sampler = TraceIdRatioBased(0.1)
provider = TracerProvider(resource=resource, sampler=sampler)
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)

# Set the global default tracer provider
trace.set_tracer_provider(provider)

# Create a tracer from the global tracer provider
tracer = trace.get_tracer("project.tracker")

# Initialize OpenTelemetry instrumentation
DjangoInstrumentor().instrument()
Psycopg2Instrumentor().instrument()
SQLite3Instrumentor().instrument()
