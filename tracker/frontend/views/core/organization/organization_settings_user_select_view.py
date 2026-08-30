from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

from core.models import user as core_user_models
from core.models import organization as core_organization_models


class OrganizationUserSelectView(LoginRequiredMixin, View):
    def handle_user_selection(self, request, organization, selected_user_ids):
        updated_users = False
        # TODO: Roles/permissions per user
        if len(selected_user_ids) > 0:
            # Make sure each user received has an account
            for user_id in selected_user_ids:
                try:
                    user = core_user_models.CoreUser.active_objects.get(pk=user_id)
                    if not organization.members.filter(pk=user.id).exists():
                        organization.members.add(user)
                        updated_users = True
                except core_user_models.CoreUser.DoesNotExist:
                    messages.error(request, 'Could not add ' + str(user_id) + ' to organization users.')
                    continue
            for user in organization.members.all():
                # Remove any users that were not selected
                if str(user.id) not in selected_user_ids:
                    organization.members.remove(user)
                    updated_users = True
        else:
            organization.members.clear()
            updated_users = True

        if updated_users:
            organization.save()
            messages.success(request, 'Organization users updated successfully!')

    def get(self, request, organization_id):
        """
        Displays the User Select Modal when a user clicks it in the Organization Settings modal.
        """

        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)
        try:
            organization = core_organization_models.Organization.active_objects.get(pk=organization_id)
        except core_organization_models.Organization.DoesNotExist:
            messages.error(request, "The specified organization does not exist.")
            return redirect("organizations")

        # TODO: Roles/permissions per user to make sure user can actually see the organization users
        # Make sure logged in user is a part of the Organization
        if not organization.members.filter(pk=logged_in_user.id).exists():
            messages.error(request, "The specified organization does not exist.")
            return redirect("organizations")

        # Get available users (organization members + project users) and exclude
        # any users already assigned to this project.
        available_users = logged_in_user.list_users().exclude(
            pk__in=organization.members.all().values_list('pk', flat=True)
            )

        return render(
            request=request,
            template_name="core/organization/organization_settings_user_select_modal.html",
            context={
                'logged_in_user': logged_in_user,
                'organization': organization,
                'current_users': organization.members.all(),
                'available_users': available_users,
                }
            )

    def post(self, request, organization_id):
        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)
        try:
            organization = core_organization_models.Organization.active_objects.get(pk=organization_id)
        except core_organization_models.Organization.DoesNotExist:
            messages.error(request, "The specified organization does not exist.")
            return redirect("organizations")

        self.handle_user_selection(request, organization, request.POST.getlist('current_users'))

        return render(
            request=request,
            template_name="core/organization/organization_users_table.html",
            context={
                'logged_in_user': logged_in_user,
                'organization': organization,
                'projects': organization.projects.all(),
                'members': organization.members.all(),
                }
            )
