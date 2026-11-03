from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsArticleViewSet, IntelligenceTrendsView, GeographicDistributionView, CategoriesListView

router = DefaultRouter()
router.register(r'articles', NewsArticleViewSet, basename='news-articles')

urlpatterns = [
    path('trends/', IntelligenceTrendsView.as_view(), name='intelligence-trends'),
    path('geographic-distribution/', GeographicDistributionView.as_view(), name='intelligence-geo-dist'),
    path('categories/', CategoriesListView.as_view(), name='intelligence-categories'),
    path('', include(router.urls)),
]

