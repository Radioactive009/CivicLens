from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DataSourceViewSet, DemographicIndicatorViewSet, DemographicTrendsView, AvailableIndicatorsView

router = DefaultRouter()
router.register(r'sources', DataSourceViewSet, basename='data-sources')
router.register(r'', DemographicIndicatorViewSet, basename='demographics')

urlpatterns = [
    path('indicators/', AvailableIndicatorsView.as_view(), name='demographics-indicators'),
    path('trends/', DemographicTrendsView.as_view(), name='demographics-trends'),
    path('', include(router.urls)),
]

