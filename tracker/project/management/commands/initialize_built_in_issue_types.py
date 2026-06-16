from django.core.management.base import BaseCommand

from core.util import timed_function
from project.models import issue_type as project_issue_type_models


class Command(BaseCommand):
    @timed_function
    def initialize_built_in_issue_types(self, *args, **options):
        project_issue_type_models.BuiltInIssueType.objects.initialize_built_in_issue_types()
        self.stdout.write("Issue types initialized.")

    def handle(self, *args, **options):
        self.initialize_built_in_issue_types(args, options)
