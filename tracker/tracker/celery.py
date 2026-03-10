import os
from celery import Celery
from celery.schedules import crontab
# from celery import signals
from celery.signals import setup_logging  # noqa
import logging

from django.conf import settings  # noqa

# import core.handlers.tasks.process_invite_expiration  # noqa


django_logger = logging.getLogger("django")
celery_logger = logging.getLogger("celery")

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tracker.settings.base')

django_logger.info("Initializing Celery...")
app = Celery('project-tracker')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# Attach beat schedule directly to the Celery app configuration so the
# worker/beat process will pick it up. Alternatively, you could place
# `CELERY_BEAT_SCHEDULE` in your Django settings (e.g. `local.py`).
app.conf.beat_schedule = {
    'process-organization-invite-expiration': {
        'task': 'core.tasks.process_invite_expiration.process_organization_invite_expiration',
        'schedule': crontab(minute=1, hour=9),
        },
    }
