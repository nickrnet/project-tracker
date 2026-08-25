from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View

from frontend.util import project as project_utils
from frontend.forms.project.component import component_form
from frontend.forms.project.project import project_form
from core.models import user as core_user_models
from project.models import component as component_models


class ComponentView(LoginRequiredMixin, View):
    def valid_component(self, logged_in_user, project_id, component):
        not_valid = False
        # Make sure component is in project
        if project_id != component.project_id:
            not_valid = True

        # Check if user can access project
        project = project_utils.get_project_by_uuid_or_label(logged_in_user, component.project_id)
        if project is None:
            not_valid = True

        if not_valid:
            return False

        return True

    def get(self, request, project_id, component_id):
        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)
        component = component_models.Component.objects.get(pk=component_id)

        if not self.valid_component(logged_in_user, project_id, component):
            messages.error(request, 'The specified Component does not exist or you do not have permission to see it.')
            return redirect("projects")

        component_data_dict = model_to_dict(component.current)
        component_form_data = component_form.ComponentDataForm(component_data_dict)

        return render(
            request=request,
            template_name="project/project/project_settings_component_modal.html",
            context={
                'logged_in_user': logged_in_user,
                'component_form': component_form_data,
                'component_id': component_id,
                'component': component,
                'project_id': project_id
                }
            )

    def post(self, request, project_id, component_id):
        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)
        component = component_models.Component.active_objects.get(pk=component_id)

        if not self.valid_component(logged_in_user, project_id, component):
            messages.error(request, 'The specified Component does not exist or you do not have permission to see it.')
            return redirect("projects")

        received_component_form = component_form.ComponentDataForm(request.POST, request.FILES)
        if received_component_form.is_valid():
            component_data = component_models.ComponentData.objects.create(
                created_by=logged_in_user,
                created_on=timezone.now(),
                component=component,
                name=received_component_form.cleaned_data.get('name', ''),
                description=received_component_form.cleaned_data.get('description', ''),
                label=received_component_form.cleaned_data.get('label', ''),
                is_active=received_component_form.cleaned_data.get('is_active', True)
                )
            component.current = component_data
            component.save()

            messages.success(request, ('Your component was successfully updated!'))
        else:
            messages.error(request, 'Invalid data received. Please try again.')

        # Get current project settings to display
        project_dict = model_to_dict(component.project.current)
        project_dict['label'] = component.project.label.current.label
        form = project_form.ProjectDataForm(project_dict)
        repositories = component.project.git_repositories.all()
        components = component.project.component_set.all()
        versions = component.project.version_set.all()

        return render(
            request=request,
            template_name="project/project/project_settings_modal.html",
            context={
                'logged_in_user': logged_in_user,
                'project': component.project,
                'project_id': component.project.id,
                'project_form': form,
                'git_repositories': repositories,
                'components': components,
                'versions': versions,
                },
            )
