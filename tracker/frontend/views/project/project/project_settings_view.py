import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect

from frontend.util import project as project_utils
from core.models import user as core_user_models
from frontend.forms.project.project import project_form
from project.models import project as project_models


def handle_post(request, logged_in_user: core_user_models.CoreUser, project_id: str, project: project_models.Project):
    received_project_data_form = project_form.ProjectDataForm(request.POST, request.FILES)
    if received_project_data_form.is_valid():
        project_data_form = received_project_data_form.cleaned_data.copy()
        project_label = project_data_form.pop("label")

        if project_label:
            new_project_label_data = project_models.ProjectLabelData.objects.create(
                created_by=logged_in_user,
                label=project_label,
                )
            new_project_label = project_models.ProjectLabel.objects.create(
                created_by=logged_in_user,
                current=new_project_label_data,
                )
            project.label = new_project_label
            # If the project label changed, and it was in the url used to get here, we need to alter the url to give back to the user
            try:
                # But ignore this if the UUID was used
                uuid.UUID(str(project_id))
            except ValueError:
                project_id = project_label

        project_data_form["created_by_id"] = str(logged_in_user.id)
        project_data = project_models.ProjectData.objects.create(**project_data_form)
        project.current = project_data
        project.save()  # THIS IS NUKING THE USER'S PROJECT_SET FOR SOME REASON IN TESTS, THIS DOES NOT APPEAR TO HAPPEN IN A WEB REQUEST WTAF

        messages.success(request, ('Your project was successfully updated!'))
    else:
        messages.error(request, 'Error saving project.')

    return redirect("project", project_id=project_id)


@login_required
def project_settings(request, project_id):
    logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)

    project = project_utils.get_project_by_uuid_or_label(logged_in_user, project_id)
    if project is None:
        messages.error(request, 'The specified Project does not exist or you do not have permission to see it. Try to create it, or contact the organization administrator.')
        return redirect("projects")

    if request.method == "POST":
        return handle_post(request, logged_in_user, project_id, project)

    project_dict = model_to_dict(project.current)
    if project.label:
        project_dict['label'] = project.label.current.label
    form = project_form.ProjectDataForm(project_dict)
    components = project.component_set.all()
    versions = project.version_set.all()
    repositories = project.git_repositories.all()
    users = project.list_users()

    return render(
        request=request,
        template_name="project/project/project_settings_modal.html",
        context={
            'logged_in_user': logged_in_user,
            'project': project,
            'project_id': project_id,
            'project_form': form,
            'components': components,
            'versions': versions,
            'git_repositories': repositories,
            'users': users,
            }
        )
