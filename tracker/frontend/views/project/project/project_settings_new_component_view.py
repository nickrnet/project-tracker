from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from frontend.util import project as project_utils
from frontend.forms.project.component import new_component_form as new_component_form
from core.models import user as core_user_models
from project.models import component as component_models


def handle_post(request, logged_in_user, project_id):
    received_new_component_form = new_component_form.NewComponentDataForm(request.POST, request.FILES)
    project = project_utils.get_project_by_uuid_or_label(logged_in_user, project_id)

    # Check if user can access project
    if project is None:
        messages.error(request, 'The specified Project does not exist or you do not have permission to see it. Try to create it, or contact the organization administrator.')
        return redirect("projects")

    if received_new_component_form.is_valid():
        component_data = component_models.ComponentData.objects.create(
            created_by=logged_in_user,
            name=received_new_component_form.cleaned_data.get('name', ''),
            description=received_new_component_form.cleaned_data.get('description', ''),
            label=received_new_component_form.cleaned_data.get('label', ''),
            is_active=received_new_component_form.cleaned_data.get('is_active', True)
            )
        component_models.Component.objects.create(
            created_by=logged_in_user,
            current=component_data,
            project=project
            )

        messages.success(request, ('Your component was successfully added!'))
    else:
        messages.error(request, 'Invalid data received. Please try again.')

    # Get current project settings to display
    repositories = project.git_repositories.all()
    components = project.component_set.all()
    versions = project.version_set.all()

    return render(
        request=request,
        template_name="project/project/project_settings_modal.html",
        context={
            'logged_in_user': logged_in_user,
            'project': project,
            'project_id': project_id,
            'git_repositories': repositories,
            'components': components,
            'versions': versions,
            },
        )


@login_required
def new_component(request, project_id=None):
    logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)

    if request.method == "POST":
        return handle_post(request, logged_in_user, project_id)

    component_form = new_component_form.NewComponentDataForm()

    return render(
        request=request,
        template_name="project/project/project_settings_new_component_modal.html",
        context={
            'logged_in_user': logged_in_user,
            'new_component_form': component_form,
            'project_id': project_id,
            }
        )
