# How to Start Developing ProjectTracker

This project is a Django app, which is a Python module. This project uses `uv` to manage the Python modules and Python version required.

## Install UV

See the instructions for the [uv package manager](https://docs.astral.sh/uv/getting-started/installation/).

If on a Mac, you may want to set `SYSTEM_VERSION_COMPAT=0` in your shell when installing a virtual environment.

## Create a `.env` file

Create a `.env` file in the `tracker` directory from the `env.sample` file. If running locally, the `DATABASE_URL` value can be empty.

## Running Django

Django commands must be run from the `tracker` directory.

To run the application, use Python 3.12, and execute the following commands (managing a Python installation is beyond the scope of this document):

```shell
cd <path to checkout>
uv venv
source .venv/bin/activate
uv sync --dev
cd tracker
python manage.py migrate                 # to upgrade an existing database, OR
python manage.py setup                   # to put standard Project Tracker configuration in a new database, OR
python manage.py install_demo_data       # to put Project Tracker demo data in a new database; also includes the setup command, so one or the other, then
python manage.py runserver 0.0.0.0:8000  # to start the Django application(s)
```

Then, navigate to http://localhost:8000 and signup for an account in order to use the web app or API, or use a user as defined in `core/management/commands/modules/test_user_data*.py` to get preconfigured demo project(s) and organization(s).

Useful app URLs:
- http://localhost:8000
- http://localhost:8000/api

See the [Development Documentation](doc/development.md) for more development tips and tricks and standards.
