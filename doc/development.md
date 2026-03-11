# Development

This document explains both Docker and local (non-Docker) development workflows.

## Quick Setup Guide

### Docker Development (Recommended)

The default `.env` file is configured for Docker development with PostgreSQL.

**Prerequisites:**
- Docker and Docker Compose installed on your machine
- The `.env` file in the repository root (already configured for Docker)

**Database Setup:**
- Docker automatically uses PostgreSQL (configured in `.env`)
- The `tracker` database is automatically created on **every startup** if it doesn't exist
  - A startup script (`ensure-db.sh`) checks and creates the database before migrations run
  - This means you can drop the database and restart to get a fresh database
- Django, Celery worker, and Celery beat all connect to the same PostgreSQL database
- Data persists in a Docker volume named `postgres_data`
- Health checks ensure PostgreSQL is ready before Django and Celery start

**Quick start:**

```bash
# Start everything (build images first time)
docker-compose up --build

# Subsequent starts (faster)
docker-compose up
```

### Local Development (Without Docker)

For local development without containers, you'll use SQLite and eager Celery tasks.

**Setup:**

```bash
# 1. Copy the local example file
cp .env.local.example .env

# 2. Create a virtual environment and install dependencies
uv venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
uv sync --dev

# 3. Run migrations
cd tracker
python manage.py migrate

# 4. Create a superuser (optional)
python manage.py createsuperuser

# 5. Start the dev server
python manage.py runserver
```

**Note:** In local mode without Docker:
- Uses SQLite database (`db.sqlite3`)
- Celery runs in eager mode (tasks execute synchronously, no Redis needed)
- No separate Celery worker or beat processes required

Quick start

Start everything (build images first):

```bash
docker-compose up --build
```

Start all containers without rebuilding (faster):

```bash
docker-compose up
```

Run a single service (e.g. django):

```bash
docker-compose up django
```

Stopping and cleaning

Stop services gracefully:

```bash
docker-compose down
```

Remove volumes and images (use when you need a clean state):

```bash
docker-compose down --volumes --rmi all
docker system prune --volumes
```

Useful one-off commands

Run Django management commands inside the running `django` container:

```bash
docker-compose exec django python manage.py migrate
```

or

```bash
docker-compose exec django python manage.py shell
```

or

```bash
docker-compose exec django python manage.py setup
```

or

```bash
docker-compose exec django python manage.py install_demo_data
```

Run a one-off worker (local debugging):

```bash
docker-compose run --rm worker celery -A tracker.celery worker -l info --autoreload
```

View logs for all services (follow):

```bash
docker-compose logs -f
```

or

```bash
docker-compose logs -f worker
```

Inspect scheduled tasks

If you need to confirm Beat has registered schedules, check Beat logs or use `flower`.
You can also list scheduled tasks from a worker using Celery's inspect API:

```bash
docker-compose exec worker celery -A tracker.celery inspect scheduled
```

Configuration notes
- The `.env` file controls `CELERY_BROKER_URL` and `CELERY_TASK_ALWAYS_EAGER`.
- `docker-compose.yml` uses the `Dockerfile` at the repo root to build images.
- **Container naming**: The `COMPOSE_PROJECT_NAME` environment variable (set in `.env`) determines container names:
  - Development: `COMPOSE_PROJECT_NAME=tracker-dev` → containers named `tracker-dev-django-1`, etc.
  - Production: `COMPOSE_PROJECT_NAME=tracker-prod` → containers named `tracker-prod-django-1`, etc.
  - This allows running dev and prod containers simultaneously on the same machine if needed
  - You can also override per-command: `COMPOSE_PROJECT_NAME=tracker-test docker-compose up`

Troubleshooting

### Celery Issues

- If tasks are scheduled but not executed, ensure `CELERY_TASK_ALWAYS_EAGER=False`
  and that the worker is connected to the broker specified by `CELERY_BROKER_URL`.

### Build Issues

- If containers fail to start due to missing dependencies, run:

```bash
docker-compose build --no-cache django
```

### General Issues

- If you see port conflicts (e.g. port 8000 already used), stop the conflicting
  service or change `ports` in `docker-compose.yml`.
- If Redis is unreachable, check the `redis` service logs and the broker URL in
  `.env`.
- To reduce log noise, start worker with `-l warning` or set `CELERY_LOG_LEVEL`
  in `.env`.

