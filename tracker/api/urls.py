from django.urls import include, path
from rest_framework import routers

from api.views import api as api_view

router = routers.DefaultRouter()
router.register(r'core_users', api_view.CoreUserViewSet)
router.register(r'users', api_view.UserViewSet)
router.register(r'groups', api_view.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
