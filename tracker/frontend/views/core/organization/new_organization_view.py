from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from frontend.forms.core.organization import new_organization_form as new_organization_form
from core.models import organization as core_organization_models
from core.models import user as core_user_models


@login_required
def new_organization(request):
    try:
        logged_in_user = core_user_models.CoreUser.objects.get(user__username=request.user)
    except core_user_models.CoreUser.DoesNotExist:
        return redirect("logout")

    if request.method == "POST":
        received_new_organization_data_form = new_organization_form.NewOrganizationDataForm(
            request.POST, request.FILES)
        if received_new_organization_data_form.is_valid():
            # received_new_organization_data_form.cleaned_data.pop('members')  # TODO: Fix the form and memberships, repos, and projects
            # received_new_organization_data_form.cleaned_data.pop('repositories')
            # received_new_organization_data_form.cleaned_data.pop('projects')
            if received_new_organization_data_form.cleaned_data['number_users_allowed'] is None:
                received_new_organization_data_form.cleaned_data[
                    'number_users_allowed'] = received_new_organization_data_form.fields['number_users_allowed'].initial

            organization_data = core_organization_models.OrganizationData(
                **received_new_organization_data_form.cleaned_data)
            organization_data.created_by = logged_in_user
            organization_data.save()

            organization = core_organization_models.Organization.objects.create(
                created_by=logged_in_user, current=organization_data)
            organization.save()
            organization.members.add(logged_in_user)
            organization.save()

            logged_in_user.organizations.add(organization)
            logged_in_user.save()

            messages.success(request, ('Your organization was successfully added!'))
            return redirect("organization", organization_id=organization.id)
        else:
            messages.error(request, 'Error saving organization.')
            return render(
                request=request,
                template_name="core/organization/new_organization_template.html"
                )

    organization_data_form = new_organization_form.NewOrganizationDataForm()
    organizations = logged_in_user.organizationmembers_set.all()
    return render(
        request=request,
        template_name="core/organization/new_organization_template.html",
        context={
            'logged_in_user': logged_in_user,
            'new_organization_data_form': organization_data_form,
            'organizations': organizations
            }
        )
