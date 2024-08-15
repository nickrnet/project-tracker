# Project Structure

There are 3 Django applications in the Django project:

- `core`

  Contains core models (perhaps some day these can be their own Django apps, but for now, speed)

- `project`

  Contains work related to Project models

- `api`

  Contains the Django REST API integration to all models

- `frontend`

  Contains the Django forms, templates, and views, as viewed in a browser

- `tracker`

  Contains the overarching Django application configuration

Try to keep management commands in the main application they work with. See the `core/management/commands/initialize_api_user.py` and `project/management/commands/initialize_built_in_issue_priorities.py` commands for an example. In some cases where commands cross application boundaries, the command should reside in the `core` application, such as `core/management/commands/setup.py`.