Performance / dev ergonomics
- The `Dockerfile` is structured to cache Python dependency installation using
  `pyproject.toml`. After the first build, rebuilds will be faster.
- The compose setup mounts your working tree into `/app` so edits are visible
  immediately in the django web container.

Further reading
- For production deployments, separate build and runtime images (multi-stage
  Dockerfile) and prefer a process manager / orchestration system.

## Database Configuration

### Docker (PostgreSQL)
The default `.env` file is already configured for PostgreSQL when using Docker:
- `DATABASE_URL=postgres://tracker:tracker@postgres:5432/tracker`
- **Automatic database creation**:
  - On **every startup**, a script (`ensure-db.sh`) checks if the `tracker` database exists
  - If missing, it automatically creates the database before running migrations
  - This means you can drop the database and restart to get a fresh database
  - The PostgreSQL init script also creates the `tracker` user on first container initialization
- All services (Django, Celery worker, Celery beat) connect to the same PostgreSQL database
- Data persists in a Docker volume (`postgres_data`)
- Health checks ensure PostgreSQL is ready before starting Django migrations

**Resetting the database:**
```bash
# Drop just the database (will be recreated on next startup)
docker-compose exec postgres psql -U tracker -d postgres -c "DROP DATABASE tracker;"
docker-compose restart django

# Or completely fresh start (removes all data)
docker-compose down -v && docker-compose up
```

### Local Development (SQLite)
For local development without Docker, comment out the `DATABASE_URL` line in `.env`:
```bash
# DATABASE_URL=postgres://tracker:tracker@postgres:5432/tracker
```
This will automatically use SQLite at `tracker/db.sqlite3`.

### Switching Between Modes
The key is the `DATABASE_URL` environment variable:
- **Uncommented/Set**: Uses PostgreSQL (for Docker)
- **Commented out/Not set**: Uses SQLite (for local development)

## Docker Commands

Start the stack as usual:

```bash
docker-compose up --build
```

Notes and tips
- The Postgres container listens on port `5432`. The compose file maps it to
  the host by default (`5432:5432`); remove that mapping if you don't want host
  access and want the DB to be reachable only from other compose services.
- The `postgres` service reads credentials from `.env` (with sensible defaults),
  so editing `.env` is the recommended way to change them.
- If switching from SQLite to Postgres you may need to recreate containers and
  the database volume to avoid conflicts:

```bash
docker-compose down --volumes
docker-compose up --build
```

- Run migrations after the DB is up:

```bash
docker-compose exec django python manage.py migrate
```

- If you need to inspect the DB locally, keep the host port mapping (`5432:5432`)
  and use a client like `psql` or a GUI (PgAdmin, TablePlus, DBeaver).

# DATABASE_URL assembly behavior

The compose file will export a `DATABASE_URL` environment variable into the
`django`, `celery-worker`, and `celery-beat` services. The value is selected as
follows:

- If you set `DATABASE_URL` in your `.env`, that value is used unchanged.
- If `DATABASE_URL` is not set, Compose will assemble one from the
  `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB` variables and point
  it at the `postgres` host. Example final URL:

```text
postgres://tracker:tracker@postgres:5432/tracker
```

Recommendation: copy `.env.sample` to `.env` and explicitly set `DATABASE_URL`
to `sqlite:///db.sqlite3` (the default) if you don't intend to enable the
`postgres` profile. If you enable the `postgres` profile, set the `POSTGRES_*`
variables or `DATABASE_URL` in `.env` before starting the stack.
- If you prefer to start Postgres separately you can also run just that
  service:

```bash
docker-compose up -d --profile postgres postgres
```

# Manual Postgres database creation (no GUI)

If you prefer to create the database and user manually (for example when
switching from SQLite or when you want explicit control), use the Postgres
container's `psql` tool. The examples assume the compose service is named
`postgres` and `.env` contains the recommended `POSTGRES_*` values.

1) Start the postgres service (no need to start the whole stack):

```bash
docker-compose up -d postgres
```

2) Create the user and database (run as the default `postgres` superuser):

```bash
# create user (if not already created by the image env)
docker-compose exec postgres psql -U postgres -c "CREATE USER tracker WITH PASSWORD 'tracker';"

# create database and set owner
docker-compose exec postgres psql -U postgres -c "CREATE DATABASE tracker OWNER tracker;"
```

