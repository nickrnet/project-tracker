from django.core.management.base import BaseCommand

from project.models import status as project_issue_status_models


class Command(BaseCommand):
    def handle(self, *args, **options):
        project_issue_status_models.BuiltInIssueStatus.objects.initialize_built_in_statuses()
        self.stdout.write("Issue statuses initialized.")
