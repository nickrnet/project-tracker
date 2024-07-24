from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from frontend.forms.organization import new_organization_form as new_organization_form
from core.models import organization as organization_models
from core.models import user as core_user_models


@login_required
def new_organization(request):
    if request.method == "POST":
        received_new_organization_data_form = new_organization_form.NewOrganizationDataForm(request.POST, request.FILES)
        if received_new_organization_data_form.is_valid():
            received_new_organization_data_form.save(request=request)
            messages.success(request, ('Your organization was successfully added!'))
        else:
            messages.error(request, 'Error saving organization.')

        return redirect(reverse("new_organization"))

    organization_data_form = new_organization_form.NewOrganizationDataForm()
    try:
        logged_in_user = core_user_models.CoreUser.objects.get(user__username=request.user)
        organizations = organization_models.Organization.active_objects.filter(members__in=[logged_in_user])
    except core_user_models.CoreUser.DoesNotExist:
        logged_in_user = None
        organizations = []

    return render(request=request, template_name="organization/new_organization_template.html", context={'logged_in_user': logged_in_user, 'new_organization_data_form': organization_data_form, 'organizations': organizations})
