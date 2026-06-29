from django.core.management import call_command
from django.core.management.base import BaseCommand

from core.util import timed_function


class Command(BaseCommand):
    @timed_function
    def setup(self, *args, **options):
        call_command('initialize_system_user')
        call_command('initialize_api_user')
        call_command('initialize_individual_subscription_types')
        call_command('initialize_organization_subscription_types')
        call_command('initialize_built_in_issue_priorities')
        call_command('initialize_built_in_issue_statuses')
        call_command('initialize_built_in_issue_types')
        call_command('initialize_built_in_issue_severities')

    def handle(self, *args, **options):
        self.setup(args, options)
