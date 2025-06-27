import uuid

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect

from frontend.forms.project.version import version_form
from frontend.forms.project.project import project_form
from core.models import user as core_user_models
from project.models import version as version_models
from project.models import project as project_models


def get_project(logged_in_user, project_id):
    try:
        project_uuid = uuid.UUID(str(project_id))
        return logged_in_user.list_projects().get(id=project_uuid)
    except ValueError:
        try:
            return logged_in_user.list_projects().get(label__current__label=project_id)
        except project_models.Project.DoesNotExist:
            return None


def handle_post(request, logged_in_user, version_id):
    received_version_form = version_form.VersionDataForm(request.POST, request.FILES)
    version = version_models.Version.objects.get(pk=version_id)
    project = version.project
    project = get_project(logged_in_user, project.id)

    if received_version_form.is_valid():
        if project:
            version_data = version_models.VersionData.objects.create(
                created_by=logged_in_user,
                name=received_version_form.cleaned_data.get('name', ''),
                description=received_version_form.cleaned_data.get('description', ''),
                label=received_version_form.cleaned_data.get('label', ''),
                is_active=received_version_form.cleaned_data.get('is_active', True)
                )
            version.current = version_data
            version.save()

            messages.success(request, ('Your version was successfully updated!'))
        else:
            messages.error(request, 'Permission denied.')
    else:
        messages.error(request, 'Invalid data received. Please try again.')

    project_dict = model_to_dict(project.current)
    if project.label.current.label:
        project_dict['label'] = project.label.current.label
    form = project_form.ProjectDataForm(project_dict)
    repositories = project.git_repositories.all()
    components = project.component_set.all()
    versions = project.version_set.all()
    return render(
        request=request,
        template_name="project/project/project_settings_modal.html",
        context={
            'logged_in_user': logged_in_user,
            'project': project,
            'project_id': project.id,
            'project_form': form,
            'git_repositories': repositories,
            'components': components,
            'versions': versions,
            },
        )


@login_required
def version(request, version_id=None):
    try:
        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)
    except core_user_models.CoreUser.DoesNotExist:
        return redirect("logout")

    if request.method == "POST":
        return handle_post(request, logged_in_user, version_id)
    
    version = version_models.Version.objects.get(pk=version_id)
    version_data_dict = model_to_dict(version.current)
    version_form_data = version_form.VersionDataForm(version_data_dict)

    return render(
        request=request,
        template_name="project/project/project_settings_version_modal.html",
        context={
            'logged_in_user': logged_in_user,
            'version_form': version_form_data,
            'version_id': version_id,
            'version': version,
            }
        )
