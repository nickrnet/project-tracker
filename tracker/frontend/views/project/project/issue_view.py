from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View

from frontend.util import project as project_utils
from core.models import user as core_user_models
from project.models import issue as issue_models
from frontend.forms.project.issue import issue_form


class IssueView(LoginRequiredMixin, View):
    def valid_issue(self, logged_in_user, project_id, issue):
        not_valid = False
        # Make sure issue is in project
        if project_id != issue.project_id:
            not_valid = True

        # Check if user can access project
        project = project_utils.get_project_by_uuid_or_label(logged_in_user, issue.project_id)
        if project is None:
            not_valid = True

        if not_valid:
            return False

        return True

    def get(self, request, project_id, issue_id):
        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)
        issue = logged_in_user.list_issues().get(pk=issue_id)

        if not self.valid_issue(logged_in_user, project_id, issue):
            messages.error(request, 'The specified Issue does not exist or you do not have permission to see it.')
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
            template_name="project/project/issue_modal.html",
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

    def post(self, request, project_id, issue_id):
        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)
        received_issue_form = issue_form.IssueForm(request.POST, request.FILES)
        selected_components = request.POST.getlist('component')
        selected_versions = request.POST.getlist('version')
        issue = issue_models.Issue.active_objects.get(pk=issue_id)

        if not self.valid_issue(logged_in_user, project_id, issue):
            messages.error(request, 'The specified Issue does not exist or you do not have permission to see it.')
            return redirect("projects")

        if received_issue_form.is_valid():
            issue_data = issue_models.IssueData.objects.create(
                created_by=logged_in_user,
                created_on=timezone.now(),
                issue=issue,
                project_id=received_issue_form.cleaned_data.get("project", ''),
                summary=received_issue_form.cleaned_data.get("summary"),
                description=received_issue_form.cleaned_data.get("description", ''),
                reporter_id=received_issue_form.cleaned_data.get("reporter", ''),
                assignee_id=received_issue_form.cleaned_data.get("assignee", ''),
                built_in_type_id=received_issue_form.cleaned_data.get("built_in_type", ''),
                built_in_priority_id=received_issue_form.cleaned_data.get("built_in_priority", ''),
                built_in_status_id=received_issue_form.cleaned_data.get("built_in_status", ''),
                built_in_severity_id=received_issue_form.cleaned_data.get("built_in_severity", ''),
                )
            issue_data.component.set(selected_components)
            issue_data.version.set(selected_versions)
            issue.current = issue_data
            issue.save()
            messages.success(request, 'Issue updated!')
        else:
            messages.error(request, 'Error saving issue.')

        return render(
            request=request,
            template_name="project/project/issues_table.html",
            context={
                'logged_in_user': logged_in_user,
                'issues': logged_in_user.list_issues(),
                },
            )