If your `POSTGRES_USER`/`POSTGRES_PASSWORD` are different, replace `tracker`
and the password above with the values in your `.env` or use the `postgres`
superuser to run the commands and adjust names accordingly.

3) Verify the database exists and list tables (connect as the app user):

```bash
docker-compose exec postgres psql -U tracker -d tracker -c "\l"
docker-compose exec postgres psql -U tracker -d tracker -c "\dt"
```

4) Run Django migrations against the new DB:

```bash
docker-compose exec django python manage.py migrate
```

5) Optional: connect from host using `psql` if you've mapped the port
   (`5432:5432`):

```bash
# on host (requires psql client installed)
psql "postgresql://tracker:tracker@localhost:5432/tracker"
```

Notes
- To reset the DB and start fresh you can remove volumes:

```bash
docker-compose down --volumes
docker-compose up -d postgres
```

# Deleting the Postgres Database

```bash
docker-compose exec postgres bash
sudo postgres
dropdb --username=tracker --password --if-exists "tracker"
```

# Development Practices

## Local development without Docker

If you prefer to develop without Docker, use the project's `uv` tool to
manage the virtual environment and dependencies. The steps below mirror the
guidance in `doc/setup.md` and keep local commands consistent with the
project's workflow.

1) Create and activate a virtual environment

```bash
uv venv
source .venv/bin/activate
```

2) Install dependencies

Install development dependencies from the project's configuration:

```bash
uv sync --dev
```

3) Prepare environment variables

Copy `.env.sample` to `.env` and edit values as needed. By default the
project uses SQLite for development (`DATABASE_URL=sqlite:///db.sqlite3`). If
you want to use Postgres locally, set `DATABASE_URL` to the Postgres
connection string or set `POSTGRES_*` values and the appropriate URL.

```bash
cp .env.sample .env
# edit .env
```

Make sure to determine if Postgres is being used or not.

4) (Optional) Install and start Redis locally

If you use Redis as the Celery broker, install it and start the service. On
macOS with Homebrew:

```bash
brew install redis
brew services start redis
# or run in foreground for a session: redis-server
```

5) Run database migrations and load demo data

```bash
uv run manage.py migrate
uv run manage.py install_demo_data  # optional
```

6) Start the Django dev server

```bash
uv run manage.py runserver 0.0.0.0:8000
```

7) Start Celery worker and beat (separate terminals)

Ensure `CELERY_BROKER_URL` in `.env` points to your running broker and that
`CELERY_TASK_ALWAYS_EAGER=False` when you expect a worker process to execute
tasks. Example commands:

```bash
uv run celery -A tracker.celery worker -l info --without-gossip --without-mingle
uv run celery -A tracker.celery beat -l info

# or a single-process dev run (not recommended for production):
uv run celery -A tracker.celery worker -B -l info --autoreload
```

8) Run tests

Run Django tests or `pytest` from the project root. Tests run against their
own test database and generally don't require running the dev DB service:

```bash
uv run manage.py test
# or
uv run pytest
```

Troubleshooting (local)
- If Celery tasks are not being executed, confirm `CELERY_BROKER_URL` points
  to a running broker (Redis/RabbitMQ) and `CELERY_TASK_ALWAYS_EAGER` is
  disabled.
- If `psycopg2` installation fails, install the platform Postgres client
  libraries first (macOS: `brew install postgresql`) or consider
  `psycopg2-binary` for development only.
- The in-memory broker (`memory://`) only works in-process, so don't use it
  when running separate worker/beat processes.
- If ports conflict, stop the conflicting service or change the port used by
  `runserver`/Redis/Postgres.

## Deleting Data

