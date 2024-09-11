from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from frontend.forms.project.issue import new_issue_form
from core.models import user as core_user_models
from project.models import issue as issue_models


@login_required
def new_issue(request, project_id=None):
    try:
        logged_in_user = core_user_models.CoreUser.objects.get(user__username=request.user)
    except core_user_models.CoreUser.DoesNotExist:
        return redirect("logout")

    if request.method == "POST":
        received_new_issue_form = new_issue_form.NewIssueForm(request.POST, request.FILES)
        if received_new_issue_form.is_valid():
            # We return the whole issues_tab_pane, so get its required data
            project = logged_in_user.project_set.get(id=received_new_issue_form.cleaned_data.get('project'))
            projects = logged_in_user.project_set.all()

            issue_data = issue_models.IssueData.objects.create(
                created_by=logged_in_user,
                summary=received_new_issue_form.cleaned_data.get("summary"),
                description=received_new_issue_form.cleaned_data.get("description"),
            )
            issue_data.save()
            issue = issue_models.Issue.objects.create(
                created_by=logged_in_user,
                current=issue_data,
                project=project,
                reporter=logged_in_user,
                sequence=issue_models.Issue.objects.get_next_sequence_number(project.id)
            )
            issue.save()
            logged_in_user.issues.add(issue)
            logged_in_user.save()
            messages.success(request, ('Your issue was successfully added!'))
        else:
            messages.error(request, 'Error saving issue.')

        return render(
            request=request,
            template_name="project/project/issues_tab_pane.html",
            context={
                'logged_in_user': logged_in_user,
                'new_issue_form': received_new_issue_form,
                'project_id': project_id,
                'project': project,
                'projects': projects,
                'issues': project.issue_set.all(),
            },
        )

    issue_form = new_issue_form.NewIssueForm()
    projects = logged_in_user.project_set.all()
    if project_id:
        # make sure the user has access to the project
        logged_in_user.project_set.get(id=project_id)

    return render(
        request=request,
        template_name="project/project/new_issue_modal.html",
        context={
            'logged_in_user': logged_in_user,
            'new_issue_form': issue_form,
            'project_id': project_id,
            'projects': projects
        }
    )
