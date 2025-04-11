import uuid

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect

from frontend.forms.project.git_repository import new_git_repository_form as new_git_repository_form
from frontend.forms.project.project import project_form
from core.models import user as core_user_models
from project.models import git_repository as git_repository_models
from project.models import project as project_models


def get_project(logged_in_user, project_id):
    try:
        project_uuid = uuid.UUID(str(project_id))
        return logged_in_user.list_projects().get(id=project_uuid)
    except ValueError:
        try:
            return logged_in_user.list_projects().get(current__label__current__label=project_id)
        except project_models.Project.DoesNotExist:
            project_uuid = None


def update_project_repositories(logged_in_user, project, git_repository):
    if project:
        project.update_project_data(logged_in_user.id, {'git_repositories': [git_repository]})


def handle_post(request, logged_in_user, project_id):
    received_new_git_repository_form = new_git_repository_form.NewGitRepositoryForm(
        request.POST, request.FILES)
    if received_new_git_repository_form.is_valid():
        project_id = received_new_git_repository_form.cleaned_data.get('project_id')
        project = get_project(logged_in_user, project_id)

        git_repository_data = git_repository_models.GitRepositoryData.objects.create(
            created_by=logged_in_user,
            name=received_new_git_repository_form.cleaned_data.get('name'),
            description=received_new_git_repository_form.cleaned_data.get('description'),
            url=received_new_git_repository_form.cleaned_data.get('url'),
            )
        git_repository = git_repository_models.GitRepository.objects.create(
            created_by=logged_in_user,
            current=git_repository_data
            )
        if project:
            update_project_repositories(logged_in_user, project, git_repository)

        messages.success(request, ('Your git repository was successfully added!'))
    else:
        project = get_project(logged_in_user, project_id)
        messages.error(request, 'Invalid data received. Please try again.')

    project_dict = model_to_dict(project.current)
    if project.current.label.current.label:
        project_dict['label'] = project.current.label.current.label
    form = project_form.ProjectDataForm(project_dict)
    repositories = project.current.git_repositories.all()
    return render(
        request=request,
        template_name="project/project/project_settings.html",
        context={
            'logged_in_user': logged_in_user,
            'project': project,
            'project_id': project_id,
            'project_form': form,
            'git_repositories': repositories,
            },
        )


@login_required
def new_git_repository(request, project_id=None):
    try:
        logged_in_user = core_user_models.CoreUser.objects.get(user__username=request.user)
    except core_user_models.CoreUser.DoesNotExist:
        return redirect("logout")

    if request.method == "POST":
        return handle_post(request, logged_in_user, project_id)

    git_repository_form = new_git_repository_form.NewGitRepositoryForm()

    return render(
        request=request,
        template_name="project/project/project_settings_new_git_repository_modal.html",
        context={
            'logged_in_user': logged_in_user,
            'new_git_repository_form': git_repository_form,
            'project_id': project_id,
            }
        )
