from django.urls import include, path
from rest_framework import routers

from api.views import user as user_api_view
from api.views import organization as organization_api_view
from api.views import project as project_api_view


router = routers.DefaultRouter()
router.register(r'users', user_api_view.UserViewSet)
router.register(r'git_repositories', project_api_view.GitRepositoryViewSet)
router.register(r'organizations', organization_api_view.OrganizationViewSet)
router.register(r'built_in_issue_priorities', project_api_view.BuiltInIssuePriorityViewSet)
router.register(r'built_in_issue_statuses', project_api_view.BuiltInIssueStatusViewSet)
router.register(r'built_in_issue_types', project_api_view.BuiltInIssueTypeViewSet)
router.register(r'custom_issue_priorities', project_api_view.CustomIssuePriorityViewSet)
router.register(r'custom_issue_statuses', project_api_view.CustomIssueStatusViewSet)
router.register(r'custom_issue_types', project_api_view.CustomIssueTypeViewSet)
router.register(r'issues', project_api_view.IssueViewSet)
router.register(r'projects', project_api_view.ProjectViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
