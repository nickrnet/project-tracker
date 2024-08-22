from django.core.management.base import BaseCommand

from project.models import issue_type as project_issue_type_models


class Command(BaseCommand):
    def handle(self, *args, **options):
        project_issue_type_models.BuiltInIssueType.objects.initialize_built_in_types()
        self.stdout.write("Issue types initialized.")
