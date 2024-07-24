from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from core.models import user as core_user_models
from frontend.forms.user import new_user_form


def new_user(request):
    if request.method == "POST":
        new_user_data_form = new_user_form.NewUserDataForm(request.POST, request.FILES)
        if new_user_data_form.is_valid():
            new_user_data_form.save()
            messages.success(request, ('Your user was successfully added!'))
        else:
            messages.error(request, 'Error saving user.')

        return redirect(reverse("new_user"))

    new_user_data_form = new_user_form.NewUserDataForm()
    try:
        logged_in_user = core_user_models.CoreUser.objects.get(user__username=request.user)
        users = logged_in_user.organizationmembers_set.all()
    except core_user_models.CoreUser.DoesNotExist:
        logged_in_user = None
        users = []

    return render(request=request, template_name="user/new_user_template.html", context={'logged_in_user': logged_in_user, 'new_user_form': new_user_data_form, 'users': users})