We have a concept of not deleting information nor updating it in-place. Whenever an update is made to a record (an issue's severity, for instance), we create a new "\<model>Data" object, or a new IssueData row in the table in this issue severity case, then link the Issue's current to the new id.

The `core/models/user.py` classes demonstrate this by referencing `CoreModel` as the base class for all models, which contains a foreign key to a `Deleted` object.

To comply with not deleting data, each model should have a corresponding `Data` class with a `current` on the object, in order to prevent live updates or deletes. This means instead of performing `record.objects.update(**data)`, we create a new `Data`, and link it to the related record. See `frontend/views/core/user/user_view.py` where a POST is handled for an example. All `current` fields should be a "ForeignKey" so things are tracked properly.

See the [Project Structure](project_structure.md) documentation for filesystem layout.

## Python Modules

Install development Python packages required by this application by running

```shell
cd <path to checkout>
uv sync --dev
```

### Postgres and psycopg2

The `psycopg2` python module is included in the Pipfile. This requires the Postgres libraries to be on the PATH. If you do not have Postgres installed and in your PATH, and are doing local development, you can comment it out in the `pyproject.toml` if there are installation errors with the `uv sync` command. Installing Postgres is platform-dependent.

Then, you can do

```shell
source .venv/bin/activate
```

to enter the virtual environment created with uv that has access to a few more command-line goodies for development.

If additional Python modules are required for either development or production, use pipenv to install them:

```shell
uv add <module(s)>
```

or

```shell
uv add --dev <module(s)>
```

This places the module in the `pyproject.toml` to be included during a `uv sync` command. This file along with the `uv.lock` file should be committed to source control. Do try to pay attention to modules required for production versus development, and use the `--dev` argument as needed, don't just install development modules for production's sake.

## Migrations

Until such time as someone is using this full-time for real data (production), we squash all migrations. This means breaking changes to existing databases if models are changed and squashed afterwards, so be wary.

## Django Settings

In the `tracker/tracker` settings directory, there is a set of settings files: a `base.py` for common settings, a `local.py` file for local or development settings, and a `production.py` file for settings that should be turned on for production. `base.py` contains the majority of the Djanog app config, including middleware, and Project Tracker app definitions. `local.py` contains settings common for local development. `production.py` contains configuration for opentelemetry among other settings, that we don't necessarily want turned on for local development. Whether local or production is loaded depends on the contens of your `tracker/.env` file, if the `LOCAL` value is set to `True`.

## Testing

Tests are run via Github Actions with `pytest` at merge to the main branch (including code coverage), and on Pull Request branches. Test your code locally the way the GitHub Action would before merging to the `main` branch with

```shell
cd tracker
uv run pytest --cov --cov-report term
```

The Django way is with

```shell
cd tracker
uv run manage.py manage.py test
```

or

```shell
cd tracker
uv run manage.py test core.tests.test_core.CoreModelTestCase.test_delete  # <substitute or change the Python path to the test to run to run more granularly>
```

Tests use their own database, there is no setup required. In theory, both the Django and pytest sets run the same tests, but do be careful as there are ways they can diverge.

We haven't had to prevent merges because of code coverage dropping yet, so try to keep unit tests up to date as much as possible.

## Running a Test Server

This application will require a database. It uses Django, so whatever Django supports and how it is configured is what should be used. Development and testing occurs with SQLite, plans are for Postgres in production. To create a database for using with the application for development or production, run

```shell
cd tracker
uv run manage.py migrate
```

There is a Django command to install demo data that has a pre-configured set of users, organizations, and projects. Run it with

```shell
cd tracker
uv run manage.py install_demo_data
```

to populate your database with demo data. *This probably should not be used in production environments as there are easy-to-guess passwords and what-not.*

Running a test instance of the django server to use the API and User Interface is as simple as

```shell
cd tracker
uv run manage.py runserver 0.0.0.0:8000
```

You can also get to a Django prompt with

```shell
cd tracker
uv run manage.py shell_plus
```

and work with the live demo data that way, just like the Django code, but live in a terminal session.

# Visual Studio Code

Development environment files for Visual Studio Code are included. The `launch.json` file contains a debug configuration for running the Django web server, Django tests with the `uv run manage.py test` command, and the 'Install Demo Data' command. The `settings.json` file contains the configuration to use the Visual Studio Code Test Explorer feature to allow to run tests within the IDE and show test coverage using the `pytest` and `django-pytest` modules.

When committing changes to these files, be sure to callout changes in Pull Requests so they can be reviewed and properly tested by other developers, potentially on other platforms (Windows, Linux, etc.) for compatibility (though for now most developers are on Macs).

## TODO

Postgres DB config for testing and production.

A guide (.md file) for development with Postgres instead of SQLite.

Figure out how to consolidate the `.coveragerc` files. The one in `tracker` is the one the GitHub action uses, so it is the source of truth for now, but the one at the top level of the directory is for VSCode's TestExplorer. It is a copy and should just be stomped over as the main one in `tracker` changes. Maybe the GH Action can be modified with a `--cov-config` argument to point at it, will take testing and commits.

