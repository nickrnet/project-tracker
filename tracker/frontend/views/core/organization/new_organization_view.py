from importlib import resources

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone

from frontend.forms.core.organization import new_organization_form as new_organization_form
from core.models import organization as core_organization_models
from core.models import user as core_user_models


def handle_post(request, logged_in_user):
    received_new_organization_data_form = new_organization_form.NewOrganizationDataForm(request.POST, request.FILES)
    if received_new_organization_data_form.is_valid():
        # TODO: Normal users cannot set this, but leave for now
        if received_new_organization_data_form.cleaned_data['number_users_allowed'] is None:
            received_new_organization_data_form.cleaned_data['number_users_allowed'] = received_new_organization_data_form.fields['number_users_allowed'].initial

        organization_data = core_organization_models.OrganizationData(**received_new_organization_data_form.cleaned_data)
        organization_data.created_by = logged_in_user
        organization_data.created_on = timezone.now()
        organization_data.save()

        organization = core_organization_models.Organization.objects.create(created_by=logged_in_user, current=organization_data)
        organization.created_aon = timezone.now()
        organization.save()
        organization.members.add(logged_in_user)
        organization.save()

        messages.success(request, ('Your organization was successfully added!'))
        return redirect("organization", organization_id=organization.id)
    else:
        messages.error(request, 'Error saving organization.')
        return redirect("organizations")


@login_required
def new_organization(request):
    logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)

    if request.method == "POST":
        return handle_post(request, logged_in_user)

    organization_data_form = new_organization_form.NewOrganizationDataForm()
    organizations = logged_in_user.list_organizations()
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
        template_name="core/organization/new_organization_modal.html",
        context={
            'logged_in_user': logged_in_user,
            'new_organization_data_form': organization_data_form,
            'organizations': organizations,
            'timezone_choices': timezone_choices,
            'country_names': country_names,
            }
        )
