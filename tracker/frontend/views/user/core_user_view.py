from django.contrib import messages
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from django.urls import reverse

from core.models import user as core_user_models
from frontend.forms.user import new_user_form, core_user_form


def core_user(request):
    if request.method == "POST":
        user_data_form = core_user_form.CoreUserDataForm(request.POST, request.FILES)
        if user_data_form.is_valid():
            user_data_form.save()
            messages.success(request, ('Your user was successfully updated!'))
        else:
            messages.error(request, 'Error saving user.')

        return redirect(reverse("core_user"))

    try:
        logged_in_user = core_user_models.CoreUser.objects.get(user__username=request.user)
        user_data_form = core_user_form.CoreUserDataForm(model_to_dict(logged_in_user.core_user_data))
        # breakpoint()
    except core_user_models.CoreUser.DoesNotExist:
        logged_in_user = None
        user_data_form = new_user_form.NewUserDataForm()

    return render(
        request=request,
        template_name="user/core_user_template.html",
        context={'logged_in_user': logged_in_user, 'user_data_form': user_data_form}
    )
