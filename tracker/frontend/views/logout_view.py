from django.contrib.auth import logout
from django.shortcuts import redirect


def logout_of_app(request):
    logout(request)

    return redirect('login')
