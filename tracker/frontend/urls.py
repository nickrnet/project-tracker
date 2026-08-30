import uuid

from django.http import HttpResponse
from django.urls import path, register_converter
# from django.urls.converters import get_converters

from frontend.views.signup_view import SignupView
from frontend.views import login_view
from frontend.views import logout_view
from frontend.views.project.git_repository import git_repository_view
from frontend.views.project.git_repository import git_repositories_view
from frontend.views.project.git_repository import new_git_repository_view
from frontend.views.core.organization import organization_view
from frontend.views.core.organization import organizations_view
from frontend.views.core.organization import new_organization_view
from frontend.views.core.organization import organization_accept_invite_view
from frontend.views.core.organization import organization_settings_view
from frontend.views.core.organization import organization_settings_user_select_view
from frontend.views.core.organization import organization_settings_invite_user_view
from frontend.views.project.project import project_view
from frontend.views.project.project import check_project_label_availability_view
from frontend.views.project.project import project_settings_view
from frontend.views.project.project import project_settings_git_repository_view as project_settings_git_repository_view
from frontend.views.project.project import project_settings_component_view
from frontend.views.project.project import project_settings_new_component_view
from frontend.views.project.project import project_settings_version_view
from frontend.views.project.project import project_settings_new_version_view
from frontend.views.project.project import project_settings_new_git_repository_view
from frontend.views.project.project import project_settings_user_select_view
from frontend.views.project.project import projects_view
from frontend.views.project.project import issue_view as project_issue_view
from frontend.views.project.project import new_issue_view as new_project_issue_view
from frontend.views.project.project import new_project_view
from frontend.views.project.issue import issue_view
from frontend.views.project.issue import issues_view
from frontend.views.project.issue import new_issue_view
from frontend.views.core.user import user_view
from frontend.views.core.user import users_view
from frontend.views.core.user import new_user_view


def squash_google_chrome_dev_tools(request):
    return HttpResponse(status=204)


class UUIDOrLabelConverter:
    regex = '[0-9a-fA-F-]{36}|[a-zA-Z0-9_-]+'

    def to_python(self, value):
        try:
            return uuid.UUID(value)
        except ValueError:
            return value

    def to_url(self, value):
        return str(value)


# if "uuid_or_label" not in get_converters():
#     register_converter(UUIDOrLabelConverter, 'uuid_or_label')
register_converter(UUIDOrLabelConverter, 'uuid_or_label')

