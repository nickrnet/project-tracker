from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect

from frontend.util import project as project_utils
from frontend.forms.project.git_repository import new_git_repository_form as new_git_repository_form
from frontend.forms.project.project import project_form
from core.models import user as core_user_models
from project.models import git_repository as git_repository_models


def handle_post(request, logged_in_user, project):
    received_new_git_repository_form = new_git_repository_form.NewGitRepositoryForm(request.POST, request.FILES)

    if received_new_git_repository_form.is_valid():
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

        project.git_repositories.add(git_repository)

        messages.success(request, ('Your git repository was successfully added!'))
    else:
        project = project_utils.get_project_by_uuid_or_label(logged_in_user, str(project.id))
        messages.error(request, 'Error saving git repository.')

    project_dict = model_to_dict(project.current)
    if project.label:
        project_dict['label'] = project.label.current.label
    form = project_form.ProjectDataForm(project_dict)
    repositories = project.git_repositories.all()
    return render(
        request=request,
        template_name="project/project/project_settings_modal.html",
        context={
            'logged_in_user': logged_in_user,
            'project': project,
            'project_id': str(project.id),
            'project_form': form,
            'git_repositories': repositories,
            },
        )


@login_required
def new_git_repository(request, project_id):
    logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)

    # Check if user can access project
    project = project_utils.get_project_by_uuid_or_label(logged_in_user, project_id)
    if project is None:
        messages.error(request, 'The specified Project does not exist or you do not have permission to see it. Try to create it, or contact the organization administrator.')
        return redirect("projects")

    if request.method == "POST":
        return handle_post(request, logged_in_user, project)

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
