from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect

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


@login_required
def git_repository(request, git_repository_id=None):
    try:
        logged_in_user = core_user_models.CoreUser.objects.get(user__username=request.user)
    except core_user_models.CoreUser.DoesNotExist:
        return redirect("logout")

    if request.method == "POST":
        received_git_repository_form = git_repository_form.GitRepositoryDataForm(
            request.POST, request.FILES)
        if received_git_repository_form.is_valid():
            git_repository = logged_in_user.git_repositories.get(pk=git_repository_id)
            git_repository_data = git_repository_models.GitRepositoryData(
                created_by=logged_in_user,
                name=received_git_repository_form.cleaned_data.get('name'),
                description=received_git_repository_form.cleaned_data.get('description'),
                url=received_git_repository_form.cleaned_data.get('url'),
                )
            git_repository_data.save()
            git_repository.current = git_repository_data
            git_repository.save()
            messages.info(request, 'Your Git Repository was successfully updated!')
        else:
            messages.error(request, 'Error saving git repository.')

        return redirect("git_repository", git_repository_id=git_repository_id)

    form = git_repository_form.GitRepositoryDataForm()

    try:
        git_repository = logged_in_user.list_git_repositories().get(id=git_repository_id)
        form = git_repository_form.GitRepositoryDataForm(model_to_dict(git_repository.current))
        valid_url = validate_url(git_repository.current.url)
    except git_repository_models.GitRepository.DoesNotExist:
        messages.error(
            request, 'The specified Git Repository does not exist. Create it and try again.')
        return redirect("new_git_repository")

    return render(
        request=request,
        template_name="project/git_repository/git_repository_modal.html",
        context={
            'logged_in_user': logged_in_user,
            'git_repository_form': form,
            'git_repository': git_repository,
            'project': git_repository.projectdata_set.first(),
            'organization': git_repository.organizationgitrepositories_set.first(),
            'valid_url': valid_url,
            }
        )
