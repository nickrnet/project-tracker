from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from core.models import user as core_user_models


class OrganizationView(LoginRequiredMixin, View):
    def get(self, request):
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
