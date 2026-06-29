from django.core.management.base import BaseCommand

from core.util import timed_function
from core.models import user as core_user_models


class Command(BaseCommand):
    @timed_function
    def initialize_system_user(self, *args, **options):
        core_user_models.CoreUser.objects.get_or_create_system_user()
        self.stdout.write("System user initialized.")

    def handle(self, *args, **options):
        self.initialize_system_user(args, options)
