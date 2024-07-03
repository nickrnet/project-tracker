from django.urls import path

from frontend.views import login_view as login_view
from frontend.views import logout_view as logout_view
from frontend.views import new_git_repository_view as new_git_repository_view
from frontend.views import new_project_view as new_project_view
from frontend.views import new_user_view as new_user_view


urlpatterns = [
    path('', login_view.login_to_app, name='index'),
    path('login', login_view.login_to_app, name='login'),
    path('logout', logout_view.logout_of_app, name='logout'),
    path('new_git_repository', new_git_repository_view.new_git_repository, name='new_git_repository'),
    path('new_project', new_project_view.new_project, name='new_project'),
    path('new_user', new_user_view.new_user, name='new_user'),
]
