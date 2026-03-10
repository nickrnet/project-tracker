from django.db import models

from core.tasks.send_organization_invite import send_organization_invite_email
from core.models import core as core_models


class OrganizationInviteData(core_models.CoreModel):
    """
    Information about an organization invite.

    @param email: The email address of the person being invited.
    @param invited_by: The user who sent the invite.
    @param organization: The organization the invite is for.
    @param status: The status of the invite (Pending, Accepted, Declined, Expired).
    @param expires_on: The date and time when the invite expires.
    """

    # TODO: Should this be its own class like CustomIssueType?
    class InviteStatusChoices(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        DECLINED = 'DECLINED', 'Declined'
        EXPIRED = 'EXPIRED', 'Expired'

    email = models.EmailField(max_length=255)
    invited_by = models.ForeignKey('core.CoreUser', on_delete=models.CASCADE)
    organization = models.ForeignKey('core.Organization', on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=InviteStatusChoices.choices, default=InviteStatusChoices.PENDING)
    expires_on = models.DateTimeField(blank=True, null=True)


class OrganizationInvite(core_models.CoreModel):
    """
    An organization invite. The _real_ information about an organization invite is stored in `current` as OrganizationInviteData.

    @param current: The current data for this organization invite.
    @param send_invite_email: A method to send the invite email to the user.
    """

    current = models.ForeignKey(OrganizationInviteData, on_delete=models.CASCADE)

    def send_invite_email(self, accept_organization_invite_url):
        to_email = self.current.email
        organization = self.current.organization

        send_organization_invite_email.delay(
            to_email,
            organization.current.name,
            accept_organization_invite_url,
            )

    def __str__(self):
        # return f"{self.current.status} invite URL for {self.current.email} to join {self.current.organization.current.name} from {self.current.invited_by.user.username}: {request.build_absolute_uri( f'/accept_organization_invite/{invite.id}/')}"
        return f"{self.current.status} Invite for {self.current.email} to join {self.current.organization.current.name} from {self.current.invited_by.user.username}"
