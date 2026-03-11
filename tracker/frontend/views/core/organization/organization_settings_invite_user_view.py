from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone

from core.models import user as core_user_models
from core.models import organization as core_organization_models
from core.models import organization_invites as core_organization_invites_models


def handle_post(request, logged_in_user, organization):
    email = request.POST.get('email')
    if not email:
        messages.error(request, "Email is required to send an invite.")
        return render(
            request=request,
            template_name="core/organization/organization_invites_table.html",
            context={
                'logged_in_user': logged_in_user,
                'organization': organization,
                'projects': organization.projects.all(),
                'members': organization.members.all(),
                'organization_invites': organization.member_invites.all().exclude(current__status="Pending").exclude(current__status="Declined"),
                }
            )

    if organization.members.filter(current__email=email).exists():
        messages.error(request, "This user is already a member of your organization.")
        return render(
            request=request,
            template_name="core/organization/organization_invites_table.html",
            context={
                'logged_in_user': logged_in_user,
                'organization': organization,
                'projects': organization.projects.all(),
                'members': organization.members.all(),
                'organization_invites': organization.member_invites.all().exclude(current__status="Pending").exclude(current__status="Declined"),
                }
            )

    invite_data = core_organization_invites_models.OrganizationInviteData.objects.create(
        created_by=logged_in_user,
        created_on=timezone.now(),
        email=email,
        invited_by=logged_in_user,
        organization=organization,
        status='PENDING',
        expires_on=timezone.now() + timezone.timedelta(days=7),
        )
    invite = core_organization_invites_models.OrganizationInvite.objects.create(
        created_by=logged_in_user,
        created_on=timezone.now(),
        current=invite_data,
        )
    organization.member_invites.add(invite)
    organization.save()

    accept_organization_invite_url = request.build_absolute_uri(f"/accept_organization_invite/{invite.id}/")
    # This is useful if mail server bits aren't set up
    # print("Accept URL:", accept_organization_invite_url)
    invite.send_invite_email(accept_organization_invite_url)
    messages.success(request, f"Invite sent to {email}!")

    return render(
        request=request,
        template_name="core/organization/organization_invites_table.html",
        context={
            'logged_in_user': logged_in_user,
            'organization': organization,
            'projects': organization.projects.all(),
            'members': organization.members.all(),
            'organization_invites': organization.member_invites.all().exclude(current__status="Pending").exclude(current__status="Declined"),
            }
        )


@login_required
def invite_user(request, organization_id):
    """
    Displays the Invite User Modal when a user clicks it in the Organization Settings modal.
    """

    logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)
    try:
        organization = core_organization_models.Organization.active_objects.get(pk=organization_id)
    except core_organization_models.Organization.DoesNotExist:
        messages.error(request, "The specified organization does not exist. Create it and try again.")
        return redirect("organizations")

    # TODO: Roles/permissions per user
    # Make sure logged in user is a part of the Organization
    if not organization.members.filter(pk=logged_in_user.id).exists():
        messages.error(request, "The specified organization does not exist. Create it and try again.")
        return redirect("organizations")

    if request.method == "POST":
        return handle_post(request, logged_in_user, organization)

    # Get available users (organization members + project users) and exclude
    # any users already assigned to this project.
    available_users = logged_in_user.list_users().exclude(
        pk__in=organization.members.all().values_list('pk', flat=True)
        )

    return render(
        request=request,
        template_name="core/organization/organization_settings_invite_user_modal.html",
        context={
            'logged_in_user': logged_in_user,
            'organization': organization,
            'current_users': organization.members.all(),
            'available_users': available_users,
            }
        )
