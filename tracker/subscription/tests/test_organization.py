from django.test import TestCase
from django.utils import timezone

from core.models.user import CoreUser
from core.models.organization import Organization, OrganizationData
from subscription.models.organization import OrganizationSubscriptionType, OrganizationSubscriptionTypeData, OrganizationSubscription, OrganizationSubscriptionData


class TestOrganizationSubscriptionType(TestCase):
    def setUp(self):
        self.system_user = CoreUser.objects.get_or_create_system_user()

    def test_initialize_subscription_types(self):
        OrganizationSubscriptionType.objects.initialize_subscriptions()
        subscriptions = OrganizationSubscriptionType.objects.all()
        self.assertEqual(subscriptions.count(), 6)
        self.assertTrue(subscriptions.filter(current__name='Trial').exists())
        self.assertTrue(subscriptions.filter(current__name='Free').exists())
        self.assertTrue(subscriptions.filter(current__name='Standard').exists())
        self.assertTrue(subscriptions.filter(current__name='Premium').exists())
        self.assertTrue(subscriptions.filter(current__name='Enterprise').exists())
        self.assertTrue(subscriptions.filter(current__name='On Premise').exists())

    def test_initialize_subscription_types_does_not_duplicate(self):
        organization_subscription_data = OrganizationSubscriptionTypeData.objects.create(created_by=self.system_user, name='Trial', description='Trial', is_active=True, term_length_days=7, user_limit=1)
        OrganizationSubscriptionType.objects.create(created_by=self.system_user, id='710153fc-3877-44a1-ae4c-ee9210194590', current=organization_subscription_data)
        OrganizationSubscriptionType.objects.initialize_subscriptions()
        subscriptions = OrganizationSubscriptionType.objects.all()
        self.assertEqual(subscriptions.count(), 6)
        self.assertTrue(subscriptions.filter(current__name='Trial').exists())
        self.assertTrue(subscriptions.filter(current__name='Free').exists())
        self.assertTrue(subscriptions.filter(current__name='Standard').exists())
        self.assertTrue(subscriptions.filter(current__name='Premium').exists())
        self.assertTrue(subscriptions.filter(current__name='Enterprise').exists())
        self.assertTrue(subscriptions.filter(current__name='On Premise').exists())


