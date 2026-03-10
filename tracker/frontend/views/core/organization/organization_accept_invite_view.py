from django.contrib import messages
from django.shortcuts import redirect, render

from core.models import user as core_user_models
from core.models import organization_invites as core_organization_invites_models


def handle_post(request, logged_in_user, invite):
    if request.POST.get('response') == 'declined':
        invite.current.status = 'DECLINED'
        invite.current.save()
        messages.info(request, "You have declined the organization invite.")
        return redirect("projects")
    else:
        organization = invite.current.organization
        if logged_in_user not in organization.members.all():
            organization.members.add(logged_in_user)
            organization.save()
            invite.current.status = 'ACCEPTED'
            invite.current.save()
            messages.success(request, f"You have successfully joined the organization {organization.current.name}!")
        else:
            messages.info(request, "You are already a member of this organization.")

        return redirect("projects")


def accept_organization_invite(request, invite_id):
    """
    View to accept an organization invite.
    """

    try:
        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)
    except core_user_models.CoreUser.DoesNotExist:
        logged_in_user = None

    try:
        invite = core_organization_invites_models.OrganizationInvite.active_objects.get(pk=invite_id)
    except core_organization_invites_models.OrganizationInvite.DoesNotExist:
        messages.error(request, 'The specified invite is invalid.')
        if logged_in_user:
            return redirect("organizations")
        else:
            return redirect("login")

    # TODO: Check that the user is the recipient of the invite
    if logged_in_user and invite.current.email != logged_in_user.user.email:
        messages.error(request, "The specified invite is invalid.")
        return redirect("organizations")

    if invite.current.status != 'PENDING':
        messages.error(request, "This invite is no longer valid.")
        if logged_in_user:
            return redirect("organizations")
        else:
            return redirect("login")

    if request.method == "POST":
        return handle_post(request, logged_in_user, invite)

    return render(
        request=request,
        template_name="core/organization/accept_organization_invite.html",
        context={
            'logged_in_user': logged_in_user,
            'invite': invite,
            'organization': invite.current.organization,
            'next_url': request.build_absolute_uri(),
            },
        )
