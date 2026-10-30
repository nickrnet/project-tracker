import uuid

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View

from frontend.util import project as project_utils
from core.models import user as core_user_models
from project.models import issue as issue_models
from frontend.forms.project.issue import issue_form


class IssueView(LoginRequiredMixin, View):
    def handle_uuid_list(self, list_to_validate_with, uuid_list):
        valid_uuids = []
        for item_id in uuid_list:
            try:
                item_id = uuid.UUID(item_id)
                if item_id in list_to_validate_with:
                    valid_uuids.append(item_id)
            except ValueError:
                continue
        return valid_uuids

    def valid_issue(self, project_id, issue):
        not_valid = False
        # Make sure issue is in specified project
        if project_id != issue.project_id:
            not_valid = True

        if not_valid:
            return False

        return True

    def get(self, request, project_id, issue_id):
        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)

        try:
            issue = logged_in_user.list_issues().get(pk=issue_id)

            if not self.valid_issue(project_id, issue):
                messages.error(request, 'The specified issue does not exist.')
                return redirect("projects")

            issue_copy = model_to_dict(issue)
            issue_copy['summary'] = issue.current.summary
            issue_copy['description'] = issue.current.description
            issue_copy.pop('current')
            form = issue_form.IssueForm(issue_copy)

            projects = logged_in_user.list_projects()
            issue_types = issue_models.Issue.objects.list_built_in_types()
            issue_priorities = issue_models.Issue.objects.list_built_in_priorities()
            issue_statuses = issue_models.Issue.objects.list_built_in_statuses()
            issue_severities = issue_models.Issue.objects.list_built_in_severities()
            issue_versions = issue_models.Issue.objects.list_versions(issue.project_id)
            issue_components = issue_models.Issue.objects.list_components(issue.project_id)

            return render(
                request=request,
                template_name="project/project/issue.html",
                context={
                    'logged_in_user': logged_in_user,
                    'issue_form': form,
                    'issue': issue,
                    'projects': projects,
                    'issue_types': issue_types,
                    'issue_priorities': issue_priorities,
                    'issue_statuses': issue_statuses,
                    'issue_severities': issue_severities,
                    'issue_versions': issue_versions,
                    'issue_components': issue_components,
                    }
                )
        except issue_models.Issue.DoesNotExist:
            messages.error(request, 'The specified issue does not exist.')
            return redirect('projects')

    def post(self, request, project_id, issue_id):
        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)
        received_issue_form = issue_form.IssueForm(request.POST, request.FILES)

        # Check if user can access project
        project = project_utils.get_project_by_uuid_or_label(logged_in_user, project_id)
        if project is None:
            messages.error(request, 'The specified issue does not exist.')
            return redirect("projects")

        if received_issue_form.is_valid():
            selected_component_ids = request.POST.getlist('component')
            selected_version_ids = request.POST.getlist('version')

            # Convert lists of id strings to UUIDs
            project_components = project.component_set.all().values_list('id', flat=True)
            selected_components = self.handle_uuid_list(project_components, selected_component_ids)
            selected_versions = []
            project_versions = project.version_set.all().values_list('id', flat=True)
            selected_versions = self.handle_uuid_list(project_versions, selected_version_ids)

            issue_form_data = received_issue_form.cleaned_data.copy()
            try:
                issue = logged_in_user.list_issues().get(pk=issue_id)

                issue_data = issue_models.IssueData.objects.create(
                    created_by=logged_in_user,
                    created_on=timezone.now(),
                    issue=issue,
                    project_id=issue_form_data.get("project", ''),
                    summary=issue_form_data.get("summary"),
                    description=issue_form_data.get("description", ''),
                    reporter_id=issue_form_data.get("reporter", ''),
                    assignee_id=issue_form_data.get("assignee", ''),
                    built_in_type_id=issue_form_data.get("built_in_type", ''),
                    built_in_priority_id=issue_form_data.get("built_in_priority", ''),
                    built_in_status_id=issue_form_data.get("built_in_status", ''),
                    built_in_severity_id=issue_form_data.get("built_in_severity", ''),
                    )
                issue_data.component.set(selected_components)
                issue_data.version.set(selected_versions)
                issue.current = issue_data
                issue.project_id = project_id
                issue.save()
                messages.success(request, 'Issue updated.')
                issue.send_issue_update_email(reverse('issue', kwargs={'issue_id': str(issue.id)}))
                return redirect(reverse('project_issue', kwargs={'project_id': project_id, 'issue_id': issue.id}))
            except issue_models.Issue.DoesNotExist:
                messages.error(request, 'The specified issue does not exist.')
                return redirect('projects')
        else:
            messages.error(request, 'Error saving issue.')
            return redirect(reverse('project_issue', kwargs={'project_id': project_id, 'issue_id': issue_id}))
