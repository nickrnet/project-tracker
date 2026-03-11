from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from django.utils import timezone

from frontend.forms.project.git_repository import git_repository_form as git_repository_form
from core.models import user as core_user_models
from project.models import git_repository as git_repository_models


def validate_url(thing_to_validate: str) -> bool:
    validator = URLValidator()
    try:
        validator(thing_to_validate)
        return True
    except ValidationError:
        return False


def handle_post(request, logged_in_user, git_repository):
    received_git_repository_form = git_repository_form.GitRepositoryDataForm(request.POST, request.FILES)

    if received_git_repository_form.is_valid():
        git_repository_data = git_repository_models.GitRepositoryData.objects.create(
            created_by=logged_in_user,
            created_on=timezone.now(),
            name=received_git_repository_form.cleaned_data.get('name'),
            description=received_git_repository_form.cleaned_data.get('description'),
            url=received_git_repository_form.cleaned_data.get('url'),
            )
        git_repository.current = git_repository_data
        git_repository.save()
        messages.info(request, 'Your git repository was successfully updated!')
    else:
        messages.error(request, 'Error saving git repository.')

    return redirect("git_repositories")


@login_required
def git_repository(request, git_repository_id=None):
    logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)
    git_repository = logged_in_user.list_git_repositories().get(id=git_repository_id)

    if request.method == "POST":
        return handle_post(request, logged_in_user, git_repository)

    form = git_repository_form.GitRepositoryDataForm(model_to_dict(git_repository.current))
    valid_url = validate_url(git_repository.current.url)
    organizations = logged_in_user.list_organizations()
    projects = logged_in_user.list_projects()

    return render(
        request=request,
        template_name="project/git_repository/git_repository_modal.html",
        context={
            'logged_in_user': logged_in_user,
            'git_repository_form': form,
            'git_repository': git_repository,
            'project': git_repository.project_set.first(),
            'organization': git_repository.organizationgitrepositories_set.first(),
            'valid_url': valid_url,
            'organizations': organizations,
            'projects': projects,
            }
        )
