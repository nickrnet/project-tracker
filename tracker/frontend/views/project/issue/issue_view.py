from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect

from core.models import user as core_user_models
from frontend.forms.project.issue import issue_form


@login_required
def issue(request, issue_id=None):
    try:
        logged_in_user = core_user_models.CoreUser.objects.get(user__username=request.user)
    except core_user_models.CoreUser.DoesNotExist:
        return redirect("logout")

    issue = logged_in_user.list_issues().get(pk=issue_id)
    issue_copy = model_to_dict(issue)
    issue_copy['summary'] = issue.current.summary
    issue_copy['description'] = issue.current.description
    issue_copy.pop('current')
    form = issue_form.IssueForm(issue_copy)
    projects = logged_in_user.list_projects()
    issue_types = issue.list_built_in_types()
    issue_priorities = issue.list_built_in_priorities()
    issue_statuses = issue.list_built_in_statuses()
    issue_severities = issue.list_built_in_severities()
    issue_versions = issue.list_versions()
    issue_components = issue.list_components()

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
