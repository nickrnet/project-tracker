from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.forms.models import model_to_dict

from frontend.forms.core.organization import organization_form as organization_form
from core.models import user as core_user_models
from core.models import organization as core_organization_models


@login_required
def organization(request, organization_id=None):
    try:
        logged_in_user = core_user_models.CoreUser.objects.get(user__username=request.user)
    except core_user_models.CoreUser.DoesNotExist:
        return redirect("logout")

    if request.method == "POST":
        received_organization_data_form = organization_form.OrganizationDataForm(request.POST, request.FILES)
        if received_organization_data_form.is_valid():
            organization = core_organization_models.Organization.objects.get(pk=organization_id)
            # TODO: Move these to the Organization
            # received_organization_data_form.cleaned_data.pop('members')
            # received_organization_data_form.cleaned_data.pop('repositories')
            # received_organization_data_form.cleaned_data.pop('projects')
            if received_organization_data_form.cleaned_data['number_users_allowed'] is None:
                received_organization_data_form.cleaned_data.pop('number_users_allowed')
            organization_data = core_organization_models.OrganizationData(**received_organization_data_form.cleaned_data)
            organization_data.created_by = logged_in_user
            organization_data.save()

            organization.current = organization_data
            organization.save()
            messages.success(request, ('Your organization was successfully updated!'))
        else:
            messages.error(request, 'Error saving organization.')

        return redirect("organization", organization_id=organization.id)

    try:
        organization = core_organization_models.Organization.objects.get(pk=organization_id)
        organization_data_form = organization_form.OrganizationDataForm(model_to_dict(organization.current))
        return render(request=request, template_name="core/organization/organization_template.html", context={
            'logged_in_user': logged_in_user,
            'organization_data_form': organization_data_form
        })
    except core_organization_models.Organization.DoesNotExist:
        messages.error(request, 'The specified Organization does not exist. Create it and try again.')
        return redirect("new_organization")
