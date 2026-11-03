from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DatasetViewSet, DatasetImportJobViewSet

router = DefaultRouter()
router.register(r'import-jobs', DatasetImportJobViewSet, basename='dataset-import-jobs')
router.register(r'', DatasetViewSet, basename='datasets')

urlpatterns = [
    path('upload/', DatasetViewSet.as_view({'post': 'create'}), name='dataset-upload'),
    path('', include(router.urls)),
]

