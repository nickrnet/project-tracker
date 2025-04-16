# How to Start Developing ProjectTracker

This project is a Django app, which is a Python module. There is a `Pipfile` included that can be used with `pipenv` to set up a Python virtual environment to get up and running.

Django commands must be run from the `tracker` directory.

To run the application, use Python 3.12, and execute the following commands (managing a Python installation is beyond the scope of this document):

```shell
cd <path to checkout>
pipenv install
pipenv shell
cd tracker
python manage.py migrate                 # to build a database
python manage.py setup                   # to put standard Project Tracker configuration in the database
python manage.py install_demo_data       # to put Project Tracker demo data in the database; also includes the setup command, so one or the other
python manage.py runserver 0.0.0.0:8000  # to start the Django application(s)
```

Then, navigate to http://localhost:8000 and signup for an account in order to use the web app or API, or use a user as defined in `core/management/commands/modules/test_user_data*.py` to get preconfigured demo project(s) and organization(s).

Useful app URLs:
- http://localhost:8000
- http://localhost:8000/api

See the [Development Documentation](doc/development.md) for more development tips and tricks and standards.
