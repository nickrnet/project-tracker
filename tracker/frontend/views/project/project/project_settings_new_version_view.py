from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect

from frontend.util import project as project_utils
from frontend.forms.project.version import new_version_form as new_version_form
from frontend.forms.project.project import project_form
from core.models import user as core_user_models
from project.models import version as version_models


def handle_post(request, logged_in_user, project):
    received_new_version_form = new_version_form.NewVersionDataForm(request.POST, request.FILES)

    if received_new_version_form.is_valid():
        version_data = version_models.VersionData.objects.create(
            created_by=logged_in_user,
            name=received_new_version_form.cleaned_data.get('name', ''),
            description=received_new_version_form.cleaned_data.get('description', ''),
            label=received_new_version_form.cleaned_data.get('label', ''),
            release_date=received_new_version_form.cleaned_data.get('release_date', ''),
            is_active=received_new_version_form.cleaned_data.get('is_active', True)
            )
        version_models.Version.objects.create(
            created_by=logged_in_user,
            current=version_data,
            project=project
            )
        messages.success(request, ('Your version was successfully added!'))
    else:
        messages.error(request, 'Invalid data received. Please try again.')

    project_dict = model_to_dict(project.current)
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
            'project_id': str(project.id),
            'project_form': form,
            'git_repositories': repositories,
            'components': components,
            'versions': versions,
            },
        )


@login_required
def new_version(request, project_id):
    logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)

    # Check if user can access project
    project = project_utils.get_project_by_uuid_or_label(logged_in_user, project_id)
    if project is None:
        messages.error(request, 'The specified Project does not exist or you do not have permission to see it. Try to create it, or contact the organization administrator.')
        return redirect("projects")

    if request.method == "POST":
        return handle_post(request, logged_in_user, project)

    version_form = new_version_form.NewVersionDataForm()

    return render(
        request=request,
        template_name="project/project/project_settings_new_version_modal.html",
        context={
            'logged_in_user': logged_in_user,
            'new_version_form': version_form,
            'project_id': project_id,
            }
        )
