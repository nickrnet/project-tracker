# Development Practices

We have a concept of not deleting information or updating it in-place.

The `core/models/user.py` classes demonstrate this by referencing `CoreModel` as the base class for all models, which contains a foreign key to a `Deleted` object.

To comply with not deleting data, each model should have a corresponding `Data` class with a `current` on the object, in order to prevent live updates or deletes. This means instead of performing `record.objects.update(**data)`, we create a new `Data`, and link it to the related record. See `frontend/views/core/user/user_view.py` where a POST is handled for an example. All `current` fields should be a "ForeignKey" so things are tracked properly.

See the [Project Structure](project_structure.md) documentation for filesystem layout.

## Python Modules

Install development Python packages required by this application by running

```shell
cd <path to checkout>
pipenv install --dev
```

*Postgres and psycopg2*

The `psycopg2` python module is included in the Pipfile. This requires the Postgres libraries to be on the PATH. If you do not have Postgres installed and in your PATH, and are doing local development, you can comment it out in the Pipfile if there are installation errors with the `pipenv install` command. Installing Postgres is platform-dependent.

Then, you can do

```shell
pipenv shell
```

to enter the virtual environment created with the `pipenv install` command that has access to a few more command-line goodies for development.

If additional Python modules are required for either development or production, use pipenv to install them:

```shell
pipenv install <module(s)>
```

or

```shell
pipenv install --dev <module(s)>
```

This places the module in the Pipfile and Pipfile.lock to be included during a `pipenv install` command. These files should be committed to source control. Do try to pay attention to modules required for production versus development, and use the `--dev` argument as needed, don't just install development modules for production's sake.

## Migrations

Until such time as someone is using this full-time for real data (production), we squash all migrations. This means breaking changes to existing databases if models are changed and squashed afterwards, so be wary.

## Testing

Tests are run via Github Actions with `pytest` at merge to the main branch, including code coverage, on Pull Request branches and every merge to the `main` branch. Test your code before merging to the `main` branch with

```shell
cd tracker
pytest --cov --cov-report term
```

The Django way is with

```shell
cd tracker
python manage.py test
```

or

```shell
cd tracker
python manage.py test core.tests.test_core.CoreModelTestCase.test_delete  # <substitute or change the Python path to the test to run to run more granularly>
```

Tests use their own database, there is no setup required. In theory, both the Django and pytest sets run the same tests, but do be careful as there are ways they can diverge.

We haven't had to prevent merges because of code coverage dropping yet, so try to keep unit tests up to date as much as possible.

## Running a Test Server

This application will require a database. It uses Django, so whatever Django supports and how it is configured is what should be used. Development and testing occurs with SQLite, plans are for Postgres in production. To create a database for using with the application for development or production, run

```shell
cd tracker
python manage.py migrate
```

There is a Django command to install demo data that has a pre-configured set of users, organizations, and projects. Run it with

```shell
cd tracker
python manage.py install_demo_data
```

to populate your database with demo data. *This probably should not be used in production environments as there are easy-to-guess passwords and what-not.*

Running a test instance of the web server to use the API and User Interface is as simple as

```shell
cd tracker
python manage.py runserver 0.0.0.0:8000
```

You can also get to a Django prompt with

```shell
cd tracker
python manage.py shell_plus
```

and work with the live demo data that way, just like the Django code, but live in a terminal session.

# Visual Studio Code

Development environment files for Visual Studio Code are included. The `launch.json` file contains a debug configuration for running the Django web server, Django tests with the `python manage.py test` command, and the 'Install Demo Data' command. The `settings.json` file contains the configuration to use the Visual Studio Code Test Explorer feature to allow to run tests within the IDE and show test coverage using the `pytest` and `django-pytest` modules.

When committing changes to these files, be sure to callout changes in Pull Requests so they can be reviewed and properly tested by other developers, potentially on other platforms (Windows, Linux, etc.) for compatibility (though for now most developers are on Macs).

## TODO

Provide an environment file containing variables for cloud storage, database connection, etc. Document as we get there.

Postgres DB config for testing and production.

A guide (.md file) for development with Postgres instead of SQLite.

Figure out how to consolidate the `.coveragerc` files. The one in `tracker` is the one the GitHub action uses, so it is the source of truth for now, but the one at the top level of the directory is for VSCode's TestExplorer. It is a copy and should just be stomped over as the main one in `tracker` changes. Maybe the GH Action can be modified with a `--cov-config` argument to point at it, will take testing and commits.

