from importlib import resources

from django.contrib import messages
from django.shortcuts import render, redirect

from core.models import user as core_user_models
from frontend.forms import signup_form


def signup(request):
    if request.method == "POST":
        new_user_data_form = signup_form.NewUserForm(request.POST, request.FILES)
        if new_user_data_form.is_valid():
            core_user_models.CoreUser.objects.create_core_user_from_web(new_user_data_form.cleaned_data)
            messages.success(request, ('Your signup was successful!'))
            return redirect("login")
        else:
            messages.error(request, 'Error saving user. Double check your data and try again.')
            return render(
                request=request,
                template_name="signup_template.html",
                context={
                    'signup_form': new_user_data_form
                }
            )

    signup_form_data = signup_form.NewUserForm()
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
        template_name="signup_template.html",
        context={
            'signup_form': signup_form_data,
            'timezone_choices': timezone_choices,
            'country_names': country_names,
        }
    )
