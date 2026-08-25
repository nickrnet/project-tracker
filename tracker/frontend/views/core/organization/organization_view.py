from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View

from frontend.forms.core.organization import organization_form as organization_form
from core.models import user as core_user_models
from core.models import organization as core_organization_models


class OrganizationView(LoginRequiredMixin, View):
    def get(self, request, organization_id=None):
        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)

        try:
            organization = core_organization_models.Organization.active_objects.get(pk=organization_id)
            return render(
                request=request,
                template_name="core/organization/organization_template.html",
                context={
                    'logged_in_user': logged_in_user,
                    'organization': organization,
                    'projects': organization.projects.all(),
                    'members': organization.members.all(),
                    'organization_invites': organization.member_invites.all().exclude(current__status='ACCEPTED'),
                    }
                )
        except core_organization_models.Organization.DoesNotExist:
            messages.error(request, 'The specified organization does not exist. Create it and try again.')
            return redirect("organizations")

    def post(self, request, organization_id):
        received_organization_data_form = organization_form.OrganizationDataForm(request.POST, request.FILES)
        organization = core_organization_models.Organization.active_objects.get(pk=organization_id)
        if received_organization_data_form.is_valid():
            logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)
            organization_form_data = received_organization_data_form.cleaned_data.copy()
            organization_data = core_organization_models.OrganizationData(**organization_form_data)
            organization_data.created_by = logged_in_user
            organization_data.created_on = timezone.now()
            organization_data.organization = organization
            organization_data.save()

            organization.current = organization_data
            organization.save()
            messages.success(request, ('Organization successfully updated!'))
        else:
            messages.error(request, 'Error updating organization.')

        return redirect("organization", organization_id=organization.id)
