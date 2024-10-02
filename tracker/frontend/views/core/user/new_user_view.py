from importlib import resources

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from core.models import user as core_user_models
from frontend.forms.core.user import new_user_form


@login_required
def new_user(request):
    try:
        logged_in_user = core_user_models.CoreUser.objects.get(user__username=request.user)
    except core_user_models.CoreUser.DoesNotExist:
        return redirect("logout")

    if request.method == "POST":
        new_user_data_form = new_user_form.NewUserForm(request.POST, request.FILES)
        if new_user_data_form.is_valid():
            new_user = core_user_models.CoreUser.objects.create_core_user_from_web(new_user_data_form.cleaned_data)
            messages.success(request, ('Your user was successfully added!'))
            return redirect("user", user_id=new_user.id)
        else:
            messages.error(request, 'Error saving user.')
            return redirect("new_user")

    new_user_data_form = new_user_form.NewUserForm()

    # Get unique users from organizations and projects
    organization_users = logged_in_user.organizationmembers_set.first().members.values_list('id', flat=True)
    project_users = logged_in_user.list_projects().values_list('users', flat=True)

    # Combine the user IDs and get distinct users
    user_ids = set(organization_users).union(set(project_users))
    users = core_user_models.CoreUser.objects.filter(id__in=user_ids)

    user_organizations = logged_in_user.organization_created_by.all()
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
        template_name="core/user/new_user_template.html",
        context={
            'logged_in_user': logged_in_user,
            'new_user_form': new_user_data_form,
            'users': users,
            'user_organizations': user_organizations,
            'timezone_choices': timezone_choices,
            'country_names': country_names,
        }
    )
