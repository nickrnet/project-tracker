from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from core.models import user as core_user_models


@login_required
def users(request):
    try:
        logged_in_user = core_user_models.CoreUser.objects.get(user__username=request.user)
    except core_user_models.CoreUser.DoesNotExist:
        return redirect("logout")

    # Get unique users from owned organizations and projects
    organization_users = logged_in_user.organizations.values_list('members', flat=True)
    project_users = logged_in_user.projects.values_list('users', flat=True)
    # Managing users of an organization is a different view
    # Combine the user IDs and get distinct users
    user_ids = set(organization_users).union(set(project_users))
    users = core_user_models.CoreUser.objects.filter(id__in=user_ids)

    return render(
        request=request,
        template_name="core/user/users_template.html",
        context={
            'logged_in_user': logged_in_user,
            'users': users,
        }
    )
