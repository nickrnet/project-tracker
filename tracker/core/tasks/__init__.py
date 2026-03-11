"""Task package for the `core` app.

Celery's `autodiscover_tasks()` imports `<app>.tasks` for each app in
`INSTALLED_APPS`. This package makes sure submodules (like
`process_invite_expiration`) are imported when `core.tasks` is imported.
"""

from .process_invite_expiration import process_organization_invite_expiration  # noqa: F401
