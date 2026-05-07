import uuid

from django.db import models
from django.utils import timezone

from core.models import core as core_models
from core.models import user as core_user_models


class IndividualSubscriptionTypeData(core_models.CoreModel):
    """
    Contains data about a subscription.

    Parameters:
        name (str): The name of the subscription.
        description (str): A description of the subscription.
        is_active (bool): Whether the subscription is active or not. Inactive subscriptions are not available for assignment to users or organizations.
        term_length_days (int): The length of the subscription term in days. If the term length is 0, the subscription does not expire. This is used to calculate the expiration date of the subscription when it is assigned to a user or organization.
        user_limit (int): The number of users that can be assigned to this subscription. If the user limit is 0, there is no limit. This is used to enforce limits on the number of users that can be assigned to a subscription. If the limit is reached, no more users can be assigned to their projects until some are unassigned.
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="")
    is_active = models.BooleanField(default=True)
    term_length_days = models.IntegerField(default=30)
    user_limit = models.IntegerField(default=1)


class IndividualSubscriptionTypeManager(models.Manager):
    def initialize_subscriptions(self):
        built_in_subscription_types = [
            ('2f42c42f-e171-4022-a786-d5f37d277943', 'Trial', 'Trial', True, 7, 1),
            ('79a9026d-968e-4670-81bb-d3fbceb92a19', 'Free', 'Free', True, 30, 1),
            ('0f367241-83eb-448b-a993-f213a65f6dc7', 'Standard', 'Standard', True, 30, 5),
            ('653091cc-03e2-41d1-8c96-c3bd1aae17a0', 'Premium', 'Premium', True, 30, 10),
            ]
        system_user = core_user_models.CoreUser.objects.get_or_create_system_user()

        for subscription_id, name, description, is_active, term_length_days, user_limit in built_in_subscription_types:
            if uuid.UUID(subscription_id) not in self.values_list('id', flat=True):
                subscription_data = IndividualSubscriptionTypeData.objects.create(created_by=system_user, name=name, description=description, is_active=is_active, term_length_days=term_length_days, user_limit=user_limit)
                self.create(created_by=system_user, id=subscription_id, current=subscription_data)
            else:
                subscription_type = self.get(id=subscription_id)
                subscription_data = IndividualSubscriptionTypeData.objects.create(created_by=system_user, name=name, description=description, is_active=is_active, term_length_days=term_length_days, user_limit=user_limit)
                subscription_type.current = subscription_data
                subscription_type.save()


class IndividualSubscriptionTypeActiveManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().select_related('current').filter(deleted=None).filter(current__is_active=True)


class IndividualSubscriptionType(core_models.CoreModel):
    """
    A User subscription type. Not to be used on Organizations. The _real_ information about a subscription is stored in `current` as IndividualSubscriptionTypeData.
    """

    objects = IndividualSubscriptionTypeManager()
    active_objects = IndividualSubscriptionTypeActiveManager()

    current = models.ForeignKey(IndividualSubscriptionTypeData, on_delete=models.CASCADE)

    def __str__(self):
        return self.current.name


class IndividualSubscriptionActiveManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().select_related('current').filter(deleted=None)


class IndividualSubscriptionData(core_models.CoreModel):
    """
    Contains data about a subscription assigned to a user.

    Parameters:
        subscription (ForeignKey to IndividualSubscription): The subscription that this data is associated with. This is used to link the subscription data to the subscription. When a subscription is assigned to a user, a new IndividualSubscriptionData is created with the expiration date calculated based on the term length of the subscription type and the expired field set to False. When a subscription expires, a new IndividualSubscriptionData is created with the expired field set to True and the expiration date set to the date and time when the subscription expired. The current field of the IndividualSubscription is then updated to point to the new IndividualSubscriptionData.
        subscription_type (ForeignKey to IndividualSubscriptionType): The type of the subscription. This is used to determine the term length and user limit of the subscription. The term length is used to calculate the expiration date of the subscription when it is assigned to a user. The user limit is used to enforce limits on the number of users that can be assigned to a subscription. If a subscription has expired, no more users can be assigned to their projects until some are unassigned.
        expiration_date (datetime): The date and time when the subscription expires. This is calculated based on the term length of the subscription type when the subscription is assigned to the user. If the term length is 0, this field is not used and the subscription does not expire.
        expired (bool): Whether the subscription has expired or not. This is used to enforce limits on the number of users that can be assigned to a subscription. If a subscription has expired, no more users can be assigned to their projects until some are unassigned.
    """

    subscription = models.ForeignKey('IndividualSubscription', on_delete=models.CASCADE, blank=True, null=True)  # Needs to be nullable to allow for the creation of IndividualSubscriptionData before the IndividualSubscription is created. The subscription field is then updated to point to the correct IndividualSubscription after it is created.
    subscription_type = models.ForeignKey(IndividualSubscriptionType, on_delete=models.CASCADE)
    expiration_date = models.DateTimeField(blank=True, null=True)
    expired = models.BooleanField(default=False)


class IndividualSubscription(core_models.CoreModel):
    """
    A User subscription. Not to be used on Organizations.

    Parameters:
        individual (ForeignKey to CoreUser): The user that the subscription is assigned to.
        subscription_type (ForeignKey to IndividualSubscriptionType): The type of the subscription. This is used to determine the term length and user limit of the subscription. The term length is used to calculate the expiration date of the subscription when it is assigned to a user. The user limit is used to enforce limits on the number of users that can be assigned to a subscription. If the limit is reached, no more users can be assigned to their projects until some are unassigned.
        current (ForeignKey to IndividualSubscriptionData): The current data of the subscription. This is used to store the expiration date and whether the subscription has expired or not. When a subscription is assigned to a user, a new IndividualSubscriptionData is created with the expiration date calculated based on the term length of the subscription type and the expired field set to False. When a subscription expires, a new IndividualSubscriptionData is created with the expired field set to True and the expiration date set to the date and time when the subscription expired. The current field is then updated to point to the new IndividualSubscriptionData.
    """

    active_objects = IndividualSubscriptionActiveManager()

    individual = models.ForeignKey(core_user_models.CoreUser, on_delete=models.CASCADE)
    current = models.ForeignKey(IndividualSubscriptionData, on_delete=models.CASCADE)

    def set_expiration_date(self, user_id=None, subscription_type=None):
        if not user_id:
            user_id = self.individual_id
        if not subscription_type:
            subscription_type = self.current.subscription_type
        individual_subscription_data = IndividualSubscriptionData.objects.create(created_by_id=user_id, subscription=self, subscription_type_id=subscription_type.id, expiration_date=timezone.now() + timezone.timedelta(days=subscription_type.current.term_length_days), expired=False)
        self.current = individual_subscription_data
        self.save()

    def expire_subscription(self, user_id=None, subscription_type=None):
        if not user_id:
            user_id = self.individual_id
        if not subscription_type:
            subscription_type = self.current.subscription_type
        if self.current and not self.current.expired:
            individual_subscription_data = IndividualSubscriptionData.objects.create(created_by_id=user_id, subscription=self, subscription_type_id=subscription_type.id, expiration_date=timezone.now() - timezone.timedelta(days=1), expired=True)
            self.current = individual_subscription_data
            self.save()

    def __str__(self):
        return f"{self.current.subscription_type}, expires {self.current.expiration_date if self.current.expiration_date else 'never'}"
