from django.core.management.base import BaseCommand

from project.models import priority as project_issue_priority_models


class Command(BaseCommand):
    def handle(self, *args, **options):
        project_issue_priority_models.BuiltInIssuePriority.objects.initialize_built_in_priorities()
        self.stdout.write("Issue priorities initialized.")
