import uuid

from django.db import models
from django.utils import timezone

from core.models import core as core_models
from core.models import user as core_user_models


class OrganizationSubscriptionTypeData(core_models.CoreModel):
    """
    Contains data about a subscription type.

    Parameters:
        name (str): The name of the subscription type.
        description (str): A description of the subscription type.
        is_active (bool): Whether the subscription type is active or not. Inactive subscription types are not available for assignment to users or organizations.
        term_length_days (int): The length of the subscription term in days. If the term length is 0, the subscription does not expire. This is used to calculate the expiration date of the subscription when it is assigned to a user or organization.
        user_limit (int): The number of users that can be assigned to this subscription type. If the user limit is 0, there is no limit. This is used to enforce limits on the number of users that can be assigned to a subscription type. If the limit is reached, no more users can be assigned to their projects until some are unassigned.
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="")
    is_active = models.BooleanField(default=True)
    term_length_days = models.IntegerField(default=30)
    user_limit = models.IntegerField(default=1)


class OrganizationSubscriptionTypeManager(models.Manager):
    def initialize_subscriptions(self):
        built_in_subscriptions = [
            ('710153fc-3877-44a1-ae4c-ee9210194590', 'Trial', 'Trial', True, 7, 1),
            ('eecfb535-2a2e-4c39-9fca-dfb39e07d010', 'Free', 'Free', True, 30, 1),
            ('d79dece7-16a2-4550-b05f-e887b5b0e1cd', 'Standard', 'Standard', True, 30, 5),
            ('12989c06-fd9e-4436-8754-07cdb9a7f3ec', 'Premium', 'Premium', True, 30, 10),
            ('b97b2747-ab8d-45f1-a924-a2323d343b77', 'Enterprise', 'Enterprise', True, 0, 0),
            ('3f5be9e8-4aae-4a35-8fb7-5c063af834c5', 'On Premise', 'On Premise', True, 0, 0),
            ]
        system_user = core_user_models.CoreUser.objects.get_or_create_system_user()

        for subscription_id, name, description, is_active, term_length_days, user_limit in built_in_subscriptions:
            if uuid.UUID(subscription_id) not in self.values_list('id', flat=True):
                subscription_data = OrganizationSubscriptionTypeData.objects.create(created_by=system_user, name=name, description=description, is_active=is_active, term_length_days=term_length_days, user_limit=user_limit)
                self.create(created_by=system_user, id=subscription_id, current=subscription_data)


class OrganizationSubscriptionTypeActiveManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().select_related('current').filter(deleted=None).filter(current__is_active=True)


class OrganizationSubscriptionType(core_models.CoreModel):
    """
    An Organization subscription type. Not to be used on Users. The _real_ information about a subscription type is stored in `current` as OrganizationSubscriptionTypeData.
    """

    objects = OrganizationSubscriptionTypeManager()
    active_objects = OrganizationSubscriptionTypeActiveManager()

    current = models.ForeignKey(OrganizationSubscriptionTypeData, on_delete=models.CASCADE)


class OrganizationSubscriptionData(core_models.CoreModel):
    """
    Contains data about a subscription.

    Parameters:
        subscription_type (OrganizationSubscriptionType): The subscription type of the subscription. This is used to determine the expiration date of the subscription and to enforce limits on the number of users that can be assigned to the subscription.
        expiration_date (datetime): The date and time when the subscription expires. This is calculated based on the term length of the subscription type when the subscription is created or renewed. If the term length of the subscription type is 0, this field is null and the subscription does not expire.
    """

    subscription = models.ForeignKey('OrganizationSubscription', on_delete=models.CASCADE, related_name='data', blank=True, null=True)
    subscription_type = models.ForeignKey(OrganizationSubscriptionType, on_delete=models.CASCADE)
    expiration_date = models.DateTimeField(null=True, blank=True)
    expired = models.BooleanField(default=False)


class OrganizationSubscription(core_models.CoreModel):
    """
    An Organization subscription.

    Parameters:
        org (ForeignKey to Organization): The organization that this subscription is associated with.
        subscription_type (ForeignKey to OrganizationSubscriptionType): The type of the subscription. This is used to determine the expiration date of the subscription and to enforce limits on the number of users that can be assigned to the subscription.
        expiration_date (datetime): The date and time when the subscription expires. This is calculated based on the term length of the subscription type when the subscription is created or renewed. If the term length of the subscription type is 0, this field is null and the subscription does not expire.
        current (ForeignKey to OrganizationSubscriptionData): The current data for this subscription. This is used to track the current expiration date and subscription type of the subscription. When a subscription is created or renewed, a new OrganizationSubscriptionData is created with the expiration date calculated based on the term length of the subscription type and the expired field set to False. When a subscription expires, a new OrganizationSubscriptionData is created with the expired field set to True and the expiration date set to the date and time when the subscription expired. The current field of the OrganizationSubscription is then updated to point to the new OrganizationSubscriptionData.
    """

    org = models.ForeignKey('core.Organization', on_delete=models.CASCADE)
    current = models.ForeignKey(OrganizationSubscriptionData, on_delete=models.CASCADE)

    def set_expiration_date(self, user_id=None, subscription_type=None):
        if not user_id:
            user_id = core_user_models.CoreUser.objects.get_or_create_system_user().id
        if not subscription_type:
            subscription_type = self.current.subscription_type
        if subscription_type.current.term_length_days > 0:
            organization_subscription_data = OrganizationSubscriptionData.objects.create(created_by_id=user_id, subscription=self, subscription_type_id=subscription_type.id, expiration_date=timezone.now() + timezone.timedelta(days=subscription_type.current.term_length_days), expired=False)
            self.current = organization_subscription_data
            self.save()

    def expire_subscription(self, user_id=None, subscription_type=None):
        if not user_id:
            user_id = core_user_models.CoreUser.objects.get_or_create_system_user().id
        if not subscription_type:
            subscription_type = self.current.subscription_type
        if self.current and not self.current.expired:
            organization_subscription_data = OrganizationSubscriptionData.objects.create(created_by_id=user_id, subscription=self, subscription_type_id=subscription_type.id, expiration_date=timezone.now(), expired=True)
            self.current = organization_subscription_data
            self.save()

    def __str__(self):
        return f"{self.subscription_type}, expires on {self.current.expiration_date if self.current.expiration_date else 'never'}"
