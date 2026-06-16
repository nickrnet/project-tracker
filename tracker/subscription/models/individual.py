import uuid

from django.db import models
from django.utils import timezone

from core.models import core as core_models
from core.models import user as core_user_models


class IndividualSubscriptionTypeData(core_models.CoreModel):
    """
    Contains data about a subscription.

    Parameters:
        individual_subscription_type (IndividualSubscriptionType): The Individual Subscription Type.
        name (str): The name of the subscription.
        description (str): A description of the subscription.
        is_active (bool): Whether the subscription is active or not. Inactive subscriptions are not available for assignment to users or organizations.
        term_length_days (int): The length of the subscription term in days. If the term length is 0, the subscription does not expire. This is used to calculate the expiration date of the subscription when it is assigned to a user or organization.
        user_limit (int): The number of users that can be assigned to this subscription. If the user limit is 0, there is no limit. This is used to enforce limits on the number of users that can be assigned to a subscription. If the limit is reached, no more users can be assigned to their projects until some are unassigned.
    """

    individual_subscription_type = models.ForeignKey('IndividualSubscriptionType', on_delete=models.CASCADE, blank=True, null=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="")
    is_active = models.BooleanField(default=True)
    term_length_days = models.IntegerField(default=30)
    user_limit = models.IntegerField(default=1)


class IndividualSubscriptionTypeManager(models.Manager):
    def initialize_subscriptions(self) -> None:
        """
        Initializes individual subscription types.
        """

        # We force specific UUIDs here to ensure consistency across all installations.
        built_in_individual_subscription_types = [
            ('2f42c42f-e171-4022-a786-d5f37d277943', 'Trial', 'Trial', True, 7, 1),
            ('79a9026d-968e-4670-81bb-d3fbceb92a19', 'Free', 'Free', True, 30, 1),
            ('0f367241-83eb-448b-a993-f213a65f6dc7', 'Standard', 'Standard', True, 30, 5),
            ('653091cc-03e2-41d1-8c96-c3bd1aae17a0', 'Premium', 'Premium', True, 30, 10),
            ]
        system_user = core_user_models.CoreUser.objects.get_or_create_system_user()

        individual_subscription_types = self.all().values_list('id', flat=True)
        for subscription_id, name, description, is_active, term_length_days, user_limit in built_in_individual_subscription_types:
            if uuid.UUID(subscription_id) not in individual_subscription_types:
                individual_subscription_type_data = IndividualSubscriptionTypeData.objects.create(
                    created_by=system_user,
                    name=name, description=description,
                    is_active=is_active,
                    term_length_days=term_length_days,
                    user_limit=user_limit
                    )
                individual_subscription_type = self.create(id=subscription_id, created_by=system_user, current=individual_subscription_type_data)
                individual_subscription_type_data.individual_subscription_type = individual_subscription_type
                individual_subscription_type_data.save()
            else:
                individual_subscription_type = self.get(id=subscription_id)
                individual_subscription_type_data = IndividualSubscriptionTypeData.objects.create(
                    created_by=system_user,
                    individual_subscription_type=individual_subscription_type,
                    name=name, description=description,
                    is_active=is_active,
                    term_length_days=term_length_days,
                    user_limit=user_limit
                    )
                individual_subscription_type.current = individual_subscription_type_data
                individual_subscription_type.save()


class IndividualSubscriptionTypeActiveManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().select_related('current').filter(deleted=None).filter(current__is_active=True)


class IndividualSubscriptionType(core_models.CoreModel):
    """
    An Individual Subscription Type. Not to be used on Organizations. The _real_ information about a subscription is stored in `current` as IndividualSubscriptionTypeData.

    Parameters:
        current (IndividualSubscriptionTypeData): The data for this IndividualSubscriptionType.
    """

    objects = IndividualSubscriptionTypeManager()
    active_objects = IndividualSubscriptionTypeActiveManager()

    current = models.OneToOneField(IndividualSubscriptionTypeData, on_delete=models.CASCADE)

    def __str__(self):
        return self.current.name


class IndividualSubscriptionActiveManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().select_related('current').filter(deleted=None)


