import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from core.models import user as core_user_models
from project.models import project as project_models


@login_required
def project(request, project_id):
    logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)

    try:
        project_uuid = uuid.UUID(str(project_id))
        project = logged_in_user.list_projects().get(id=project_uuid)
    except ValueError:
        try:
            project = logged_in_user.list_projects().get(label__current__label=project_id)
        except project_models.Project.DoesNotExist:
            messages.error(
                request, 'The specified Project does not exist or you do not have permission to see it. Try to create it, or contact the organization administrator.')
            return redirect("projects")
    except project_models.Project.DoesNotExist:
        messages.error(
            request, 'The specified Project does not exist or you do not have permission to see it. Try to create it, or contact the organization administrator.')
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
