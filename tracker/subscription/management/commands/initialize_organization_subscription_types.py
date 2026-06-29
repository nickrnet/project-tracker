from django.core.management.base import BaseCommand

from core.util import timed_function
from subscription.models import organization as subscription_organization_type_models


class Command(BaseCommand):
    @timed_function
    def initialize_subscriptions(self, *args, **options):
        subscription_organization_type_models.OrganizationSubscriptionType.objects.initialize_subscriptions()
        self.stdout.write("Organization subscriptions initialized.")

    def handle(self, *args, **options):
        self.initialize_subscriptions(args, options)
