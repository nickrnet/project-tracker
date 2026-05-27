from django.core.management.base import BaseCommand

from subscription.models import individual as subscription_individual_models


class Command(BaseCommand):
    def handle(self, *args, **options):
        subscription_individual_models.IndividualSubscriptionType.objects.initialize_subscriptions()
        self.stdout.write("Individual subscription types initialized.")
