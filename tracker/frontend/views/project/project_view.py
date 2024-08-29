import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect

from core.models import user as core_user_models
from frontend.forms.git_repository import git_repository_form
from frontend.forms.project import project_form
from project.models import project as project_models


def handle_post(request, project_id, logged_in_user):
    received_project_data_form = project_form.ProjectDataForm(request.POST, request.FILES)
    if received_project_data_form.is_valid():
        try:
            project = logged_in_user.project_set.get(id=project_id)
            project_data_form = received_project_data_form.cleaned_data.copy()
            # TODO: Create a new git repository if needed
            project_data_form.pop("git_repository")
            project_data_form["created_by_id"] = str(logged_in_user.id)
            project_data = project_models.ProjectData.objects.create(**project_data_form)
            project_data.save()
            project.current = project_data
            project.save()
            messages.success(request, ('Your project was successfully updated!'))
            return redirect("project", project_id=project_id)
        except project_models.Project.DoesNotExist:
            messages.error(request, "The specified Project does not exist. Create it and try again.")
            return redirect("new_project")
    else:
        messages.error(request, 'Error saving project.')
        return render(request, "project/new_project_template.html")


@login_required
def project(request, project_id=None):
    try:
        logged_in_user = core_user_models.CoreUser.objects.get(user__username=request.user)
    except core_user_models.CoreUser.DoesNotExist:
        return redirect("logout")

    if request.method == "POST":
        handle_post(request, project_id, logged_in_user)

    try:
        # TODO: Check all projects the user has access to including other organizations and other users' projects in both the try and except blocks
        project_uuid = uuid.UUID(str(project_id))
        project = logged_in_user.project_set.get(id=project_uuid)
    except ValueError:
        project = logged_in_user.project_set.get(label=project_id)
    except project_models.Project.DoesNotExist:
        messages.error(request, 'The specified Project does not exist. Create it and try again.')
        return redirect("new_project")

    form = project_form.ProjectDataForm(model_to_dict(project.current))
    git_repo_form = git_repository_form.GitRepositoryDataForm()
    # TODO: Use all git repositories the user has access to, including other organizations and projects
    git_repositories = logged_in_user.git_repositories.all()

    return render(request=request, template_name="project/project_template.html", context={
        'logged_in_user': logged_in_user,
        'project_form': form,
        'git_repository_form': git_repo_form,
        'repositories': git_repositories,
    })
