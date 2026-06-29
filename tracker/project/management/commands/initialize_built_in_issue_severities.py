from django.core.management.base import BaseCommand

from core.util import timed_function
from project.models import severity as project_issue_severity_models


class Command(BaseCommand):
    @timed_function
    def initialize_built_in_issue_severities(self, *args, **options):
        project_issue_severity_models.BuiltInIssueSeverity.objects.initialize_built_in_issue_severities()
        self.stdout.write("Issue severities initialized.")

    def handle(self, *args, **options):
        self.initialize_built_in_issue_severities(args, options)
