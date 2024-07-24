from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from frontend.forms import signup_form


def signup(request):
    if request.method == "POST":
        new_user_data_form = signup_form.NewUserDataForm(request.POST, request.FILES)
        if new_user_data_form.is_valid():
            new_user_data_form.save()
            messages.success(request, ('Your user was successfully added!'))
        else:
            messages.error(request, 'Error saving user.')

        return redirect(reverse("new_project"))

    signup_form_data = signup_form.NewUserDataForm()

    return render(request=request, template_name="signup_template.html", context={'signup_form': signup_form_data})
