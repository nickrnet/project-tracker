import logging

from django.test import TestCase
from django.utils import timezone

from core.models.user import CoreUser
from core.tasks.process_individual_subscription_expiration import process_individual_subscription_expiration
from subscription.models.individual import (
    IndividualSubscription,
    IndividualSubscriptionData,
    IndividualSubscriptionType,
    IndividualSubscriptionTypeData,
)


class TestProcessIndividualSubscriptionExpiration(TestCase):
    def setUp(self):
        self.user = CoreUser.objects.create_core_user_from_web({'email': 'testuser1@project-tracker.dev', 'password': 'password'})
        subscription_type_data = IndividualSubscriptionTypeData.objects.create(
            created_by=self.user,
            name='Test',
            description='Test subscription',
            is_active=True,
            term_length_days=30,
            user_limit=1,
        )
        self.subscription_type = IndividualSubscriptionType.objects.create(
            created_by=self.user,
            current=subscription_type_data,
        )

    def test_process_individual_subscription_expiration_does_not_expire_valid_subscriptions(self):
        subscription_data = IndividualSubscriptionData.objects.create(
            created_by=self.user,
            subscription_type=self.subscription_type,
            expiration_date=timezone.now() + timezone.timedelta(days=1),
            expired=False,
        )
        subscription = IndividualSubscription.objects.create(
            created_by=self.user,
            individual=self.user,
            current=subscription_data,
        )
        with self.assertLogs(logger=logging.getLogger('core.tasks.process_individual_subscription_expiration'), level='INFO') as cm:
            process_individual_subscription_expiration()
        self.assertIn("Processed 0 expired individual subscriptions.", cm.output[1])
        subscription.refresh_from_db()
        self.assertFalse(subscription.current.expired)

    def test_process_individual_subscription_expiration_expires_subscriptions(self):
        subscription_data = IndividualSubscriptionData.objects.create(
            created_by=self.user,
            subscription_type=self.subscription_type,
            expiration_date=timezone.now() - timezone.timedelta(days=1),
            expired=False,
        )
        subscription = IndividualSubscription.objects.create(
            created_by=self.user,
            individual=self.user,
            current=subscription_data,
        )
        with self.assertLogs(logger=logging.getLogger('core.tasks.process_individual_subscription_expiration'), level='INFO') as cm:
            process_individual_subscription_expiration()
        self.assertIn("Processed 1 expired individual subscriptions.", cm.output[1])
        subscription.refresh_from_db()
        self.assertTrue(subscription.current.expired)
