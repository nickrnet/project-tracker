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
                    messages.success(request, ('You were successfully logged in!'))
                    return redirect(request.GET.get("next", '/projects'))
                except core_user_models.CoreUser.DoesNotExist:
                    messages.error(request, 'Error logging in.')
                    return render(
                        request=request,
                        template_name="login_template.html",
                        context={
                            'login_form': login_form.LoginForm(data={'next': request.GET.get("next")})
                        }
                    )
            else:
                messages.error(request, 'Error logging in.')
                return render(
                    request=request,
                    template_name="login_template.html",
                    context={
                        'login_form': login_form.LoginForm(data={'next': request.GET.get("next")})
                    }
                )
        else:
            messages.error(request, 'Check the values you entered and try again.')
            return render(
                request=request,
                template_name="login_template.html",
                context={
                    'login_form': login_form.LoginForm(data={'next': request.GET.get("next")})
                }
            )

    return render(
        request=request,
        template_name="login_template.html",
        context={
            'login_form': login_form.LoginForm(data={'next': request.GET.get("next")})
        }
    )
