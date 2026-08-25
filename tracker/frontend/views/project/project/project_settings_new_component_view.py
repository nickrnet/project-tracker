from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View

from frontend.util import project as project_utils
from frontend.forms.project.component import new_component_form as new_component_form
from core.models import user as core_user_models
from project.models import component as component_models


class NewComponentView(LoginRequiredMixin, View):
    def get(self, request, project_id):
        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)

        # Check if user can access project
        project = project_utils.get_project_by_uuid_or_label(logged_in_user, project_id)
        if project is None:
            messages.error(request, 'The specified Project does not exist or you do not have permission to see it.')
            return redirect("projects")

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

    def post(self, request, project_id):
        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)
        # Check if user can access project
        project = project_utils.get_project_by_uuid_or_label(logged_in_user, project_id)
        if project is None:
            messages.error(request, 'The specified Project does not exist or you do not have permission to see it. Try to create it, or contact the organization administrator.')
            return redirect("projects")
        # TODO: Make sure the project detected is the project passed in

        received_new_component_form = new_component_form.NewComponentDataForm(request.POST, request.FILES)
        if received_new_component_form.is_valid():
            component_data = component_models.ComponentData.objects.create(
                created_by=logged_in_user,
                created_on=timezone.now(),
                name=received_new_component_form.cleaned_data.get('name', ''),
                description=received_new_component_form.cleaned_data.get('description', ''),
                label=received_new_component_form.cleaned_data.get('label', ''),
                is_active=received_new_component_form.cleaned_data.get('is_active', True)
                )
            component = component_models.Component.objects.create(
                created_by=logged_in_user,
                created_on=timezone.now(),
                current=component_data,
                project=project
                )
            component_data.component = component
            component_data.save()
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
                'project_id': str(project.id),
                'git_repositories': repositories,
                'components': components,
                'versions': versions,
                },
            )
