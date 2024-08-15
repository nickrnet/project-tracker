from django.contrib import messages
from django.shortcuts import render, redirect

from core.models import user as core_user_models
from frontend.forms import signup_form


def signup(request):
    if request.method == "POST":
        new_user_data_form = signup_form.NewUserDataForm(request.POST, request.FILES)
        if new_user_data_form.is_valid():
            core_user_models.CoreUser.objects.create_core_user_from_web(new_user_data_form.cleaned_data)
            messages.success(request, ('Your signup was successful!'))
            return redirect("login")
        else:
            messages.error(request, 'Error saving user. Double check your data and try again.')
            return render(request, "signup_template.html", context={'signup_form': new_user_data_form})

    signup_form_data = signup_form.NewUserDataForm()

    return render(request=request, template_name="signup_template.html", context={
        'signup_form': signup_form_data
    })
