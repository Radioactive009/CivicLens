from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GeneratedReportViewSet

router = DefaultRouter()
router.register(r'', GeneratedReportViewSet, basename='reports')

urlpatterns = [
    path('generate/', GeneratedReportViewSet.as_view({'post': 'create'}), name='report-generate'),
    path('', include(router.urls)),
]

