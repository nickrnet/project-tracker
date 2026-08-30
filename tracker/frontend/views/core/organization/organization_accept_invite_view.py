from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from core.models import user as core_user_models
from core.models import organization_invites as core_organization_invites_models


class AcceptOrganizationInviteView(LoginRequiredMixin, View):
    def valid_invite(self, request, logged_in_user, organization_id, invite):
        not_valid = False
        if invite.current.email != logged_in_user.user.email:
            not_valid = True

        if invite.current.organization.id != organization_id:
            not_valid = True

        if invite.current.status != 'PENDING':
            not_valid = True

        if not_valid:
            messages.error(request, 'The specified invite is invalid.')
            return False

        return True

    def get(self, request, organization_id, invite_id, *args, **kwargs):
        """
        View to accept an organization invite.
        """

        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)

        try:
            invite = core_organization_invites_models.OrganizationInvite.active_objects.get(pk=invite_id)
            if not self.valid_invite(request, logged_in_user, organization_id, invite):
                messages.error(request, 'The specified invite is invalid.')
                return redirect('organizations')

            return render(
                request=request,
                template_name='core/organization/accept_organization_invite.html',
                context={
                    'logged_in_user': logged_in_user,
                    'invite': invite,
                    'organization': invite.current.organization,
                    'next_url': request.build_absolute_uri(),
                    },
                )
        except core_organization_invites_models.OrganizationInvite.DoesNotExist:
            messages.error(request, 'The specified invite is invalid.')
            return redirect('organizations')

    def post(self, request, organization_id, invite_id):
        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)
        try:
            invite = core_organization_invites_models.OrganizationInvite.active_objects.get(pk=invite_id)
            if not self.valid_invite(request, logged_in_user, organization_id, invite):
                messages.error(request, 'The specified invite is invalid.')
                return redirect('organizations')

            if request.POST.get('response') == 'declined':
                invite_data = core_organization_invites_models.OrganizationInviteData.objects.create(
                    created_by=logged_in_user,
                    organization=invite.current.organization,
                    organization_invite=invite,
                    invited_by=invite.current.invited_by,
                    email=invite.current.email,
                    status='DECLINED',
                )
                invite.current = invite_data
                invite.save()
                messages.info(request, 'You have declined the organization invite.')
                return redirect('projects')
            else:
                organization = invite.current.organization
                if organization.members.filter(current__email=logged_in_user.current.email).exists():
                    messages.info(request, 'You are already a member of this organization.')
                else:
                    invite_data = core_organization_invites_models.OrganizationInviteData.objects.create(
                        created_by=logged_in_user,
                        organization=invite.current.organization,
                        organization_invite=invite,
                        invited_by=invite.current.invited_by,
                        email=invite.current.email,
                        status='ACCEPTED',
                    )
                    invite.current = invite_data
                    invite.save()
                    organization.members.add(logged_in_user)
                    organization.save()
                    messages.success(request, f"You have successfully joined the organization {organization.current.name}.")

                return redirect('projects')
        except core_organization_invites_models.OrganizationInvite.DoesNotExist:
            messages.error(request, 'The specified invite is invalid.')
            return redirect('organizations')
