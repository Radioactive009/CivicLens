from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserAdminViewSet, AuditLogViewSet

router = DefaultRouter()
router.register(r'users', UserAdminViewSet, basename='admin-users')
router.register(r'audit-logs', AuditLogViewSet, basename='admin-audit-logs')

urlpatterns = [
    path('', include(router.urls)),
]

