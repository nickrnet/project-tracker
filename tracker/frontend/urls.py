from django.urls import path

from frontend.views import login_view
from frontend.views import logout_view
from frontend.views.git_repository import git_repository_view
from frontend.views.git_repository import git_repositories_view
from frontend.views.git_repository import new_git_repository_view
from frontend.views.organization import organization_view
from frontend.views.organization import organizations_view
from frontend.views.organization import new_organization_view
from frontend.views.project import project_view
from frontend.views.project import projects_view
from frontend.views.project import new_project_view
from frontend.views.user import user_view
from frontend.views.user import users_view
from frontend.views.user import new_user_view
from frontend.views import signup_view


urlpatterns = [
    path('', login_view.login_to_app, name='index'),
    path('login', login_view.login_to_app, name='login'),
    path('logout', logout_view.logout_of_app, name='logout'),
    path('git_repository/<uuid:git_repository_id>/', git_repository_view.git_repository, name='git_repository'),
    path('git_repositories', git_repositories_view.git_repositories, name='git_repositories'),
    path('new_git_repository', new_git_repository_view.new_git_repository, name='new_git_repository'),
    path('organization/<uuid:organization_id>/', organization_view.organization, name='organization'),
    path('organizations', organizations_view.organizations, name='organizations'),
    path('new_organization', new_organization_view.new_organization, name='new_organization'),
    path('project/<uuid:project_id>/', project_view.project, name='project'),
    path('projects', projects_view.projects, name='projects'),
    path('new_project', new_project_view.new_project, name='new_project'),
    path('user/<uuid:user_id>/', user_view.user, name='user'),
    path('users', users_view.users, name='users'),
    path('new_user', new_user_view.new_user, name='new_user'),
    path('signup', signup_view.signup, name='signup')
]
