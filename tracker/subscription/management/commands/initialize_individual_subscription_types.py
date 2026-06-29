from django.core.management.base import BaseCommand

from core.util import timed_function
from subscription.models import individual as subscription_individual_models


class Command(BaseCommand):
    @timed_function
    def initialize_subscriptions(self, *args, **options):
        subscription_individual_models.IndividualSubscriptionType.objects.initialize_subscriptions()
        self.stdout.write("Individual subscription types initialized.")

    def handle(self, *args, **options):
        self.initialize_subscriptions(args, options)
