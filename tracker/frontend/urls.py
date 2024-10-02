import uuid

from django.urls import path, register_converter

from frontend.views import login_view
from frontend.views import logout_view
from frontend.views.project.git_repository import git_repository_view
from frontend.views.project.git_repository import git_repositories_view
from frontend.views.project.git_repository import new_git_repository_view
from frontend.views.core.organization import organization_view
from frontend.views.core.organization import organizations_view
from frontend.views.core.organization import new_organization_view
from frontend.views.project.project import project_view
from frontend.views.project.project import project_settings_view
from frontend.views.project.project import project_settings_git_repository_view as project_settings_git_repository_view
from frontend.views.project.project import project_settings_new_git_repository_view
from frontend.views.project.project import projects_view
from frontend.views.project.project import new_git_repository_view as new_project_git_repository_view
from frontend.views.project.project import new_project_new_git_repository_view as new_project_new_git_repository_view
from frontend.views.project.project import new_issue_view as new_project_issue_view
from frontend.views.project.project import new_project_view
from frontend.views.project.issue import issue_view
from frontend.views.project.issue import issues_view
from frontend.views.project.issue import new_issue_view
from frontend.views.core.user import user_view
from frontend.views.core.user import users_view
from frontend.views.core.user import new_user_view
from frontend.views import signup_view


class UUIDOrLabelConverter:
    regex = '[0-9a-fA-F-]{36}|[a-zA-Z0-9_-]+'

    def to_python(self, value):
        try:
            return uuid.UUID(value)
        except ValueError:
            return value

    def to_url(self, value):
        return str(value)


register_converter(UUIDOrLabelConverter, 'uuid_or_label')

urlpatterns = [
    # TODO: Audit these to make sure they're all still hit
    path('', login_view.login_to_app, name='index'),

    path('signup', signup_view.signup, name='signup'),
    path('login', login_view.login_to_app, name='login'),
    path('logout', logout_view.logout_of_app, name='logout'),

    path('new_project', new_project_view.new_project, name='new_project'),
    path('projects', projects_view.projects, name='projects'),
    path('project/<uuid_or_label:project_id>/', project_view.project, name='project'),
    path('project/new_git_repository/', new_project_git_repository_view.new_git_repository, name='new_project_git_repository'),
    path('project/new_git_repository/<uuid_or_label:project_id>/', new_project_git_repository_view.new_git_repository, name='new_project_git_repository'),
    path('project/new_project_new_git_repository/', new_project_new_git_repository_view.new_git_repository, name='new_project_new_git_repository'),
    path('project/new_issue/', new_project_issue_view.new_issue, name='new_project_issue'),
    path('project/new_issue/<uuid_or_label:project_id>/', new_project_issue_view.new_issue, name='new_project_issue'),

    path('project-settings/<uuid_or_label:project_id>/', project_settings_view.project_settings, name='project_settings'),
    path('project-settings/git-repository/', project_settings_git_repository_view.git_repository, name='project_settings_git_repository'),
    path('project-settings/git-repository/<uuid:git_repository_id>/', project_settings_git_repository_view.git_repository, name='project_settings_git_repository'),
    path('project-settings/new-git-repository/', project_settings_new_git_repository_view.new_git_repository, name='project_settings_new_git_repository'),
    path('project-settings/new-git-repository/<uuid_or_label:project_id>/', project_settings_new_git_repository_view.new_git_repository, name='project_settings_new_git_repository'),

    path('new_git_repository', new_git_repository_view.new_git_repository, name='new_git_repository'),
    path('git_repositories', git_repositories_view.git_repositories, name='git_repositories'),
    path('git_repository/<uuid:git_repository_id>/', git_repository_view.git_repository, name='git_repository'),

    path('new_issue/', new_issue_view.new_issue, name='new_issue'),
    path('new_issue/<uuid_or_label:project_id>/', new_issue_view.new_issue, name='new_issue'),
    path('issues', issues_view.issues, name='issues'),
    path('issue/<uuid:issue_id>/', issue_view.issue, name='issue'),

    path('new_organization', new_organization_view.new_organization, name='new_organization'),
    path('organizations', organizations_view.organizations, name='organizations'),
    path('organization/<uuid:organization_id>/', organization_view.organization, name='organization'),

    path('new_user', new_user_view.new_user, name='new_user'),
    path('users', users_view.users, name='users'),
    path('user/<uuid:user_id>/', user_view.user, name='user'),
]
