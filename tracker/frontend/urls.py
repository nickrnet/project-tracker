from django.urls import path

from frontend.views import new_user_view as new_user_view


urlpatterns = [
    path('new_user', new_user_view.homepage, name='new_user'),
]
