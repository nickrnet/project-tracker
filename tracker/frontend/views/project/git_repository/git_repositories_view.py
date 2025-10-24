from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.models import user as core_user_models


@login_required
def git_repositories(request):
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
