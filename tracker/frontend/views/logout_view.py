from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils import timezone

from core.util import validate_ip_address

from core.models import user as core_user_models


def logout_of_app(request):
    user = core_user_models.CoreUser.active_objects.get(user__username=request.user)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
    remote_addr = request.META.get('REMOTE_ADDR', '')
    core_user_models.UserLogout.objects.create(
        created_by=user,
        user=user,
        x_forwarded_for=validate_ip_address(x_forwarded_for).split(',')[0] if x_forwarded_for else None,
        remote_addr=validate_ip_address(remote_addr) if remote_addr else None,
        user_agent=request.META.get('HTTP_USER_AGENT', 'UNKNOWN'),
        logout_time=timezone.now(),
        session_key=request.session.session_key
        )
    logout(request)

    messages.success(request, ('You were successfully logged out!'))
    return redirect('login')
