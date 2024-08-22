from django.core.management import call_command
from django.core.management.base import BaseCommand

from .modules import test_user_data
from .modules import test_organization_data
from project.management.commands.modules import test_git_repository_data
from project.management.commands.modules import test_project_data


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Flushing database...")
        call_command('flush', '--noinput')
        call_command('initialize_system_user')
        call_command('initialize_api_user')
        call_command('initialize_built_in_issue_priorities')
        call_command('initialize_built_in_issue_statuses')
        call_command('initialize_built_in_issue_types')

        test_user_data.initialize_test_user()
        self.stdout.write("Test user initialized.")
        test_organization_data.initialize_test_organization()
        self.stdout.write("Test organization initialized.")
        test_git_repository_data.initialize_test_git_repository()
        self.stdout.write("Test git repository initialized.")
        test_project_data.initialize_test_project()
        self.stdout.write("Test project initialized.")
