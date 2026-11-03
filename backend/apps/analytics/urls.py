from django.urls import path
from .views import (
    DashboardAnalyticsView, ConstituencyAnalyticsView,
    CompareConstituenciesView, ElectionTrendsAnalyticsView, PartyPerformanceAnalyticsView
)

urlpatterns = [
    path('dashboard/', DashboardAnalyticsView.as_view(), name='analytics-dashboard'),
    path('constituency/<int:pk>/', ConstituencyAnalyticsView.as_view(), name='analytics-constituency'),
    path('compare/', CompareConstituenciesView.as_view(), name='analytics-compare'),
    path('election-trends/', ElectionTrendsAnalyticsView.as_view(), name='analytics-election-trends'),
    path('party-performance/', PartyPerformanceAnalyticsView.as_view(), name='analytics-party-performance'),
]

