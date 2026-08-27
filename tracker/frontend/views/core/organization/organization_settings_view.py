from importlib import resources

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View

from frontend.forms.core.organization import organization_form as organization_form
from core.models import user as core_user_models
from core.models import organization as core_organization_models


class OrganizationSettingsView(LoginRequiredMixin, View):
    def get(self, request, organization_id):
        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)
        timezone_choices = core_user_models.TIMEZONE_CHOICES
        with resources.files('tzdata.zoneinfo').joinpath('iso3166.tab').open('r') as f:
            country_names = dict(
                line.rstrip('\n').split('\t', 1)
                for line in f
                if not line.startswith('#')
                )
            country_names = sorted(country_names.items(), key=lambda x: x[1])

        try:
            organization = core_organization_models.Organization.active_objects.get(pk=organization_id)
            return render(
                request=request,
                template_name="core/organization/organization_settings.html",
                context={
                    'logged_in_user': logged_in_user,
                    'organization': organization,
                    'organization_id': organization.id,
                    'timezone_choices': timezone_choices,
                    'country_names': country_names,
                    }
                )
        except core_organization_models.Organization.DoesNotExist:
            messages.error(request, "The specified organization does not exist.")
            return redirect("organizations")

    def post(self, request, organization_id):
        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)
        received_organization_data_form = organization_form.OrganizationDataForm(request.POST, request.FILES)
        try:
            if received_organization_data_form.is_valid():
                organization = core_organization_models.Organization.active_objects.get(pk=organization_id)
                organization_form_data = received_organization_data_form.cleaned_data.copy()
                organization_data = core_organization_models.OrganizationData(**organization_form_data)
                organization_data.created_by = logged_in_user
                organization_data.created_on = timezone.now()
                organization_data.organization = organization
                organization_data.save()

                organization.current = organization_data
                organization.save()
                messages.success(request, ('Your organization was successfully updated.'))
                return redirect("organization", organization_id=organization_id)
            else:
                messages.error(request, 'Error updating organization.')
                return redirect("organizations")
        except core_organization_models.Organization.DoesNotExist:
            messages.error(request, "The specified organization does not exist.")
            return redirect("organizations")
