from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect

from frontend.forms.git_repository import git_repository_form
from frontend.forms.project import project_form
from core.models import user as core_user_models
from project.models import git_repository as git_repository_models
from project.models import project as project_models


@login_required
def project(request, project_id=None):
    try:
        logged_in_user = core_user_models.CoreUser.objects.get(user__username=request.user)
    except core_user_models.CoreUser.DoesNotExist:
        return redirect("logout")

    if request.method == "POST":
        received_project_data_form = project_form.ProjectDataForm(request.POST, request.FILES)
        if received_project_data_form.is_valid():
            try:
                project = logged_in_user.project_created_by.get(id=project_id)
                # TODO: Create a new git repository if needed
                received_project_data_form.cleaned_data["git_repository_id"] = received_project_data_form.cleaned_data.get("git_repository")
                received_project_data_form.cleaned_data.pop("git_repository")
                received_project_data_form.cleaned_data["created_by_id"] = str(logged_in_user.id)
                project_data = project_models.ProjectData.objects.create(**received_project_data_form.cleaned_data)
                project_data.save()
                project.current = project_data
                project.save()
                messages.success(request, ('Your project was successfully updated!'))
                return redirect("project", project_id=project_id)
            except project_models.Project.DoesNotExist:
                messages.error(request, "The specified Project does not exist. Create it and try again.")
                return redirect("new_project")
            except git_repository_models.GitRepository.DoesNotExist:
                messages.error(request, "The specified Git Repository for your Project does not exist. Create it and try again.")
                return redirect("new_git_repository")
        else:
            messages.error(request, 'Error saving project.')
            return render(request, "project/new_project_template.html")

    form = project_form.ProjectDataForm()
    try:
        project = logged_in_user.project_created_by.get(id=project_id)
        form = project_form.ProjectDataForm(model_to_dict(project.current))
        git_repo_form = git_repository_form.GitRepositoryDataForm()
        git_repositories = logged_in_user.gitrepository_created_by.all()
    except project_models.Project.DoesNotExist:
        messages.error(request, 'The specified Project does not exist. Create it and try again.')
        return redirect("new_project")

    return render(request=request, template_name="project/project_template.html", context={
        'logged_in_user': logged_in_user,
        'project_form': form,
        'git_repository_id': str(project.current.git_repository_id),
        'git_repository_form': git_repo_form,
        'repositories': git_repositories,
    })
