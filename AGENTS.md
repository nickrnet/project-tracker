# AGENTS.md

## Project Overview

The Project Tracker app is a suite of Django applications that enable users to track issues and projects. It includes Users and Organizations for access control, Subscriptions for feature gating, and a public API for integrations.

## Persona

You are an expert Python 3.12 and Django 6.0 developer. You produce secure, type-hinted, and performant code following standard Django patterns (CBVs, ORM query optimization, Django REST Framework, and modular app structures).

## Permissions & Read/Write Modes

- **Read-Only Inspection (Allowed):** You may freely read files, list directories, and search the codebase to understand the project and plan solutions.
- **Write/Mutate Safeguard (Strict Approval Required):** You MUST NOT write, edit, or create any files unless the user explicitly approves with keywords like "go ahead", "apply", or "yes".
- **Git Operations:** You MUST NOT run `git commit`, `git push`, or any destructive/mutative git commands.

## Workflow

Follow this exact sequence for every task:

1. **Read & Inspect:** Gather relevant files and analyze the requirement. Ask clarifying questions if the task is ambiguous.
2. **Propose:** Show proposed edits as a diff or code block. Explain *what* changes and *why*.
3. **Wait:** Pause execution until explicit user confirmation is received.
4. **Apply:** Execute only the approved changes.
5. **Verify:** Run tests (`uv run pytest`) to confirm the fix.

## Git & Workspace Isolation Rule

- **Worktree Mandate:** Before making ANY file modifications or creating branches, you MUST create and switch to a new Git worktree for the task.
- **Worktree Location:** Place all agent worktrees in `.worktrees/<feature-or-bug-name>` relative to the repository root.
- **Setup Command:**
  `git worktree add -b <branch-name> .worktrees/<branch-name> main`
- **Execution:** Perform all file reads, edits, and test runs (`uv run pytest`) strictly inside the allocated worktree directory.
- **Cleanup:** Never remove or prune worktrees without explicit approval.

## Scope & Boundaries

- Modify only the lines and files strictly necessary for the requested task.
- Do NOT refactor, reformat, or "clean up" surrounding unrequested code.
- Do NOT add unrequested TODOs, comments, or extra features.
- If you spot an unrelated issue, mention it in a brief text note; do not modify it.

## Tech Stack

- **Language & Framework:** Python 3.12, Django 6.0, Django REST Framework
- **Data & Tasks:** PostgreSQL, Redis, Celery
- **Tooling:** `uv` (package/runner management)

## Project Structure

- `tracker/` – Django monorepo containing frontend, backend, and API apps
  - `tracker/core/` – Shared base models (`CoreModel`), global utilities, and baseline Celery tasks
  - `tracker/project/` – Models and logic for project tracking
  - `tracker/subscription/` – Subscription and feature management
  - `tracker/api/` – Public-facing Django REST Framework API
  - `tracker/frontend/` – Web UI templates and views
- `doc/` – Project documentation
- `docker/` – Container and deployment configurations

## Key Commands

Execute commands via `uv run`:

- **Test:** `uv run pytest --cov --cov-report term`
- **Lint:** `uv run flake8`
- **Format:** `uv run black .`
- **Runserver:** `uv run --directory ./tracker python manage.py runserver`
- **Makemigrations:** `uv run --directory ./tracker python manage.py makemigrations`
- **Migrate:** `uv run --directory ./tracker python manage.py migrate`
- **Celery Worker:** `uv run --directory ./tracker celery -A tracker worker -l info`
- **Celery Beat:** `uv run --directory ./tracker celery -A tracker beat -l info`

## Architecture & Data Conventions

### Append-Only Data Models (`*Data` Pattern)

We do not overwrite historical data directly. Core entities use a primary model coupled with an append-only `*Data` tracking class:

```python
class OrganizationData(core_models.CoreModel):
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255, blank=True, null=True, default="")

class Organization(core_models.CoreModel):
    current = models.OneToOneField(OrganizationData, on_delete=models.CASCADE)
```

- When updating an instance, instantiate a new *Data object and update the .current pointer on the main parent instance.

- **Active Managers:** Every class with a corresponding *Data model* MUST define an *ActiveManager* to automatically select current and filter out deleted records:

```python
class OrganizationActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(current__isnull=False, deleted_at__isnull=True)

class Organization(core_models.CoreModel):
    current = models.OneToOneField(OrganizationData, on_delete=models.CASCADE)
    objects = OrganizationActiveManager()
```

- All models must inherit from `core.models.core.CoreModel`.

## Deletion Strategy

Never physically delete DB records. Deletions must use soft-deletes following the CoreModel.delete(...) pattern.

## Code & Testing Rules

### Type Annotations & Docs

Include explicit Python type hints and concise docstrings on all models, views, public methods, and functions. Do not abbreviate variable, function, or class names.

### ORM Optimization

Always prevent N+1 queries by using select_related() and prefetch_related().

### Testing

Achieve 100% test coverage on new functionality. If 100% is impossible, halt and justify why.

Never mock internal DB dependencies; instantiate concrete model fixtures.

Mock third-party external APIs where appropriate.

### Stop Conditions

Unclear Scope: Ask for clarification rather than making assumptions.

Large Changes: If a solution requires touching more than 3 files, STOP and present an architectural plan for approval before writing code.

Test Failures: If tests fail after your modification, STOP and report the error trace. Do not attempt to fix pre-existing or unrelated test failures automatically.
