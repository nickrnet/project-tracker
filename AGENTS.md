# AGENTS.md

## Project Overview

The Project Tracker app is a set of Django apps that let users track issues, tests, and projects. It includes Users and Organizations for permissions, and Subscriptions for managing access.

## Persona

You are an expert developer for this project. You specialize in **[Python, Django, and Bootstrap]** and translate that into **[a project tracker app called Project Tracker]**.

## Tech Stack
- Python 3.12
- Django 5.2 + Django REST Framework
- PostgreSQL, Redis, Celery

## Project Structure
  - `tracker/` – The Django code for the Project Tracker apps, a monorepo for frontend, backend, and api
  - `tracker/core` - The Django backend code for Core Project Tracker features, including globally inherited base model classes, and Celery tasks
  - `tracker/project` - The Django backend code for the Project Tracker project models
  - `tracker/subscription` - The Django backend code for the Project Tracker subscriptions
  - `tracker/api` – The Django code for the public Project Tracker API
  - `tracker/frontend` - The Django frontend code for the public Project Tracker web site
  - `doc/` - Documentation about the project
  - `docker/` - Files included in Docker images

## Commands

- **Test:** `uv run pytest --cov --cov-report term`

## Code Style

- All models should be a subclass of `core.models.core.CoreModel`
- We never overwrite data in the database, to keep history of how data changes

  There is typically a class with a corresponding `*Data` class, like:

  ```python
  ...
  class OrganizationData(core_models.CoreModel):
    ...
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255, blank=True, null=True, default="")
    ...
  class Organization(core_models.CoreModel):
    ...
    current = models.ForeignKey(OrganizationData, on_delete=models.CASCADE)
  ```

  Then, when a record gets updated, in a `view` for example, we create a new `*Data` class and only change the `current` field on the main class

  Make sure every class that has a corresponding `*Data` class ForeignKey has an `*ActiveManager` to select the related `current` field and filter deleted items, like:

  ```python
  class OrganizationActiveManager(models.Manager):
      def get_queryset(self):
          return super().get_queryset().select_related('current', 'subscription').filter(deleted=None)
  ```

  There are rare cases to not have a corresponding `*Data` class, you should ask the developer if you ever think it should *not* be used

- We do not ever delete data from the database, deleting records from the database will be a Celery task at some point

  Follow the `CoreModel.delete(...)` pattern

## Boundaries

- ✅ **Always:**
  - Add Python docstrings to model classes and functions to document what it is for and any arguments or parameters
  - Run tests before commits
  - List only human authors in git commits

- ⚠️ **Ask first:**
  - Database schema changes
  - Adding new dependencies

### 🚫 Never

- Commit secrets or `.env` files
- Abbreviate variable or function or class names
- Force push to main

## Testing Guidelines

- Write unit tests for all new functionality, get code coverage to 100%
- *Never* mock internal dependencies in tests, always create new items for tests
- Mock external dependencies when appropriate
- Ensure tests are deterministic and isolated
