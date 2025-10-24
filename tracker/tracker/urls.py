from django.urls import include, path


urlpatterns = [
    path('', include('frontend.urls')),
    path('api/', include('api.urls')),
    path(r'ht/', include('health_check.urls')),
    ]
