from celery import shared_task
import logging

from django.utils import timezone

from core.models.user import CoreUser
from subscription.models.individual import IndividualSubscription


logger = logging.getLogger(__name__)


@shared_task
def process_individual_subscription_expiration():
    """
    Processes the expiration of individual subscriptions.
    """

    logger.info("Starting process to handle expiration of individual subscriptions.")

    now = timezone.now()
    system_user = CoreUser.objects.get_or_create_system_user()
    expired_subscriptions = IndividualSubscription.active_objects.filter(current__expiration_date__lt=now, current__expired=False)

    for subscription in expired_subscriptions:
        subscription.expire_subscription(user_id=system_user.id)
        subscription.save()

    logger.info(f"Processed {len(expired_subscriptions)} expired individual subscriptions.")
