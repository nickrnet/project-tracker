from django.urls import include, path
from rest_framework import routers

from api.views import user as user_api_view
from api.views import organization as organization_api_view
from api.views import project as project_api_view


router = routers.DefaultRouter()

# We want these in this order
router.register(r'projects', project_api_view.ProjectViewSet)
router.register(r'issues', project_api_view.IssueViewSet)
router.register(r'git_repositories', project_api_view.GitRepositoryViewSet)
router.register(r'organizations', organization_api_view.OrganizationViewSet)
router.register(r'users', user_api_view.CoreUserViewSet)

router.register(r'components', project_api_view.ComponentViewSet)
router.register(r'versions', project_api_view.VersionViewSet)
router.register(r'built_in_issue_priorities', project_api_view.BuiltInIssuePriorityViewSet)
router.register(r'built_in_issue_severities', project_api_view.BuiltInIssueSeverityViewSet)
router.register(r'built_in_issue_statuses', project_api_view.BuiltInIssueStatusViewSet)
router.register(r'built_in_issue_types', project_api_view.BuiltInIssueTypeViewSet)
router.register(r'custom_issue_priorities', project_api_view.CustomIssuePriorityViewSet)
router.register(r'custom_issue_severities', project_api_view.CustomIssueSeverityViewSet)
router.register(r'custom_issue_statuses', project_api_view.CustomIssueStatusViewSet)
router.register(r'custom_issue_types', project_api_view.CustomIssueTypeViewSet)

router.register(r'project_data', project_api_view.ProjectDataViewSet)
router.register(r'issue_data', project_api_view.IssueDataViewSet)
router.register(r'git_repository_data', project_api_view.GitRepositoryDataViewSet)
router.register(r'organization_data', organization_api_view.OrganizationDataViewSet)
router.register(r'user_data', user_api_view.UserDataViewSet)
router.register(r'component_data', project_api_view.ComponentDataViewSet)
router.register(r'version_data', project_api_view.VersionDataViewSet)
router.register(r'custom_issue_priority_data', project_api_view.CustomIssuePriorityDataViewSet)
router.register(r'custom_issue_severity_data', project_api_view.CustomIssueSeverityDataViewSet)
router.register(r'custom_issue_status_data', project_api_view.CustomIssueStatusDataViewSet)
router.register(r'custom_issue_type_data', project_api_view.CustomIssueTypeDataViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
