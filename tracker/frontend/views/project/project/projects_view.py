from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from core.models import user as core_user_models


@login_required
def projects(request):
    try:
        logged_in_user = core_user_models.CoreUser.objects.get(user__username=request.user)
    except core_user_models.CoreUser.DoesNotExist:
        return redirect("logout")

    projects = logged_in_user.list_projects()

    return render(
        request=request,
        template_name="project/project/projects_template.html",
        context={
            'logged_in_user': logged_in_user,
            'projects': projects,
        }
    )
