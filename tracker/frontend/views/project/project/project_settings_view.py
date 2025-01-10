import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect

from core.models import user as core_user_models
from frontend.forms.project.project import project_form
from project.models import project as project_models


def handle_post(request, project_id, logged_in_user):
    received_project_data_form = project_form.ProjectDataForm(request.POST, request.FILES)
    if received_project_data_form.is_valid():
        try:
            project = logged_in_user.list_projects().get(id=project_id)
            project_data_form = received_project_data_form.cleaned_data.copy()
            # TODO: Create a new git repository if needed
            project_data_form.pop("git_repository")

            project_label = project_data_form.pop("label")
            project_label_name = project_models.ProjectLabelName(
                created_by_id=logged_in_user.id,
                name=project_label,
                )
            project_label_name.save()
            project_label_data = project_models.ProjectLabelData(
                created_by_id=logged_in_user.id,
                name=project_label_name,
                )
            project_label_data.save()
            project_label = project_models.ProjectLabel(
                created_by_id=logged_in_user.id,
                current=project_label_data,
                )
            project_label.save()

            project_data_form["created_by_id"] = str(logged_in_user.id)
            project_data = project_models.ProjectData.objects.create(**project_data_form)

            project.current = project_data
            project.label = project_label
            project.save()

            messages.success(request, ('Your project was successfully updated!'))
            return redirect("project", project_id=project_id)
        except project_models.Project.DoesNotExist:
            messages.error(
                request, "The specified Project does not exist. Create it and try again.")
            return redirect("new_project")
    else:
        messages.error(request, 'Error saving project.')
        return render(
            request=request,
            template_name="project/project/new_project_template.html"
            )


@login_required
def project_settings(request, project_id=None):
    try:
        logged_in_user = core_user_models.CoreUser.objects.get(user__username=request.user)
    except core_user_models.CoreUser.DoesNotExist:
        return redirect("logout")

    if request.method == "POST":
        handle_post(request, project_id, logged_in_user)

    try:
        project_uuid = uuid.UUID(str(project_id))
        project = logged_in_user.list_projects().get(id=project_uuid)
    except ValueError:
        try:
            project = logged_in_user.list_projects().get(current__label__current__label=project_id)
        except project_models.Project.DoesNotExist:
            messages.error(
                request, 'The specified Project does not exist or you do not have permission to see it. Try to create it, or contact the organization administrator.')
            return redirect("projects")
    except project_models.Project.DoesNotExist:
        messages.error(
            request, 'The specified Project does not exist or you do not have permission to see it. Try to create it, or contact the organization administrator.')
        return redirect("projects")

    project_dict = model_to_dict(project.current)
    if project.current.label:
        project_dict['label'] = project.current.label.current.label
    form = project_form.ProjectDataForm(project_dict)
    repositories = project.current.git_repositories.all()
    users = project.list_users(logged_in_user)

    return render(
        request=request,
        template_name="project/project/project_settings.html",
        context={
            'logged_in_user': logged_in_user,
            'project': project,
            'project_id': project_id,
            'project_form': form,
            'git_repositories': repositories,
            'users': users,
            'issues': project.issuedata_set.all(),
            }
        )
