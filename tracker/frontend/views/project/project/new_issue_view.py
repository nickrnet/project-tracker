import uuid

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from frontend.forms.project.issue import new_issue_form
from core.models import user as core_user_models
from project.models import issue as issue_models
from project.models import project as project_models


def handle_post(request, logged_in_user, project):
    received_new_issue_form = new_issue_form.NewIssueForm(request.POST, request.FILES)

    if received_new_issue_form.is_valid():
        issue_data = issue_models.IssueData.objects.create(
            created_by=logged_in_user,
            project=project,
            reporter_id=received_new_issue_form.cleaned_data.get("reporter"),
            assignee_id=received_new_issue_form.cleaned_data.get("assignee"),
            summary=received_new_issue_form.cleaned_data.get("summary"),
            description=received_new_issue_form.cleaned_data.get("description"),
            built_in_type_id=received_new_issue_form.cleaned_data.get("built_in_type"),
            built_in_priority_id=received_new_issue_form.cleaned_data.get("built_in_priority"),
            built_in_status_id=received_new_issue_form.cleaned_data.get("built_in_status"),
            built_in_severity_id=received_new_issue_form.cleaned_data.get("built_in_severity"),
            version_id=received_new_issue_form.cleaned_data.get("version"),
            component_id=received_new_issue_form.cleaned_data.get("component"),
            )
        issue_models.Issue.objects.create(
            created_by=logged_in_user,
            current=issue_data,
            project=project,
            sequence=issue_models.Issue.objects.get_next_sequence_number(project.id)
            )

        messages.success(request, ('Your issue was successfully added!'))
    else:
        messages.error(request, 'Error saving issue.')

    return render(
        request=request,
        template_name="project/project/issues_tab_pane.html",
        context={
            'logged_in_user': logged_in_user,
            'project': project,
            'issues': project.list_issues() if project else [],
            },
        )

@login_required
def new_issue(request, project_id=None):
    logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)

    try:
        project_uuid = uuid.UUID(str(project_id))
        project = logged_in_user.list_projects().get(id=project_uuid)
    except ValueError:
        try:
            project = logged_in_user.list_projects().get(label__current__label=project_id)
        except project_models.Project.DoesNotExist:
            messages.error(request, 'Choose a project.')
            return redirect(reverse('projects'))

    if request.method == "POST":
        return handle_post(request, logged_in_user, project)

    issue_form = new_issue_form.NewIssueForm()
    projects = logged_in_user.list_projects()
    issue_types = issue_models.Issue.objects.list_built_in_types()
    issue_priorities = issue_models.Issue.objects.list_built_in_priorities()
    issue_statuses = issue_models.Issue.objects.list_built_in_statuses()
    issue_severities = issue_models.Issue.objects.list_built_in_severities()
    issue_versions = issue_models.Issue.objects.list_versions(project.id) if project else []
    issue_components = issue_models.Issue.objects.list_components(project.id) if project else []

    return render(
        request=request,
        template_name="project/project/new_issue_modal.html",
        context={
            'logged_in_user': logged_in_user,
            'new_issue_form': issue_form,
            'project_id': project_id,
            'projects': projects,
            'project': project,
            'issue_types': issue_types,
            'issue_priorities': issue_priorities,
            'issue_statuses': issue_statuses,
            'issue_severities': issue_severities,
            'issue_versions': issue_versions,
            'issue_components': issue_components,
            }
        )
