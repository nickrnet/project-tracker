from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from frontend.util import project as project_utils
from core.models import user as core_user_models


@login_required
def project(request, project_id):
    logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)

    project = project_utils.get_project_by_uuid_or_label(logged_in_user, project_id)
    if project is None:
        messages.error(request, 'The specified Project does not exist or you do not have permission to see it. Try to create it, or contact the organization administrator.')
        return redirect("projects")

    return render(
        request=request,
        template_name="project/project/project_template.html",
        context={
            'logged_in_user': logged_in_user,
            'project': project,
            'project_id': project_id,
            'issues': project.issue_set.all(),
            }
        )
