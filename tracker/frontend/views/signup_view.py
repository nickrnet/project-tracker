from importlib import resources

from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View

from core.models import user as core_user_models
from frontend.forms.signup_form import SignupForm


class SignupView(View):
    signup_form_data = SignupForm()
    timezone_choices = core_user_models.TIMEZONE_CHOICES
    with resources.files('tzdata.zoneinfo').joinpath('iso3166.tab').open('r') as f:
        country_names = dict(
            line.rstrip('\n').split('\t', 1)
            for line in f
            if not line.startswith('#')
            )
        country_names = sorted(country_names.items(), key=lambda x: x[1])

    def get(self, request):
        signup_form_data = SignupForm()
        return render(
            request=request,
            template_name="signup_template.html",
            context={
                'signup_form': signup_form_data,
                'timezone_choices': self.timezone_choices,
                'country_names': self.country_names,
                }
            )

    def post(self, request):
        new_user_data_form = SignupForm(request.POST, request.FILES)
        next_url = request.GET.get('next')
        if new_user_data_form.is_valid():
            new_user = core_user_models.CoreUser.objects.create_core_user_from_web(new_user_data_form.cleaned_data)
            new_user.subscribe_to_trial()
            messages.success(request, ('Your signup was successful!'))
            if next_url and url_has_allowed_host_and_scheme(url=next_url, allowed_hosts=request.get_host()):
                return redirect(next_url)
            else:
                return redirect('login')
        else:
            messages.error(request, 'Error saving user. Double check your information and try again.')
            return render(
                request=request,
                template_name="signup_template.html",
                context={
                    'signup_form': new_user_data_form,
                    'timezone_choices': self.timezone_choices,
                    'country_names': self.country_names,
                    }
                )
