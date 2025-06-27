import uuid

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect

from frontend.forms.project.component import new_component_form as new_component_form
from frontend.forms.project.project import project_form
from core.models import user as core_user_models
from project.models import component as component_models
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


def handle_post(request, logged_in_user, project_id):
    received_new_component_form = new_component_form.NewComponentDataForm(request.POST, request.FILES)
    project = get_project(logged_in_user, project_id)

    if project:  # ALWAYS MAKE SURE USER CAN SEE THE PROJECT FIRST
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
            project = get_project(logged_in_user, project_id)
            messages.error(request, 'Invalid data received. Please try again.')
    else:
        messages.error(request, 'Permission denied.')

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
            'project_id': project_id,
            'project_form': form,
            'git_repositories': repositories,
            'components': components,
            'versions': versions,
            },
        )


@login_required
def new_component(request, project_id=None):
    try:
        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)
    except core_user_models.CoreUser.DoesNotExist:
        return redirect("logout")

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
