from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from core.models import user as core_user_models


class IssuesView(LoginRequiredMixin, View):
    def get(self, request):
        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)

        issues = logged_in_user.list_issues()

        return render(
            request=request,
            template_name="project/issue/issues_template.html",
            context={
                'logged_in_user': logged_in_user,
                'issues': issues,
                }
            )
