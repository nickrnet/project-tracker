from django.urls import include, path


urlpatterns = [
    path('', include('frontend.urls')),
    path('frontend/', include('frontend.urls')),
    path('api/', include('api.urls')),
]
