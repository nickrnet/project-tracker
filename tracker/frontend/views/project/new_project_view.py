from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone

from frontend.forms.git_repository import new_git_repository_form
from frontend.forms.project import new_project_form
from core.models import user as core_user_models
from project.models import project as project_models


@login_required
def new_project(request):
    try:
        logged_in_user = core_user_models.CoreUser.objects.get(user__username=request.user)
    except core_user_models.CoreUser.DoesNotExist:
        return redirect("logout")

    if request.method == "POST":
        received_new_project_form = new_project_form.NewProjectForm(request.POST, request.FILES)
        if received_new_project_form.is_valid():
            # TODO: Create a new git repo when creating a new project if specified
            if received_new_project_form.cleaned_data.get("git_repository", None):
                git_repository = logged_in_user.gitrepository_created_by.get(id=received_new_project_form.cleaned_data.get("git_repository"))
            else:
                git_repository = None
            start_date = received_new_project_form.cleaned_data.get("start_date") if received_new_project_form.cleaned_data.get("start_date") else timezone.now()

            project_data = project_models.ProjectData.objects.create(
                created_by=logged_in_user,
                name=received_new_project_form.cleaned_data.get("name"),
                description=received_new_project_form.cleaned_data.get("description"),
                is_active=received_new_project_form.cleaned_data.get("is_active"),
                is_private=received_new_project_form.cleaned_data.get("is_private"),
                start_date=start_date,
                end_date=received_new_project_form.cleaned_data.get("end_date"),
                git_repository=git_repository,
            )
            project_data.save()
            project_data.users.add(logged_in_user)
            project_data.save()
            project = project_models.Project.objects.create(current=project_data, created_by=logged_in_user)
            messages.success(request, ('Your project was successfully added!'))
            return redirect("project", project_id=project.id)
        else:
            messages.error(request, 'Error saving project.')
            return redirect("new_project")

    project_form = new_project_form.NewProjectForm()
    git_repository_form = new_git_repository_form.NewGitRepositoryDataForm()
    projects = logged_in_user.project_created_by.all()
    git_repositories = logged_in_user.gitrepository_created_by.all()

    return render(request=request, template_name="project/new_project_template.html", context={
        'logged_in_user': logged_in_user,
        'new_project_form': project_form,
        'projects': projects,
        'git_repository_form': git_repository_form,
        'repositories': git_repositories,
    })
