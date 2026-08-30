from importlib import resources

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from core.models import user as core_user_models


class UsersView(LoginRequiredMixin, View):
    def get(self, request):
        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)
        users = logged_in_user.list_users()
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
