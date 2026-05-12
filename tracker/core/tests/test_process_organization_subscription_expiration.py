import logging

from django.test import TestCase
from django.utils import timezone

from core.models.organization import Organization, OrganizationData
from core.models.user import CoreUser
from core.tasks.process_organization_subscription_expiration import process_organization_subscription_expiration
from subscription.models.organization import (
    OrganizationSubscription,
    OrganizationSubscriptionData,
    OrganizationSubscriptionType,
    OrganizationSubscriptionTypeData,
)


class TestProcessOrganizationSubscriptionExpiration(TestCase):
    def setUp(self):
        self.user = CoreUser.objects.create_core_user_from_web({'email': 'testuser1@project-tracker.dev', 'password': 'password'})
        organization_data = {
            'created_by_id': str(self.user.id),
            'name': 'Test Organization',
            'responsible_party_email': 'testuser1@project-tracker.dev',
            'responsible_party_phone': '123-456-7890',
            'address_line_1': '123 Main St',
            'city': 'Anytown',
            'state': 'NY',
            'postal_code': '12345',
            }
        self.organization_data = OrganizationData.objects.create(**organization_data)
        self.organization = Organization.objects.create(
            created_by_id=self.user.id,
            current=self.organization_data,
            )
        subscription_type_data = OrganizationSubscriptionTypeData.objects.create(
            created_by=self.user,
            name='Test',
            description='Test subscription',
            is_active=True,
            term_length_days=30,
            user_limit=1,
        )
        self.subscription_type = OrganizationSubscriptionType.objects.create(
            created_by=self.user,
            current=subscription_type_data,
        )

    def test_process_organization_subscription_expiration_does_not_expire_valid_subscriptions(self):
        subscription_data = OrganizationSubscriptionData.objects.create(
            created_by=self.user,
            subscription_type=self.subscription_type,
            expiration_date=timezone.now() + timezone.timedelta(days=1),
            expired=False,
        )
        subscription = OrganizationSubscription.objects.create(
            created_by=self.user,
            org=self.organization,
            current=subscription_data,
        )
        with self.assertLogs(logger=logging.getLogger('core.tasks.process_organization_subscription_expiration'), level='INFO') as cm:
            process_organization_subscription_expiration()
        self.assertIn("Processed 0 expired organization subscriptions.", cm.output[1])
        subscription.refresh_from_db()
        self.assertFalse(subscription.current.expired)

    def test_process_organization_subscription_expiration_expires_subscriptions(self):
        subscription_data = OrganizationSubscriptionData.objects.create(
            created_by=self.user,
            subscription_type=self.subscription_type,
            expiration_date=timezone.now() - timezone.timedelta(days=1),
            expired=False,
        )
        subscription = OrganizationSubscription.objects.create(
            created_by=self.user,
            org=self.organization,
            current=subscription_data,
        )
        with self.assertLogs(logger=logging.getLogger('core.tasks.process_organization_subscription_expiration'), level='INFO') as cm:
            process_organization_subscription_expiration()
        self.assertIn("Processed 1 expired organization subscriptions.", cm.output[1])
        subscription.refresh_from_db()
        self.assertTrue(subscription.current.expired)
