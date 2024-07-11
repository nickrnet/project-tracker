from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from frontend.forms import new_user_form as new_user_forms


def signup(request):
    if request.method == "POST":
        new_user_data_form = new_user_forms.NewUserDataForm(request.POST, request.FILES)
        if new_user_data_form.is_valid():
            new_user_data_form.save()
            messages.success(request, ('Your user was successfully added!'))
        else:
            messages.error(request, 'Error saving user')

        return redirect(reverse("new_project"))

    new_user_data_form = new_user_forms.NewUserDataForm()

    return render(request=request, template_name="signup_template.html", context={'new_user_form': new_user_data_form})