class IndividualSubscriptionData(core_models.CoreModel):
    """
    Contains data about a subscription assigned to a user.

    Parameters:
        individual_subscription (IndividualSubscription): The Individual Subscription that this data is associated with. This is used to link the subscription data to the subscription. When a subscription is assigned to a user, a new IndividualSubscriptionData is created with the expiration date calculated based on the term length of the subscription type and the expired field set to False. When a subscription expires, a new IndividualSubscriptionData is created with the expired field set to True and the expiration date set to the date and time when the subscription expired. The current field of the IndividualSubscription is then updated to point to the new IndividualSubscriptionData.
        individual_subscription_type (IndividualSubscriptionType): The type of the subscription. This is used to determine the term length and user limit of the subscription. The term length is used to calculate the expiration date of the subscription when it is assigned to a user. The user limit is used to enforce limits on the number of users that can be assigned to a subscription. If a subscription has expired, no more users can be assigned to their projects until some are unassigned.
        expiration_date (datetime): The date and time when the subscription expires. This is calculated based on the term length of the subscription type when the subscription is assigned to the user. If the term length is 0, this field is not used and the subscription does not expire.
        expired (bool): Whether the subscription has expired or not. This is used to enforce limits on the number of users that can be assigned to a subscription. If a subscription has expired, no more users can be assigned to their projects until some are unassigned.
    """

    core_user = models.ForeignKey(core_user_models.CoreUser, on_delete=models.CASCADE)
    individual_subscription_type = models.ForeignKey(IndividualSubscriptionType, on_delete=models.CASCADE)
    individual_subscription = models.ForeignKey('IndividualSubscription', on_delete=models.CASCADE, blank=True, null=True)  # Needs to be nullable to allow for the creation of IndividualSubscriptionData before the IndividualSubscription is created. The subscription field is then updated to point to the correct IndividualSubscription after it is created.

    expiration_date = models.DateTimeField(blank=True, null=True)
    expired = models.BooleanField(default=False)


class IndividualSubscription(core_models.CoreModel):
    """
    A User subscription. Not to be used on Organizations.

    Parameters:
        current (IndividualSubscriptionData): The current data of the Individual Subscription. This is used to store the expiration date and whether the subscription has expired or not. When a subscription is assigned to a user, a new IndividualSubscriptionData is created with the expiration date calculated based on the term length of the subscription type and the expired field set to False. When a subscription expires, a new IndividualSubscriptionData is created with the expired field set to True and the expiration date set to the date and time when the subscription expired. The current field is then updated to point to the new IndividualSubscriptionData.
    """

    active_objects = IndividualSubscriptionActiveManager()

    current = models.OneToOneField(IndividualSubscriptionData, on_delete=models.CASCADE)

    def set_expiration_date(self, user_id=None, subscription_type=None):
        if not user_id:
            # Subscription expiration setting can be a system task, default to that user.
            user_id = core_user_models.CoreUser.objects.get_or_create_system_user().id
        if not subscription_type:
            subscription_type = self.current.individual_subscription_type
        individual_subscription_data = IndividualSubscriptionData.objects.create(
            created_by_id=user_id,
            core_user_id=self.current.core_user_id,
            individual_subscription=self,
            individual_subscription_type_id=subscription_type.id,
            expiration_date=timezone.now() + timezone.timedelta(days=subscription_type.current.term_length_days),
            expired=False
            )
        self.current = individual_subscription_data
        self.save()

    def expire_subscription(self, user_id=None, subscription_type=None):
        if not user_id:
            # Subscription expiration setting can be a system task, default to that user.
            user_id = core_user_models.CoreUser.objects.get_or_create_system_user().id
        if not subscription_type:
            subscription_type = self.current.individual_subscription_type
        if self.current and not self.current.expired:
            individual_subscription_data = IndividualSubscriptionData.objects.create(
                created_by_id=user_id,
                core_user_id=self.current.core_user_id,
                individual_subscription=self,
                individual_subscription_type_id=subscription_type.id,
                expiration_date=timezone.now() - timezone.timedelta(days=1),
                expired=True
                )
            self.current = individual_subscription_data
            self.save()

    def __str__(self):
        return f"{self.current.individual_subscription_type}, expires {self.current.expiration_date if self.current.expiration_date else 'never'}"
