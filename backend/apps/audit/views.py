from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import AuditLog
from .serializers import AuditLogSerializer
from apps.accounts.serializers import UserSerializer
from apps.accounts.permissions import IsAdminUser

User = get_user_model()

class UserAdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all().select_related('user')
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdminUser]
    filterset_fields = ['action', 'resource_type']
    search_fields = ['action', 'resource_type', 'resource_id', 'user__username']
