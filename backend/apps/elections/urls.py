from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PoliticalPartyViewSet, CandidateViewSet, ElectionViewSet,
    ElectionResultViewSet, TurnoutAnalyticsView, WinningMarginsView
)

router = DefaultRouter()
router.register(r'parties', PoliticalPartyViewSet, basename='parties')
router.register(r'candidates', CandidateViewSet, basename='candidates')
router.register(r'results', ElectionResultViewSet, basename='results')
router.register(r'', ElectionViewSet, basename='elections')

urlpatterns = [
    path('turnout/', TurnoutAnalyticsView.as_view(), name='election-turnout'),
    path('winning-margins/', WinningMarginsView.as_view(), name='election-winning-margins'),
    path('', include(router.urls)),
]

