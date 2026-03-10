**Production Deployment**

This document describes a simple, pragmatic production deployment approach using
the provided `docker-compose.prod.yml` skeleton. It's intended as a starting
point for small deployments (VMs, single hosts) or for local testing of a
production-like environment. For serious production use you should prefer
immutable images built in CI, a managed database, and a proven orchestration
platform (Kubernetes, ECS, Nomad, etc.).

- **Files you should use**: `docker-compose.prod.yml`, `.env.prod` (created
  from `.env.prod.sample`), and your `secrets/` directory containing Docker
  secret files.

1) Prepare secrets and environment

  - Create the `secrets/` directory (keep it out of git and set restrictive
    permissions):

    ```sh
    mkdir -p secrets
    printf '%s' "supersecret_pg_password" > secrets/postgres_password
    printf '%s' "django-secret-key-value" > secrets/secret_key
    chmod 600 secrets/*
    ```

  - Copy the sample env and edit values:

    ```sh
    cp .env.prod.sample .env.prod
    # Edit .env.prod and set DATABASE_URL or POSTGRES_* values as needed.
    ```

  - Important: Do not commit `.env.prod` or the `secrets/` files.

2) Build and run

  - For local testing with the production compose file (builds images locally):

    ```sh
    docker-compose -f docker-compose.prod.yml --env-file .env.prod up --build -d
    ```

  - **Note**: The web service automatically runs migrations and collectstatic on startup,
    so you don't need to run them manually. The database will also be created
    automatically if it doesn't exist.

  - To manually run migrations or collectstatic (if needed):

    ```sh
    docker-compose -f docker-compose.prod.yml --env-file .env.prod exec web uv run manage.py migrate
    docker-compose -f docker-compose.prod.yml --env-file .env.prod exec web uv run manage.py collectstatic --noinput
    ```

3) Deployment recommendations

  - CI/CD: Prefer building images in CI and pushing them to a registry. In
    production-compose replace the `build:` keys with `image: your-registry/your-image:tag`.
  - Reverse proxy / TLS: Put a reverse proxy (NGINX, Traefik) in front of the
    `web` service to handle TLS termination, static file caching, gzip, and
    request buffering.
  - Database: Use a managed Postgres (RDS, Cloud SQL) in production for durability
    and backups. If you self-host Postgres, make sure you have backups and a
    monitoring/alerting plan.
  - Secrets: Use a secrets manager when possible. Docker secrets are better than
    plaintext env vars, but an external secrets manager is preferable.

4) Scaling

  - Scale workers independently from web processes. Example:

    ```sh
    docker-compose -f docker-compose.prod.yml up -d --scale worker=3
    ```

  - Monitor Celery queues and tune the number of worker processes/threads per
    host according to CPU/memory and queue depth.

5) Volumes and backups

  - The compose skeleton uses named volumes (`postgres_data`, `redis_data`).
    Ensure you have a backup strategy for any stateful volumes (database and
    attachments). For media/static files prefer object storage (S3) for
    scalability and backups.

6) Logging & Monitoring

  - Send application logs to a central system (ELK/EFK, Loki, Datadog). Use
    structured logging where possible. Configure access and rotation for any
    logs written to disk inside containers.

7) Security

  - Ensure `DEBUG=false` in production.
  - Restrict `ALLOWED_HOSTS` to your hostnames.
  - Keep secret files permissions restricted (600) and restrict access to the
    deployment host.

8) Next steps / advanced

  - Replace compose with orchestration (Kubernetes) for multi-host, scalable
    production deployments.
  - Add health checks, readiness/liveness probes, and rolling deployments.
  - Integrate with a hosted Postgres and Redis for reliability.

If you'd like, I can generate a `docker-compose.prod.override.yml` with an
example NGINX proxy (with TLS placeholders), or a short CI job snippet that
builds and pushes images to a registry and deploys with SSH/Ansible.

