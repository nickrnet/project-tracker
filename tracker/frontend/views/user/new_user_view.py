from django.contrib import messages
from django.shortcuts import render, redirect

from core.models import user as core_user_models
from frontend.forms.user import new_user_form


def new_user(request):
    try:
        logged_in_user = core_user_models.CoreUser.objects.get(user__username=request.user)
    except core_user_models.CoreUser.DoesNotExist:
        return redirect("logout")

    if request.method == "POST":
        new_user_data_form = new_user_form.NewUserDataForm(request.POST, request.FILES)
        if new_user_data_form.is_valid():
            new_user = core_user_models.CoreUser.objects.create_core_user_from_web(new_user_data_form.cleaned_data)
            messages.success(request, ('Your user was successfully added!'))
            return redirect("user", user_id=new_user.id)
        else:
            messages.error(request, 'Error saving user.')
            return redirect("new_user")

    new_user_data_form = new_user_form.NewUserDataForm()
    users = logged_in_user.organizationmembers_set.all()
    user_organizations = logged_in_user.organization_created_by.all()
    return render(request=request, template_name="user/new_user_template.html", context={
        'logged_in_user': logged_in_user,
        'new_user_form': new_user_data_form,
        'users': users,
        'user_organizations': user_organizations
    })
