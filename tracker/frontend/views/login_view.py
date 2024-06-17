from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect

from frontend.forms import login_form as login_form
from core.models import user as core_user_models


def login_to_app(request):
    if request.method == "POST":
        received_login_form = login_form.LoginForm(request.POST, request.FILES)
        if received_login_form.is_valid():
            user = authenticate(username=received_login_form.cleaned_data['email'], password=received_login_form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                try:
                    core_user_models.CoreUser.objects.get(user=user)
                except core_user_models.CoreUser.DoesNotExist:
                    print("User does not exist.")
                    messages.error(request, 'The user specified is not a valid user.')
                    return render(request=request, template_name="login_template.html", context={'login_form': login_form.LoginForm(data={'next': request.GET.get("next")})})
                return redirect(request.GET.get("next", '/frontend/new_user'))
            else:
                print("User not found.")
                messages.error(request, 'Error logging in.')
                return render(request=request, template_name="login_template.html", context={'login_form': login_form.LoginForm(data={'next': request.GET.get("next")})})
        else:
            print("Bad user data submitted.")
            messages.error(request, 'Error logging in.')
            return render(request=request, template_name="login_template.html", context={'login_form': login_form.LoginForm(data={'next': request.GET.get("next")})})

    return render(request=request, template_name="login_template.html", context={'login_form': login_form.LoginForm(data={'next': request.GET.get("next")})})
