"""
Django settings for testing.

Inherits from base settings and overrides specific settings to:
- Use in-memory Celery tasks (no Redis needed)
- Speed up password hashing
- Use SQLite for faster test database creation
"""

from .base import *  # noqa: F403, F401

# Use eager execution for Celery tasks in tests (no Redis needed)
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_BROKER_URL = 'memory://localhost/'
CELERY_RESULT_BACKEND = 'cache+memory://'

# Speed up password hashing in tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
    ]

# Disable debug toolbar and unnecessary middleware in tests
if 'debug_toolbar.middleware.DebugToolbarMiddleware' in MIDDLEWARE:  # noqa: F405
    MIDDLEWARE.remove('debug_toolbar.middleware.DebugToolbarMiddleware')  # noqa: F405
