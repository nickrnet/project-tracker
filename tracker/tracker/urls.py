from django.urls import include, path

from health_check.views import HealthCheckView


urlpatterns = [
    path('', include('frontend.urls')),
    path('api/', include('api.urls')),
    path('ht/', HealthCheckView.as_view()),
    ]
