from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from django.utils import timezone

from frontend.forms.project.project import new_project_form
from core.models import user as core_user_models
from project.models import project as project_models


def handle_post(request, logged_in_user):
    received_new_project_form = new_project_form.NewProjectForm(request.POST, request.FILES)

    if received_new_project_form.is_valid():
        new_project_data = received_new_project_form.cleaned_data.copy()

        # TODO: This git repo stuff feels sus, check later
        new_project_git_repository = new_project_data.pop("git_repository", None)
        if new_project_git_repository:
            git_repositories = logged_in_user.list_git_repositories().filter(id__in=new_project_git_repository)
        else:
            git_repositories = None

        start_date = new_project_data.get("start_date") if new_project_data.get("start_date") else timezone.now()
        project_data = project_models.ProjectData.objects.create(
            created_by=logged_in_user,
            name=new_project_data.get("name"),
            description=new_project_data.get("description"),
            is_active=new_project_data.get("is_active"),
            is_private=new_project_data.get("is_private"),
            start_date=start_date,
            end_date=new_project_data.get("end_date"),
            )
        project_data.save()
        project = project_models.Project.objects.create(
            created_by=logged_in_user,
            current=project_data,
            )

        if new_project_data.get("label", None):
            project_label_name = new_project_data.pop("label")
            project_label_data = project_models.ProjectLabelData(
                created_by_id=logged_in_user.id,
                label=project_label_name,
                )
            project_label_data.save()
            project_label = project_models.ProjectLabel(
                created_by_id=logged_in_user.id,
                current=project_label_data,
                )
            project_label.save()
        else:
            project_label = None

        if project_label:
            project.label = project_label

        if git_repositories:
            for repository in git_repositories:
                project.git_repositories.add(repository)

        project.users.add(logged_in_user)
        project.current.save()
        project.save()
        messages.success(request, ('Your project was successfully added!'))
    else:
        messages.error(request, 'Error saving project.')

    return render(
        request=request,
        template_name="project/project/projects_table.html",
        context={
            'logged_in_user': logged_in_user,
            'projects': logged_in_user.list_projects(),
            }
        )


@login_required
def new_project(request):
    logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)

    if request.method == "POST":
        return handle_post(request, logged_in_user)

    project_data = project_models.ProjectData(start_date=timezone.now())
    project = project_models.Project(current=project_data)
    project_form = new_project_form.NewProjectForm()
    git_repositories = logged_in_user.list_git_repositories()
    organizations = logged_in_user.list_organizations()
    users = logged_in_user.list_users()

    return render(
        request=request,
        template_name="project/project/new_project_modal.html",
        context={
            'logged_in_user': logged_in_user,
            'new_project_form': project_form,
            'repositories': git_repositories,
            'organizations': organizations,
            'project': project,
            'users': users,
            # We use Django Forms to validate the form data, but the date selector is generic
            # HTML that is not part of the form, so we need to pass the field names here to
            # render the date selector correctly so the data gets sent back correctly.
            'model_date_today_label': 'Start date:',
            'model_date_today_month': 'start_date_month',
            'model_date_today_day': 'start_date_day',
            'model_date_today_year': 'start_date_year',
            'model_date_unset_label': 'End date:',
            'model_date_unset_month': 'end_date_month',
            'model_date_unset_day': 'end_date_day',
            'model_date_unset_year': 'end_date_year',
            }
        )
