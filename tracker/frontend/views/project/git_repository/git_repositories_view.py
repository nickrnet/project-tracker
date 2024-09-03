from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from core.models import user as core_user_models
from project.models import git_repository as git_repository_models


@login_required
def git_repositories(request):
    try:
        logged_in_user = core_user_models.CoreUser.objects.get(user__username=request.user)
    except core_user_models.CoreUser.DoesNotExist:
        return redirect("logout")

    # Get unique repositories from organizations and projects
    organization_repositories = logged_in_user.organizations.values_list('repositories', flat=True)
    project_repositories = logged_in_user.projects.values_list('git_repository', flat=True)

    # Combine the user IDs and get distinct users
    repository_ids = set(organization_repositories).union(set(project_repositories))
    repositories = git_repository_models.GitRepository.objects.filter(id__in=repository_ids)

    # repositories = logged_in_user.git_repositories.all()
    return render(
        request=request,
        template_name="project/git_repository/git_repositories_template.html",
        context={
            'logged_in_user': logged_in_user,
            'repositories': repositories
        }
    )
