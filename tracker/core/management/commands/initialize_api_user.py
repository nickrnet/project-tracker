from django.core.management.base import BaseCommand

from core.models import user as core_user_models


class Command(BaseCommand):
    def handle(self, *args, **options):
        core_user_models.CoreUser.objects.get_or_create_api_user()
        self.stdout.write("API user initialized.")
