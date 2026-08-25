from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from core.models import user as core_user_models


class GitRepositoriesView(LoginRequiredMixin, View):
    def get(self, request):
        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)

        repositories = logged_in_user.list_git_repositories()

        return render(
            request=request,
            template_name="project/git_repository/git_repositories_template.html",
            context={
                'logged_in_user': logged_in_user,
                'git_repositories': repositories,
                }
            )
