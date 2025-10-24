from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.models import user as core_user_models


@login_required
def organizations(request):
    logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)

    organizations = logged_in_user.list_organizations()
    return render(
        request=request,
        template_name="core/organization/organizations_template.html",
        context={
            'logged_in_user': logged_in_user,
            'organizations': organizations
            }
        )
