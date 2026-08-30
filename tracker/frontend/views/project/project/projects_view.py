from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from core.models import user as core_user_models


class ProjectsView(LoginRequiredMixin, View):
    def get(self, request):
        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)

        projects = logged_in_user.list_projects()

        return render(
            request=request,
            template_name="project/project/projects_template.html",
            context={
                'logged_in_user': logged_in_user,
                'projects': projects,
                }
            )
