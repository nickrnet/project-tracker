from django.core.management.base import BaseCommand

from subscription.models import organization as subscription_organization_type_models


class Command(BaseCommand):
    def handle(self, *args, **options):
        subscription_organization_type_models.OrganizationSubscriptionType.objects.initialize_subscriptions()
        self.stdout.write("Organization subscriptions initialized.")
