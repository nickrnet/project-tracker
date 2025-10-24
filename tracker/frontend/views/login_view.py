from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone

from core.util import validate_ip_address

from frontend.forms import login_form as login_form
from core.models import user as core_user_models


def handle_post(request):
    received_login_form = login_form.LoginForm(request.POST, request.FILES)
    if received_login_form.is_valid():
        user = authenticate(username=received_login_form.cleaned_data['email'], password=received_login_form.cleaned_data['password'])
        if user is not None:
            login(request, user)
            core_user = core_user_models.CoreUser.active_objects.get(user=user)
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
            remote_addr = request.META.get('REMOTE_ADDR', '')
            core_user_models.UserLogin.objects.create(
                created_by=core_user,
                created_on=timezone.now(),
                user=core_user,
                x_forwarded_for=validate_ip_address(x_forwarded_for).split(',')[0] if x_forwarded_for else None,
                remote_addr=validate_ip_address(remote_addr) if remote_addr else None,
                user_agent=request.META.get('HTTP_USER_AGENT', 'UNKNOWN'),
                login_time=timezone.now(),
                session_key=request.session.session_key
                )
            messages.success(request, ('You were successfully logged in!'))

            return redirect(request.GET.get("next", '/projects'))
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
        messages.error(request, 'Error logging in.')

        return render(
            request=request,
            template_name="login_template.html",
            context={
                'login_form': login_form.LoginForm(data={'next': request.GET.get("next")})
                }
            )


def login_to_app(request):
    if request.method == "POST":
        return handle_post(request)

    return render(
        request=request,
        template_name="login_template.html",
        context={
            'login_form': login_form.LoginForm(data={'next': request.GET.get("next")})
            }
        )
