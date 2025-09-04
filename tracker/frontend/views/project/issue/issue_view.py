from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.shortcuts import render

from core.models import user as core_user_models
from project.models import issue as issue_models
from frontend.forms.project.issue import issue_form


@login_required
def issue(request, issue_id=None):
    logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)

    issue = logged_in_user.list_issues().get(pk=issue_id)
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
        template_name="project/issue/issue_modal.html",
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
