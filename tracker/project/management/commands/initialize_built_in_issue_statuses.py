from django.core.management.base import BaseCommand

from core.util import timed_function
from project.models import status as project_issue_status_models


class Command(BaseCommand):
    @timed_function
    def initialize_built_in_issue_statuses(self, *args, **options):
        project_issue_status_models.BuiltInIssueStatus.objects.initialize_built_in_issue_statuses()
        self.stdout.write("Issue statuses initialized.")

    def handle(self, *args, **options):
        self.initialize_built_in_issue_statuses(args, options)
