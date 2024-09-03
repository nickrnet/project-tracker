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

    issue = logged_in_user.issue_created_by.get(pk=issue_id)
    issue_copy = model_to_dict(issue)
    issue_copy['summary'] = issue.current.summary
    issue_copy['description'] = issue.current.description
    issue_copy.pop('current')
    form = issue_form.IssueForm(issue_copy)
    projects = logged_in_user.projects.all()

    return render(
        request=request,
        template_name="project/issue/issue_template.html",
        context={
            'logged_in_user': logged_in_user,
            'issue_form': form,
            'projects': projects,
        }
    )
