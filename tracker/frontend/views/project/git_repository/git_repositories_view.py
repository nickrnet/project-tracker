from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from core.models import user as core_user_models


@login_required
def git_repositories(request):
    try:
        logged_in_user = core_user_models.CoreUser.objects.get(user__username=request.user)
    except core_user_models.CoreUser.DoesNotExist:
        return redirect("logout")

    repositories = logged_in_user.list_git_repositories()

    return render(
        request=request,
        template_name="project/git_repository/git_repositories_template.html",
        context={
            'logged_in_user': logged_in_user,
            'git_repositories': repositories,
        }
    )
