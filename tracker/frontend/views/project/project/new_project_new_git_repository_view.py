import uuid

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from frontend.forms.project.git_repository import new_git_repository_form as new_git_repository_form
from core.models import user as core_user_models
from project.models import git_repository as git_repository_models
from project.models import project as project_models


def get_project(logged_in_user, project_id):
    try:
        project_uuid = uuid.UUID(str(project_id))
        return logged_in_user.list_projects().get(id=project_uuid)
    except ValueError:
        return logged_in_user.list_projects().filter(label__current__name__name=project_id).first()


def update_project_repositories(project, git_repository):
    if project:
        project.git_repositories.add(git_repository)
        project.save()
        if project.organizationprojects_set.count():
            organization = project.organizationprojects_set.first()
            organization.git_repositories.add(git_repository)
            organization.save()


@login_required
def new_git_repository(request, project_id=None):
    try:
        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)
    except core_user_models.CoreUser.DoesNotExist:
        return redirect("logout")

    if request.method == "POST":
        received_new_git_repository_form = new_git_repository_form.NewGitRepositoryForm(
            request.POST, request.FILES)
        if received_new_git_repository_form.is_valid():
            # We return the whole git_repositories_tab_pane, so get its required data
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
                update_project_repositories(project, git_repository)

            messages.success(request, ('Your git repository was successfully added!'))
        else:
            messages.error(request, 'Invalid data received. Please try again.')

        return redirect("new_project")

    try:
        project_uuid = uuid.UUID(str(project_id))
        project = logged_in_user.list_projects().get(id=project_uuid)
    except ValueError:
        try:
            project = logged_in_user.list_projects().filter(label__current__name__name=project_id).first()
        except project_models.Project.DoesNotExist:
            project = None

    git_repository_form = new_git_repository_form.NewGitRepositoryForm()

    return render(
        request=request,
        template_name="project/project/new_project_new_git_repository_modal.html",
        context={
            'logged_in_user': logged_in_user,
            'new_git_repository_form': git_repository_form,
            'project_id': project_id,
            }
        )