class TestOrganizationSubscription(TestCase):
    def setUp(self):
        self.system_user = CoreUser.objects.get_or_create_system_user()
        OrganizationSubscriptionType.objects.initialize_subscriptions()
        self.subscription_type = OrganizationSubscriptionType.objects.get(current__name='Trial')
        self.member1 = CoreUser.objects.create_core_user_from_web({'email': 'testuser1@project-tracker.dev', 'password': 'password'})
        organization_data = {
            'created_by_id': str(self.member1.id),
            'name': 'Test Organization',
            'responsible_party_email': 'testuser1@project-tracker.dev',
            'responsible_party_phone': '123-456-7890',
            'address_line_1': '123 Main St',
            'city': 'Anytown',
            'state': 'NY',
            'postal_code': '12345',
            'is_paid': True,
            'number_users_allowed': 5,
            }
        self.organization_data = OrganizationData.objects.create(**organization_data)
        self.organization = Organization.objects.create(
            created_by_id=self.member1.id,
            current=self.organization_data,
            )

    def test_create_organization_subscription(self):
        organization_subscription_data = OrganizationSubscriptionData.objects.create(created_by=self.system_user, subscription_type=self.subscription_type, expiration_date=timezone.now() + timezone.timedelta(days=self.subscription_type.current.term_length_days), expired=False)
        organization_subscription = OrganizationSubscription.objects.create(created_by=self.system_user, org=self.organization, current=organization_subscription_data)
        organization_subscription.set_expiration_date(self.system_user.id, self.subscription_type)
        self.assertIsNotNone(organization_subscription.current.expiration_date)
        expected_expiration_date = organization_subscription.created_on + timezone.timedelta(days=self.subscription_type.current.term_length_days)
        self.assertEqual(organization_subscription.current.expiration_date.date(), expected_expiration_date.date())

    def test_create_organization_subscription_no_user_no_subscription_type(self):
        organization_subscription_data = OrganizationSubscriptionData.objects.create(created_by=self.system_user, subscription_type=self.subscription_type, expiration_date=timezone.now() + timezone.timedelta(days=self.subscription_type.current.term_length_days), expired=False)
        organization_subscription = OrganizationSubscription.objects.create(created_by=self.system_user, org=self.organization, current=organization_subscription_data)
        organization_subscription.set_expiration_date()
        self.assertIsNotNone(organization_subscription.current.expiration_date)
        expected_expiration_date = organization_subscription.created_on + timezone.timedelta(days=self.subscription_type.current.term_length_days)
        self.assertEqual(organization_subscription.current.expiration_date.date(), expected_expiration_date.date())

    def test_organization_subscription_enterprise(self):
        enterprise_subscription_type = OrganizationSubscriptionType.objects.get(current__name='Enterprise')
        organization_subscription_data = OrganizationSubscriptionData.objects.create(created_by=self.system_user, subscription_type=enterprise_subscription_type, expiration_date=None, expired=False)
        organization_subscription = OrganizationSubscription.objects.create(created_by=self.system_user, org=self.organization, current=organization_subscription_data)
        organization_subscription.set_expiration_date(self.system_user.id, enterprise_subscription_type)
        self.assertIsNone(organization_subscription.current.expiration_date)

    def test_expire_organization_subscription(self):
        organization_subscription_data = OrganizationSubscriptionData.objects.create(created_by=self.system_user, subscription_type=self.subscription_type, expiration_date=timezone.now() + timezone.timedelta(days=self.subscription_type.current.term_length_days), expired=False)
        organization_subscription = OrganizationSubscription.objects.create(created_by=self.system_user, org=self.organization, current=organization_subscription_data)
        organization_subscription.set_expiration_date(self.system_user.id, self.subscription_type)
        organization_subscription.expire_subscription(self.system_user.id, self.subscription_type)
        organization_subscription.refresh_from_db()
        self.assertTrue(organization_subscription.current.expired)
        self.assertIsNotNone(organization_subscription.current.expiration_date)

    def test_expire_organization_subscription_no_user_no_subscription_type(self):
        organization_subscription_data = OrganizationSubscriptionData.objects.create(created_by=self.system_user, subscription_type=self.subscription_type, expiration_date=timezone.now() + timezone.timedelta(days=self.subscription_type.current.term_length_days), expired=False)
        organization_subscription = OrganizationSubscription.objects.create(created_by=self.system_user, org=self.organization, current=organization_subscription_data)
        organization_subscription.set_expiration_date()
        organization_subscription.expire_subscription()
        organization_subscription.refresh_from_db()
        self.assertTrue(organization_subscription.current.expired)
        self.assertIsNotNone(organization_subscription.current.expiration_date)

    def test_expire_organization_subscription_already_expired(self):
        organization_subscription_data = OrganizationSubscriptionData.objects.create(created_by=self.system_user, subscription_type=self.subscription_type, expiration_date=timezone.now() + timezone.timedelta(days=self.subscription_type.current.term_length_days), expired=True)
        organization_subscription = OrganizationSubscription.objects.create(created_by=self.system_user, org=self.organization, current=organization_subscription_data)
        self.assertTrue(organization_subscription.current.expired)
        organization_subscription.expire_subscription()
        organization_subscription.refresh_from_db()
        self.assertTrue(organization_subscription.current.expired)
        self.assertIsNotNone(organization_subscription.current.expiration_date)

    def test_get_organization_subscription(self):
        organization_subscription_data = OrganizationSubscriptionData.objects.create(created_by=self.system_user, subscription_type=self.subscription_type, expiration_date=timezone.now() + timezone.timedelta(days=self.subscription_type.current.term_length_days), expired=False)
        organization_subscription = OrganizationSubscription.objects.create(created_by=self.system_user, org=self.organization, current=organization_subscription_data)
        organization_subscription.set_expiration_date(self.system_user.id, self.subscription_type)
        self.assertFalse(organization_subscription.current.expired)
        subscriptions = OrganizationSubscription.active_objects.all()
        self.assertEqual(subscriptions.count(), 1)
        self.assertEqual(subscriptions.first(), organization_subscription)
