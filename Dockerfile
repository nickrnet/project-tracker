FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install basic build dependencies required by many Python packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc libpq-dev postgresql-client git ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

# Copy pyproject and uv.lock first for layer caching
COPY pyproject.toml uv.lock* /app/

# Install `uv` and create the virtualenv with dependencies baked into the image.
# Each container gets its own .venv built during image build, not at runtime.
RUN pip install --upgrade pip setuptools wheel uv \
    && uv venv \
    && . .venv/bin/activate \
    && uv sync --dev

# Copy the project files
COPY ./tracker /app/tracker

WORKDIR /app/tracker

EXPOSE 8000

ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
