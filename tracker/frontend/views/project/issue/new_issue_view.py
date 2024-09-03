from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from frontend.forms.project.issue import new_issue_form
from core.models import user as core_user_models
from project.models import issue as issue_models


@login_required
def new_issue(request):
    try:
        logged_in_user = core_user_models.CoreUser.objects.get(user__username=request.user)
    except core_user_models.CoreUser.DoesNotExist:
        return redirect("logout")

    if request.method == "POST":
        received_new_issue_data_form = new_issue_form.NewIssueDataForm(request.POST, request.FILES)
        if received_new_issue_data_form.is_valid():
            issue_data = issue_models.IssueData.objects.create(
                created_by=logged_in_user,
                summary=received_new_issue_data_form.cleaned_data.get("summary"),
                description=received_new_issue_data_form.cleaned_data.get("description"),
            )
            issue_data.save()
            request_fields = request.POST.copy()
            current = {'summary': request.POST.get('summary'), 'description': request.POST.get('description')}
            request_fields.pop('summary')
            request_fields.pop('description')
            request_fields.update(current)
            issue = issue_models.Issue.objects.create(
                created_by=logged_in_user,
                current=issue_data,
                project=logged_in_user.projects.get(id=request_fields.get("project")),
                reporter=logged_in_user,
            )
            issue.save()
            logged_in_user.issues.add(issue)
            logged_in_user.save()
            messages.success(request, ('Your issue was successfully added!'))
            return redirect("issue", issue_id=issue.id)
        else:
            messages.error(request, 'Error saving issue.')
            return redirect("new_issue")

    issue_form = new_issue_form.NewIssueForm()
    issue_data_form = new_issue_form.NewIssueDataForm()
    projects = logged_in_user.projects.all()

    return render(request=request, template_name="project/issue/new_issue_template.html", context={
        'logged_in_user': logged_in_user,
        'new_issue_form': issue_form,
        'new_issue_data_form': issue_data_form,
        'projects': projects,
    })
