from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import State, District, Constituency
from .serializers import StateSerializer, DistrictSerializer, ConstituencySerializer, ConstituencyDetailSerializer
from apps.accounts.permissions import IsAnalystOrAdmin

class StateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = State.objects.all().prefetch_related('districts', 'constituencies')
    serializer_class = StateSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'state_code']
    ordering_fields = ['name', 'state_code']

class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = District.objects.all().select_related('state')
    serializer_class = DistrictSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['state', 'state__state_code']
    search_fields = ['name', 'district_code']
    ordering_fields = ['name']

class ConstituencyViewSet(viewsets.ModelViewSet):
    queryset = Constituency.objects.all().select_related('state', 'district')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['state', 'state__state_code', 'district', 'constituency_type', 'is_reserved']
    search_fields = ['name', 'constituency_code', 'district__name', 'state__name']
    ordering_fields = ['name', 'constituency_code']

    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return ConstituencyDetailSerializer
        return ConstituencySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAnalystOrAdmin()]
        return [permissions.AllowAny()]

