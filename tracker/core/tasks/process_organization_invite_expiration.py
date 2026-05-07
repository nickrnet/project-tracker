from celery import shared_task
import logging

from django.utils import timezone

from core.models import organization_invites as core_organization_invite_models


logger = logging.getLogger(__name__)


@shared_task
def process_organization_invite_expiration():
    """
    Processes the expiration of organization invites.
    """

    logger.info("Starting process to handle expiration of organization invites.")
    expiration_datetime = timezone.now()
    invites_to_process = core_organization_invite_models.OrganizationInvite.active_objects.filter(
        current__status='PENDING',
        current__expires_on__lt=expiration_datetime,
        )
    invites_expired = 0
    for invite in invites_to_process:
        invite_data = core_organization_invite_models.OrganizationInviteData.objects.create(
            created_by=invite.current.created_by,
            created_on=invite.current.created_on,
            email=invite.current.email,
            invited_by=invite.current.invited_by,
            organization=invite.current.organization,
            status='EXPIRED',
            expires_on=invite.current.expires_on,
            )
        invite.current = invite_data
        invite.save()
        invites_expired += 1

    if invites_expired > 0:
        logger.info(f"Expired {invites_expired} organization invites.")
    else:
        logger.info("No invites to expire.")
