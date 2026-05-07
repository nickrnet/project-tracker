from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Delete local app migration files and regenerate migrations."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Preview migration files/directories that would be deleted.",
        )

    def _iterate_local_apps(self):
        base_dir = Path(settings.BASE_DIR)
        return sorted(
            app_dir
            for app_dir in base_dir.iterdir()
            if app_dir.is_dir() and (app_dir / "apps.py").exists()
        )

    def _iterate_migration_targets(self):
        for app_dir in self._iterate_local_apps():
            migrations_dir = app_dir / "migrations"
            if not migrations_dir.exists() or not migrations_dir.is_dir():
                continue

            for migration_path in migrations_dir.iterdir():
                if migration_path.name == "__init__.py":
                    continue
                yield migration_path

    @staticmethod
    def _delete_pycache_dir(pycache_dir):
        for pycache_file in pycache_dir.rglob("*"):
            if pycache_file.is_file():
                pycache_file.unlink()
        pycache_dir.rmdir()

    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        deleted_files = 0
        deleted_dirs = 0

        for migration_path in self._iterate_migration_targets():
            if migration_path.is_file():
                if dry_run:
                    self.stdout.write(f"Would delete file: {migration_path}")
                else:
                    migration_path.unlink()
                deleted_files += 1
                continue

            if migration_path.is_dir() and migration_path.name == "__pycache__":
                if dry_run:
                    self.stdout.write(f"Would delete directory: {migration_path}")
                else:
                    self._delete_pycache_dir(migration_path)
                deleted_dirs += 1

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f"Dry run: would delete {deleted_files} migration files and {deleted_dirs} directories."
                )
            )
            self.stdout.write(self.style.NOTICE("Skipped makemigrations in dry run mode."))
            return

        self.stdout.write(
            self.style.WARNING(
                f"Deleted {deleted_files} migration files and {deleted_dirs} directories."
            )
        )
        self.stdout.write(self.style.NOTICE("Running makemigrations..."))
        call_command("makemigrations")
        self.stdout.write(self.style.SUCCESS("Done."))
