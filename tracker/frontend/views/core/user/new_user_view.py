from importlib import resources

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from core.models import user as core_user_models
from frontend.forms.core.user import new_user_form


class NewUserView(LoginRequiredMixin, View):
    def get(self, request):
        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)
        new_user_data_form = new_user_form.NewUserForm()
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
            template_name="core/user/new_user_modal.html",
            context={
                'logged_in_user': logged_in_user,
                'new_user_form': new_user_data_form,
                'timezone_choices': timezone_choices,
                'country_names': country_names,
                }
            )

    def post(self, request):
        new_user_data_form = new_user_form.NewUserForm(request.POST, request.FILES)
        if new_user_data_form.is_valid():
            new_user = core_user_models.CoreUser.objects.create_core_user_from_web(new_user_data_form.cleaned_data.copy())
            messages.success(request, ('Your user was successfully added.'))
            return redirect("user", user_id=new_user.id)
        else:
            messages.error(request, 'Error saving user.')
            return redirect("users")
