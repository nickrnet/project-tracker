from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect

from core.models import user as core_user_models
from frontend.forms.user import core_user_form


@login_required
def user(request, user_id=None):
    try:
        logged_in_user = core_user_models.CoreUser.objects.get(user__username=request.user)
    except core_user_models.CoreUser.DoesNotExist:
        return redirect("logout")

    user = core_user_models.CoreUser.objects.get(pk=user_id)
    if request.method == "POST":
        user_data_form = core_user_form.UserDataForm(request.POST, request.FILES)
        if user_data_form.is_valid():
            user.current.hard_delete(user_id)
            user_data = core_user_models.CoreUserData(
                created_by_id=user_id,
                first_name=user_data_form.cleaned_data.get('first_name', ''),
                last_name=user_data_form.cleaned_data.get('last_name', ''),
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

    user_data_form = core_user_form.UserDataForm(model_to_dict(user.current))
    return render(
        request=request,
        template_name="user/core_user_template.html",
        context={
            "logged_in_user": logged_in_user,
            "user_data_form": user_data_form
        }
    )
