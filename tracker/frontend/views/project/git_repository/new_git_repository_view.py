from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone

from frontend.forms.project.git_repository import new_git_repository_form as new_git_repository_form
from core.models import user as core_user_models
from project.models import git_repository as git_repository_models


def handle_post(request, logged_in_user):
    received_new_git_repository_data_form = new_git_repository_form.NewGitRepositoryForm(request.POST, request.FILES)

    if received_new_git_repository_data_form.is_valid():
        git_repository_data = git_repository_models.GitRepositoryData.objects.create(
            created_by=logged_in_user,
            created_on=timezone.now(),
            name=received_new_git_repository_data_form.cleaned_data.get('name'),
            description=received_new_git_repository_data_form.cleaned_data.get('description'),
            url=received_new_git_repository_data_form.cleaned_data.get('url'),
            )
        git_repository = git_repository_models.GitRepository.objects.create(
            created_by=logged_in_user,
            created_on=timezone.now(),
            current=git_repository_data
            )
        messages.success(request, ('Your git repository was successfully added!'))

        return redirect("git_repository", git_repository_id=git_repository.id)
    else:
        messages.error(request, 'Error saving git repository.')

        return redirect("new_git_repository")


@login_required
def new_git_repository(request):
    logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)

    if request.method == "POST":
        return handle_post(request, logged_in_user)

    git_repository_form = new_git_repository_form.NewGitRepositoryForm()
    repositories = logged_in_user.list_git_repositories()

    return render(
        request=request,
        template_name="project/git_repository/new_git_repository_modal.html",
        context={
            'logged_in_user': logged_in_user,
            'git_repository_form': git_repository_form,
            'repositories': repositories
            }
        )
