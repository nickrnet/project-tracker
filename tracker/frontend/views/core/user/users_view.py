from importlib import resources

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
    organization_users = logged_in_user.organizationmembers_set.first().members.values_list('id', flat=True)
    project_users = logged_in_user.list_projects().values_list('users', flat=True)
    # Managing users of an organization is a different view
    # Combine the user IDs and get distinct users
    user_ids = set(organization_users).union(set(project_users))
    users = core_user_models.CoreUser.objects.filter(id__in=user_ids)
    timezone_choices = core_user_models.TIMEZONE_CHOICES
    with resources.files('tzdata.zoneinfo').joinpath('iso3166.tab').open('r') as f:
        country_names = dict(
            line.rstrip('\n').split('\t', 1)
            for line in f
            if not line.startswith('#')
        )
        country_names = sorted(country_names.items(), key=lambda x: x[1])

    return render(
        request=request,
        template_name="core/user/users_template.html",
        context={
            'logged_in_user': logged_in_user,
            'users': users,
            'country_names': country_names,
            'timezones': timezone_choices,
        }
    )
