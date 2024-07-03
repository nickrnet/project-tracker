from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from core.models import user as core_user_models
from frontend.forms import new_user_form as new_user_forms


def new_user(request):
    if request.method == "POST":
        new_user_data_form = new_user_forms.NewUserDataForm(request.POST, request.FILES)
        if new_user_data_form.is_valid():
            new_user_data_form.save()
            messages.success(request, ('Your user was successfully added!'))
        else:
            messages.error(request, 'Error saving user')

        return redirect(reverse("new_user"))

    new_user_data_form = new_user_forms.NewUserDataForm()
    users = core_user_models.CoreUser.active_objects.all()

    return render(request=request, template_name="new_user_template.html", context={'new_user_form': new_user_data_form, 'users': users})