9) Enabling NGINX TLS and static root (optional override)

  - The repository includes `docker-compose.prod.override.yml` and
    `docker/nginx/prod-ssl.conf` as an example TLS configuration. Use them by
    combining compose files so you don't permanently alter `docker-compose.prod.yml`:

    ```sh
    docker-compose -f docker-compose.prod.yml -f docker-compose.prod.override.yml up --build -d
    ```

  - Provide certificate files locally (or via your orchestration or secret
    manager). Example placeholder filenames used in the override:

    ```sh
    secrets/fullchain.pem   # public cert chain
    secrets/privkey.pem     # private key (keep safe)
    ```

  - The override mounts `fullchain.pem` and `privkey.pem` into the nginx
    container at `/etc/ssl/certs/fullchain.pem` and
    `/etc/ssl/private/privkey.pem`. If you use an external TLS terminator
    (cloud load balancer, Traefik), you can skip the override entirely.

  - Static files: The `web` service writes static files into a named volume
    (`static_data`) via `collectstatic`. NGINX mounts that same named volume
    read-only to serve the files. Confirm your Django `settings.py` includes:

    ```py
    # settings.py
    STATIC_ROOT = '/app/staticfiles'
    ```

    Then run collectstatic after starting the stack:

    ```sh
    docker-compose -f docker-compose.prod.yml -f docker-compose.prod.override.yml run --rm web uv run manage.py collectstatic --noinput
    ```

  - Security reminder: keep private keys out of version control and prefer a
    secrets manager or cloud certificate store for production deployments.


  10) Quick enable commands for TLS options

    The project supports two TLS approaches via the production override:

    - Option A — automatic Let's Encrypt using `nginx-proxy` + `acme-companion`.
    - Option B — manual certificates with `nginx` serving TLS (you manage certs).

    Option A — automatic Let's Encrypt (recommended for single trusted host)

    1. Ensure `.env.prod` contains your domain and contact email:

      ```sh
      NGINX_HOST=example.com
      LETSENCRYPT_EMAIL=ops@example.com
      ```

    2. Start the stack (proxy + acme companion):

      ```sh
      docker-compose -f docker-compose.prod.yml -f docker-compose.prod.override.yml up --build -d
      ```

    3. Run migrations and collectstatic:

      ```sh
      docker-compose -f docker-compose.prod.yml -f docker-compose.prod.override.yml run --rm web uv run manage.py migrate --noinput
      docker-compose -f docker-compose.prod.yml -f docker-compose.prod.override.yml run --rm web uv run manage.py collectstatic --noinput
      ```

    Option B — manual certs (you manage certificates)

    1. Provide cert files under `secrets/`:

      ```sh
      mkdir -p secrets
      cp /path/to/fullchain.pem secrets/fullchain.pem
      cp /path/to/privkey.pem secrets/privkey.pem
      chmod 600 secrets/*
      ```

    2. Edit `docker-compose.prod.override.yml` and uncomment the `nginx` service
      block (the file contains a commented example). Then start the stack:

      ```sh
      docker-compose -f docker-compose.prod.yml -f docker-compose.prod.override.yml up --build -d
      ```

    3. Run migrations and collectstatic:

      ```sh
      docker-compose -f docker-compose.prod.yml -f docker-compose.prod.override.yml run --rm web uv run manage.py migrate --noinput
      docker-compose -f docker-compose.prod.yml -f docker-compose.prod.override.yml run --rm web uv run manage.py collectstatic --noinput
      ```

    Notes:
    - Do not enable both options at once; they both bind ports 80/443.
    - The automatic option requires mounting the Docker socket; use it only
     on trusted single-host deployments. For multi-host or managed setups,
     prefer an external TLS terminator or cloud-managed certificates.

    10) Environment variables reference

      A few environment variables are particularly important when running the
      production compose stacks. These can be placed in `.env.prod` (see
      `.env.prod.sample`) or provided by your deployment system.

      - `DJANGO_SETTINGS_MODULE`: Should be set to `tracker.settings.production` to
        ensure Django loads the production settings file. The compose files set a
        sensible default, but overriding here is possible for troubleshooting.

      - `CELERY_BROKER_URL`: URL for your Celery broker (e.g., `redis://redis:6379/0`).
        Workers and beat use this to connect to the broker; make sure it matches
        your running Redis or messaging service.

      - `DATABASE_URL`: Full DB connection URL (Postgres recommended). If not
        provided, the app falls back to SQLite for convenience, but Postgres is
        preferred in production.

      - `SECRET_KEY_FILE`: Path to a file containing the Django `SECRET_KEY`,
        e.g. `/run/secrets/secret_key` when using Docker secrets. `production.py`
        will read the key from this file if present; otherwise it falls back to
        `DJANGO_SECRET_KEY` environment variable.

      See `.env.prod.sample` for example values and comments.

**TODO**

Investigate a Traefik-based override instead of the docker-socket-based proxy instead of the nginx+acme.
