# Project Structure

There are 4 Django applications in the Django project:

- `core`

  Contains core models (perhaps some day these can be their own Django apps, but for now, we choose dev speed over deployment logic)

- `project`

  Contains work related to Project models

- `api`

  Contains the Django REST API integration to all models

- `frontend`

  Contains the Django forms, templates, and views, as viewed in a browser

- `tracker`

  Contains the Django project configuration

Try to keep management commands in the main application they work with. See the `core/management/commands/initialize_api_user.py` and `project/management/commands/initialize_built_in_issue_priorities.py` commands for an example. In some cases where commands cross application boundaries, the command should reside in the `core` application, such as `core/management/commands/setup.py`. Use management command modules when possible for reusability, see `core/management/commands/modules` and `project/management/commands/modules` for examples.

Try to keep tests in the main application they are testing. `api` tests in api, `core` in core, etc.

Be very careful placing things in the `tracker/settings.py` file, avoid things like secrets and credentials specifically.
