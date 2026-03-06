from django.urls import include, path

urlpatterns = [
    path('api/auth/', include('accounts.urls')),
    path('api/access/', include('access_control.urls')),
    path('api/business/', include('business_api.urls')),
]
