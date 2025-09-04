from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from frontend.forms.core.organization import organization_form as organization_form
from core.models import user as core_user_models
from core.models import organization as core_organization_models


def handle_post(request, logged_in_user, organization=None):
    received_organization_data_form = organization_form.OrganizationDataForm(request.POST, request.FILES)
    if received_organization_data_form.is_valid():
        # TODO: Normal users can't set this, but leave for now
        if received_organization_data_form.cleaned_data['number_users_allowed'] is None:
            received_organization_data_form.cleaned_data.pop('number_users_allowed')
        organization_data = core_organization_models.OrganizationData(**received_organization_data_form.cleaned_data)
        organization_data.created_by = logged_in_user
        organization_data.save()

        organization.current = organization_data
        organization.save()
        messages.success(request, ('Your organization was successfully updated!'))
    else:
        messages.error(request, 'Error updating organization.')

    return redirect("organization", organization_id=organization.id)


@login_required
def organization(request, organization_id=None):
    logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)

    try:
        organization = core_organization_models.Organization.active_objects.get(pk=organization_id)

        if request.method == "POST":
            return handle_post(request, logged_in_user, organization)

        return render(
            request=request,
            template_name="core/organization/organization_template.html",
            context={
                'logged_in_user': logged_in_user,
                'organization': organization,
                'projects': organization.projects.all(),
                'members': organization.members.all()
                }
            )
    except core_organization_models.Organization.DoesNotExist:
        messages.error(request, 'The specified Organization does not exist. Create it and try again.')
        return redirect("organizations")
