from django.test import TestCase
from django.utils import timezone

from core.models.user import CoreUser
from subscription.models.individual import IndividualSubscriptionType, IndividualSubscriptionTypeData, IndividualSubscription, IndividualSubscriptionData


class TestIndividualSubscriptionTypes(TestCase):
    def setUp(self):
        self.system_user = CoreUser.objects.get_or_create_system_user()

    def test_initialize_subscription_types(self):
        IndividualSubscriptionType.objects.initialize_subscriptions()
        subscriptions = IndividualSubscriptionType.objects.all()
        self.assertEqual(subscriptions.count(), 4)
        self.assertTrue(subscriptions.filter(current__name='Trial').exists())
        self.assertTrue(subscriptions.filter(current__name='Free').exists())
        self.assertTrue(subscriptions.filter(current__name='Standard').exists())
        self.assertTrue(subscriptions.filter(current__name='Premium').exists())

    def test_initialize_subscription_types_does_not_duplicate(self):
        individual_subscription_data = IndividualSubscriptionTypeData.objects.create(created_by=self.system_user, name='Trial', description='Trial Description', is_active=True, term_length_days=7, user_limit=1)
        IndividualSubscriptionType.objects.create(created_by=self.system_user, id='2f42c42f-e171-4022-a786-d5f37d277943', current=individual_subscription_data)
        IndividualSubscriptionType.objects.initialize_subscriptions()
        subscriptions = IndividualSubscriptionType.objects.all()
        self.assertEqual(subscriptions.count(), 4)
        self.assertTrue(subscriptions.filter(current__name='Trial').exists())
        self.assertTrue(subscriptions.filter(current__name='Free').exists())
        self.assertTrue(subscriptions.filter(current__name='Standard').exists())
        self.assertTrue(subscriptions.filter(current__name='Premium').exists())


class TestIndividualSubscription(TestCase):
    def setUp(self):
        self.system_user = CoreUser.objects.get_or_create_system_user()
        IndividualSubscriptionType.objects.initialize_subscriptions()
        self.subscription_type = IndividualSubscriptionType.objects.get(current__name='Trial')

    def test_create_individual_subscription(self):
        subscription_data = IndividualSubscriptionData.objects.create(created_by=self.system_user, subscription_type=self.subscription_type, expiration_date=timezone.now() + timezone.timedelta(days=self.subscription_type.current.term_length_days), expired=False)
        subscription = IndividualSubscription.objects.create(created_by=self.system_user, individual=self.system_user, current=subscription_data)
        subscription.current.subscription = subscription
        subscription.current.save()
        subscription.set_expiration_date(self.system_user.id, self.subscription_type)
        self.assertIsNotNone(subscription.current.expiration_date)
        expected_expiration_date = subscription.created_on + timezone.timedelta(days=self.subscription_type.current.term_length_days)
        self.assertEqual(subscription.current.expiration_date.date(), expected_expiration_date.date())

    def test_create_individual_subscription_no_user_no_subscription_type(self):
        subscription_data = IndividualSubscriptionData.objects.create(created_by=self.system_user, subscription_type=self.subscription_type, expiration_date=timezone.now() + timezone.timedelta(days=self.subscription_type.current.term_length_days), expired=False)
        subscription = IndividualSubscription.objects.create(created_by=self.system_user, individual=self.system_user, current=subscription_data)
        subscription.current.subscription = subscription
        subscription.current.save()
        subscription.set_expiration_date()
        self.assertIsNotNone(subscription.current.expiration_date)
        expected_expiration_date = subscription.created_on + timezone.timedelta(days=self.subscription_type.current.term_length_days)
        self.assertEqual(subscription.current.expiration_date.date(), expected_expiration_date.date())

    def test_expire_individual_subscription(self):
        subscription_data1 = IndividualSubscriptionData.objects.create(created_by=self.system_user, subscription_type=self.subscription_type, expiration_date=timezone.now() + timezone.timedelta(days=self.subscription_type.current.term_length_days), expired=False)
        subscription1 = IndividualSubscription.objects.create(created_by=self.system_user, individual=self.system_user, current=subscription_data1)
        subscription1.current.subscription = subscription1
        subscription1.current.save()
        subscription1.set_expiration_date(self.system_user.id, self.subscription_type)
        subscription1.expire_subscription(self.system_user.id, self.subscription_type)
        subscription1.refresh_from_db()
        self.assertTrue(subscription1.current.expired)

    def test_expire_individual_subscription_no_user_no_subscription_type(self):
        subscription_data1 = IndividualSubscriptionData.objects.create(created_by=self.system_user, subscription_type=self.subscription_type, expiration_date=timezone.now() + timezone.timedelta(days=self.subscription_type.current.term_length_days), expired=False)
        subscription1 = IndividualSubscription.objects.create(created_by=self.system_user, individual=self.system_user, current=subscription_data1)
        subscription1.current.subscription = subscription1
        subscription1.current.save()
        subscription1.set_expiration_date()
        subscription1.expire_subscription()
        subscription1.refresh_from_db()
        self.assertTrue(subscription1.current.expired)

    def test_expire_individual_subscription_already_expired(self):
        subscription_data1 = IndividualSubscriptionData.objects.create(created_by=self.system_user, subscription_type=self.subscription_type, expiration_date=timezone.now() + timezone.timedelta(days=self.subscription_type.current.term_length_days), expired=True)
        subscription1 = IndividualSubscription.objects.create(created_by=self.system_user, individual=self.system_user, current=subscription_data1)
        subscription1.current.subscription = subscription1
        subscription1.current.save()
        self.assertTrue(subscription1.current.expired)
        subscription1.expire_subscription()
        subscription1.refresh_from_db()
        self.assertTrue(subscription1.current.expired)

    def test_get_individual_subscriptions(self):
        subscription_data1 = IndividualSubscriptionData.objects.create(created_by=self.system_user, subscription_type=self.subscription_type, expiration_date=timezone.now() + timezone.timedelta(days=self.subscription_type.current.term_length_days), expired=False)
        subscription1 = IndividualSubscription.objects.create(created_by=self.system_user, individual=self.system_user, current=subscription_data1)
        subscription1.current.subscription = subscription1
        subscription1.current.save()
        self.assertFalse(subscription1.current.expired)
        subscriptions = IndividualSubscription.active_objects.all()
        self.assertEqual(subscriptions.count(), 1)
        self.assertEqual(subscriptions.first(), subscription1)
