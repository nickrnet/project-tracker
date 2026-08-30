from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View

from frontend.util import project as project_utils
from frontend.forms.project.version import version_form
from frontend.forms.project.project import project_form
from core.models import user as core_user_models
from project.models import version as version_models


class ProjectSettingsVersionView(LoginRequiredMixin, View):
    def valid_version(self, logged_in_user, project_id, version):
        not_valid = False
        # Make sure component is in project
        if project_id != version.project_id:
            not_valid = True

        # Check if user can access project
        project = project_utils.get_project_by_uuid_or_label(logged_in_user, version.project_id)
        if project is None:
            not_valid = True

        if not_valid:
            return False

        return True

    def get(self, request, project_id, version_id):
        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)
        try:
            version = version_models.Version.active_objects.get(pk=version_id)

            if not self.valid_version(logged_in_user, project_id, version):
                messages.error(request, 'The specified version does not exist.')
                return redirect("projects")

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
        except version_models.Version.DoesNotExist:
            messages.error(request, 'The specified version does not exist.')
            return redirect("projects")

    def post(self, request, project_id, version_id):
        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)

        try:
            version = version_models.Version.active_objects.get(pk=version_id)

            if not self.valid_version(logged_in_user, project_id, version):
                messages.error(request, 'The specified version does not exist.')
                return redirect("projects")

            received_version_form = version_form.VersionDataForm(request.POST, request.FILES)
            if received_version_form.is_valid():
                version_data = version_models.VersionData.objects.create(
                    created_by=logged_in_user,
                    created_on=timezone.now(),
                    version=version,
                    name=received_version_form.cleaned_data.get('name', ''),
                    description=received_version_form.cleaned_data.get('description', ''),
                    label=received_version_form.cleaned_data.get('label', ''),
                    release_date=version.current.release_date,  # TODO: Get this in the web page
                    is_active=received_version_form.cleaned_data.get('is_active', True)
                    )
                version.current = version_data
                version.save()

                messages.success(request, ('Your version was successfully updated.'))
            else:
                messages.error(request, 'Error saving version.')

            project = version.project
            project_dict = model_to_dict(project.current)
            if project.label:
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
        except version_models.Version.DoesNotExist:
            messages.error(request, 'The specified version does not exist.')
            return redirect("projects")
