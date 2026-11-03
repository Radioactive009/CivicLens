from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StateViewSet, DistrictViewSet, ConstituencyViewSet

router = DefaultRouter()
router.register(r'states', StateViewSet, basename='states')
router.register(r'districts', DistrictViewSet, basename='districts')
router.register(r'constituencies', ConstituencyViewSet, basename='constituencies')

urlpatterns = [
    path('', include(router.urls)),
]
