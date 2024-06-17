from django.urls import include, path
from rest_framework import routers

from api.views import api as api_view


router = routers.DefaultRouter()
router.register(r'core_users', api_view.CoreUserViewSet)
router.register(r'git_repositories', api_view.GitRepositoryViewSet)
router.register(r'projects', api_view.ProjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
