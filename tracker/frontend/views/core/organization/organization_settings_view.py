from importlib import resources

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone

from frontend.forms.core.organization import organization_form as organization_form
from core.models import user as core_user_models
from core.models import organization as core_organization_models


def handle_post(request, logged_in_user, organization_id=None):
    received_organization_data_form = organization_form.OrganizationDataForm(request.POST, request.FILES)
    if received_organization_data_form.is_valid():
        organization = core_organization_models.Organization.active_objects.get(pk=organization_id)
        # TODO: This isn't allowed by normal users, but leave for now
        if received_organization_data_form.cleaned_data['number_users_allowed'] is None:
            received_organization_data_form.cleaned_data.pop('number_users_allowed')
        organization_data = core_organization_models.OrganizationData(
            **received_organization_data_form.cleaned_data)
        organization_data.created_by = logged_in_user
        organization_data.created_on = timezone.now()
        organization_data.save()

        organization.current = organization_data
        organization.save()
        messages.success(request, ('Your organization was successfully updated!'))
    else:
        messages.error(request, 'Error updating organization.')

    return redirect("organization", organization_id=organization_id)


@login_required
def organization_settings(request, organization_id=None):
    logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)

    if request.method == "POST":
        return handle_post(request, logged_in_user, organization_id)

    organization = core_organization_models.Organization.active_objects.get(pk=organization_id)
    timezone_choices = core_user_models.TIMEZONE_CHOICES
    with resources.files('tzdata.zoneinfo').joinpath('iso3166.tab').open('r') as f:
        country_names = dict(
            line.rstrip('\n').split('\t', 1)
            for line in f
            if not line.startswith('#')
            )
        country_names = sorted(country_names.items(), key=lambda x: x[1])

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
