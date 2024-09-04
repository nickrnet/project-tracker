from django.core.management import call_command
from django.core.management.base import BaseCommand

from .modules import test_user_data_01
from .modules import test_user_data_02
from .modules import test_user_data_03
from .modules import test_organization_data_01
from .modules import test_organization_data_02
from project.management.commands.modules import test_git_repository_data_01
from project.management.commands.modules import test_git_repository_data_02
from project.management.commands.modules import test_project_data_01
from project.management.commands.modules import test_project_data_02


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Flushing database...")
        call_command('flush', '--noinput')
        call_command('setup')

        test_user_data_01.initialize_test_user_01()
        test_user_data_02.initialize_test_user_02()
        self.stdout.write("Test users initialized.")
        test_organization_data_01.initialize_test_organization_01()
        test_organization_data_02.initialize_test_organization_02()
        self.stdout.write("Test organizations initialized.")
        test_git_repository_data_01.initialize_test_git_repository_01()
        test_git_repository_data_02.initialize_test_git_repository_02()
        self.stdout.write("Test git repositories initialized.")
        test_project_data_01.initialize_test_project_01()
        test_project_data_02.initialize_test_project_02()
        self.stdout.write("Test projects initialized.")
        test_user_data_03.initialize_test_user_03()
        self.stdout.write("Test User 03 initialized and added to organizations and projects.")
