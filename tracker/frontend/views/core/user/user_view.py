from importlib import resources

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect

from core.models import user as core_user_models
from frontend.forms.core.user import core_user_form


def handle_post(request, logged_in_user, user_id):
    user_data_form = core_user_form.UserDataForm(request.POST, request.FILES)
    if user_data_form.is_valid():
        user = core_user_models.CoreUser.active_objects.get(pk=user_id)
        user_data = core_user_models.CoreUserData(
            created_by=logged_in_user,
            name_prefix=user_data_form.cleaned_data.get('name_prefix', ''),
            first_name=user_data_form.cleaned_data.get('first_name', ''),
            middle_name=user_data_form.cleaned_data.get('middle_name', ''),
            last_name=user_data_form.cleaned_data.get('last_name', ''),
            name_suffix=user_data_form.cleaned_data.get('name_suffix', ''),
            email=user_data_form.cleaned_data.get('email'),
            secondary_email=user_data_form.cleaned_data.get('secondary_email', ''),
            home_phone=user_data_form.cleaned_data.get('home_phone', ''),
            mobile_phone=user_data_form.cleaned_data.get('mobile_phone', ''),
            work_phone=user_data_form.cleaned_data.get('work_phone', ''),
            address_line_1=user_data_form.cleaned_data.get('address_line_1', ''),
            address_line_2=user_data_form.cleaned_data.get('address_line_2', ''),
            postal_code=user_data_form.cleaned_data.get('postal_code', ''),
            city=user_data_form.cleaned_data.get('city', ''),
            state=user_data_form.cleaned_data.get('state', ''),
            country=user_data_form.cleaned_data.get('country', ''),
            timezone=user_data_form.cleaned_data.get('timezone', ''),
            )
        user_data.save()
        user.current = user_data
        user.save()
        messages.success(request, ("Your user was successfully updated!"))
    else:
        messages.error(request, "Error saving user.")

    return redirect("user", user_id=user_id)


@login_required
def user(request, user_id=None):
    logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)
    user = core_user_models.CoreUser.active_objects.get(pk=user_id)

    if request.method == "POST":
        return handle_post(request, logged_in_user, user_id)

    user_data_form = core_user_form.UserDataForm(model_to_dict(user.current))
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
        template_name="core/user/core_user_template.html",
        context={
            "logged_in_user": logged_in_user,
            "user_data_form": user_data_form,
            "user": user,
            'timezone_choices': timezone_choices,
            'country_names': country_names,
            }
        )
