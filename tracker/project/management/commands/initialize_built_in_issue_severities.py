from django.core.management.base import BaseCommand

from project.models import severity as project_issue_severity_models


class Command(BaseCommand):
    def handle(self, *args, **options):
        project_issue_severity_models.BuiltInIssueSeverity.objects.initialize_built_in_severities()
        self.stdout.write("Issue priorities initialized.")