urlpatterns = [
    # These are URL paths that don't mean anything to us
    # Stupid Chrome
    path('.well-known/appspecific/com.chrome.devtools.json', squash_google_chrome_dev_tools),


    # TODO: Audit these to make sure they're all still hit/legit

    # These are the "endpoints" in Project Tracker
    path('', login_view.LoginView.as_view(), name='index'),
    path('signup', SignupView.as_view(), name='signup'),
    path('login', login_view.LoginView.as_view(), name='login'),
    path('logout', logout_view.LogoutView.as_view(), name='logout'),

    # Project
    path('check_project_label_availability/', check_project_label_availability_view.CheckProjectLabelAvailabilityView.as_view(), name='check_project_label_availability'),
    path('check_project_label_availability/<slug:label_text>/', check_project_label_availability_view.CheckProjectLabelAvailabilityView.as_view, name='check_project_label_availability'),
    path('projects', projects_view.ProjectsView.as_view(), name='projects'),
    path('projects/new_project', new_project_view.NewProjectView.as_view(), name='new_project'),
    path('project/<uuid_or_label:project_id>/', project_view.ProjectView.as_view(), name='project'),
    path('project/<uuid_or_label:project_id>/issue/', project_issue_view.IssueView.as_view(), name='project_issue'),
    path('project/<uuid_or_label:project_id>/issue/<uuid_or_label:issue_id>/', project_issue_view.IssueView.as_view(), name='project_issue'),
    path('project/<uuid_or_label:project_id>/new_issue/', new_project_issue_view.NewIssueView.as_view(), name='new_project_issue'),
    # Project Settings modal(s)
    path('project/<uuid_or_label:project_id>/project-settings/', project_settings_view.ProjectSettingsView.as_view(), name='project_settings'),
    path('project/<uuid_or_label:project_id>/project-settings/git-repository/', project_settings_git_repository_view.GitRepositoryView.as_view(), name='project_settings_git_repository'),
    path('project/<uuid_or_label:project_id>/project-settings/git-repository/<uuid_or_label:git_repository_id>/', project_settings_git_repository_view.GitRepositoryView.as_view(), name='project_settings_git_repository'),
    path('project/<uuid_or_label:project_id>/project-settings/new-git-repository/', project_settings_new_git_repository_view.ProjectSettingsNewGitRepositoryView.as_view(), name='project_settings_new_git_repository'),
    path('project/<uuid_or_label:project_id>/project-settings/component/<uuid_or_label:component_id>/', project_settings_component_view.ComponentView.as_view(), name='project_settings_component'),
    path('project/<uuid_or_label:project_id>/project-settings/new-component/', project_settings_new_component_view.NewComponentView.as_view(), name='project_settings_new_component'),
    path('project/<uuid_or_label:project_id>/project-settings/version/<uuid_or_label:version_id>/', project_settings_version_view.ProjectSettingsVersionView.as_view(), name='project_settings_version'),
    path('project/<uuid_or_label:project_id>/project-settings/new-version/', project_settings_new_version_view.NewVersionView.as_view(), name='project_settings_new_version'),
    path('project/<uuid_or_label:project_id>/project-settings/user-select/', project_settings_user_select_view.ProjectSettingUserSelectView.as_view(), name='project_settings_user_select'),

    # Git Repository
    path('new_git_repository', new_git_repository_view.NewGitRepositoryView.as_view(), name='new_git_repository'),
    path('git_repositories', git_repositories_view.GitRepositoriesView.as_view(), name='git_repositories'),
    path('git_repository/<uuid_or_label:git_repository_id>/', git_repository_view.GitRepositoryView.as_view(), name='git_repository'),

    # Issue
    path('new_issue/', new_issue_view.NewIssueView.as_view(), name='new_issue'),
    path('new_issue/<uuid_or_label:project_id>/', new_issue_view.NewIssueView.as_view(), name='new_issue'),
    path('issues', issues_view.IssuesView.as_view(), name='issues'),
    path('issue/<uuid_or_label:issue_id>/', issue_view.IssueView.as_view(), name='issue'),

    # Organization
    path('new_organization', new_organization_view.NewOrganizationView.as_view(), name='new_organization'),
    path('organizations', organizations_view.OrganizationView.as_view(), name='organizations'),
    path('organization/<uuid_or_label:organization_id>/', organization_view.OrganizationView.as_view(), name='organization'),
    # Organization Settings modal
    path('organization/<uuid_or_label:organization_id>/organization-settings/', organization_settings_view.OrganizationSettingsView.as_view(), name='organization_settings'),
    path('organization/<uuid_or_label:organization_id>/organization-settings/user-select/', organization_settings_user_select_view.OrganizationUserSelectView.as_view(), name='organization_settings_user_select'),
    path('organization/<uuid_or_label:organization_id>/organization-settings/invite-user/', organization_settings_invite_user_view.OrganizationSettingsInviteUserView.as_view(), name='organization_settings_invite_user'),
    path('organization/<uuid_or_label:organization_id>/accept_organization_invite/<uuid_or_label:invite_id>/', organization_accept_invite_view.AcceptOrganizationInviteView.as_view(), name='accept_organization_invite'),

    # User
    path('users', users_view.UsersView.as_view(), name='users'),
    path('new_user', new_user_view.NewUserView.as_view(), name='new_user'),
    path('user/<uuid_or_label:user_id>/', user_view.UserView.as_view(), name='user'),
    ]
