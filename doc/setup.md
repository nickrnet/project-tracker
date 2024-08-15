# How to Start Developing ProjectTracker

This project is a Django app, which is a Python module. There is a `Pipfile` included that can be used with `pipenv` to set up a Python virtual environment to get up and running.

Django commands must be run from the `tracker` directory.

To start developing, use Python 3.12, and execute the following (managing a Python installation is beyond the scope of this document):

```shell
cd <path to checkout>
pipenv install
pipenv shell
cd tracker
python manage.py migrate  # to build a database
python manage.py setup    # to put standard Project Tracker configuration in the database
python manage.py runserver 0.0.0.0:8000  # to start the Django application(s)
```

Then, navigate to http://localhost:8000 and signup for an account in order to use the web app or API.

Useful app URLs:
- http://localhost:8000
- http://localhost:8000/new_git_repository
- http://localhost:8000/api

If additional Python modules are required, use pipenv to install them:

```shell
cd <path to checkout>
pipenv install <module>
```

This places the module in the Pipfile and Pipfile.lock to be included during a `pipenv install` command. These files should be committed to source control.
