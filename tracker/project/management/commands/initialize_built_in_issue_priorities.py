from django.core.management.base import BaseCommand

from core.util import timed_function
from project.models import priority as project_issue_priority_models


class Command(BaseCommand):
    @timed_function
    def initialize_built_in_issue_priorities(self, *args, **options):
        project_issue_priority_models.BuiltInIssuePriority.objects.initialize_built_in_issue_priorities()
        self.stdout.write("Issue priorities initialized.")

    def handle(self, *args, **options):
        self.initialize_built_in_issue_priorities(args, options)
