from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from frontend.util import project as project_utils
from frontend.forms.project.issue import new_issue_form
from core.models import user as core_user_models
from project.models import issue as issue_models


def handle_post(request, logged_in_user, project):
    received_new_issue_form = new_issue_form.NewIssueForm(request.POST, request.FILES)
    if received_new_issue_form.is_valid():
        # We return the whole issues_tab_pane, so get its required data

        issue_data = issue_models.IssueData.objects.create(
            created_by=logged_in_user,
            project=project,
            summary=received_new_issue_form.cleaned_data.get("summary"),
            description=received_new_issue_form.cleaned_data.get("description", ''),
            # TODO: Make reporter selectable from a list of project members or customers
            reporter=logged_in_user,
            assignee_id=received_new_issue_form.cleaned_data.get("assignee", ''),
            built_in_type_id=received_new_issue_form.cleaned_data.get("built_in_type", ''),
            built_in_priority_id=received_new_issue_form.cleaned_data.get("built_in_priority", ''),
            built_in_status_id=received_new_issue_form.cleaned_data.get("built_in_status", ''),
            built_in_severity_id=received_new_issue_form.cleaned_data.get("built_in_severity", ''),
            version_id=received_new_issue_form.cleaned_data.get("version", ''),
            component_id=received_new_issue_form.cleaned_data.get("component", ''),
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
        template_name="project/issue/issues_table.html",
        context={
            'logged_in_user': logged_in_user,
            'issues': logged_in_user.list_issues(),
            },
        )


@login_required
def new_issue(request, project_id):
    logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)

    # Check if user can access project
    project = project_utils.get_project_by_uuid_or_label(logged_in_user, project_id)
    if project is None:
        messages.error(request, 'The specified Project does not exist or you do not have permission to see it. Try to create it, or contact the organization administrator.')
        return redirect("projects")

    if request.method == "POST":
        return handle_post(request, logged_in_user, project)

    issue_form = new_issue_form.NewIssueForm()
    projects = logged_in_user.list_projects()
    issue_types = issue_models.Issue.active_objects.list_built_in_types()
    issue_priorities = issue_models.Issue.active_objects.list_built_in_priorities()
    issue_statuses = issue_models.Issue.active_objects.list_built_in_statuses()
    issue_severities = issue_models.Issue.active_objects.list_built_in_severities()
    issue_versions = issue_models.Issue.active_objects.list_versions(project.id) if project else []
    issue_components = issue_models.Issue.active_objects.list_components(project.id) if project else []

    return render(
        request=request,
        template_name="project/issue/new_issue_modal.html",
        context={
            'logged_in_user': logged_in_user,
            'new_issue_form': issue_form,
            'project_id': project_id,
            'projects': projects,
            'issue_types': issue_types,
            'issue_priorities': issue_priorities,
            'issue_statuses': issue_statuses,
            'issue_severities': issue_severities,
            'issue_versions': issue_versions,
            'issue_components': issue_components,
            }
        )
