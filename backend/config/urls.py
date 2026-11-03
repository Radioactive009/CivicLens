from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # OpenAPI Schema & Docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # API v1 endpoints
    path('api/v1/auth/', include('apps.accounts.urls')),
    path('api/v1/', include('apps.constituencies.urls')),
    path('api/v1/elections/', include('apps.elections.urls')),
    path('api/v1/demographics/', include('apps.demographics.urls')),
    path('api/v1/analytics/', include('apps.analytics.urls')),
    path('api/v1/datasets/', include('apps.datasets.urls')),
    path('api/v1/intelligence/', include('apps.intelligence.urls')),
    path('api/v1/reports/', include('apps.reports.urls')),
    path('api/v1/admin/', include('apps.audit.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
