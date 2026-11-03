from rest_framework import viewsets, filters, views
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Min, Max, Count
from .models import DataSource, DemographicIndicator
from .serializers import DataSourceSerializer, DemographicIndicatorSerializer

class DataSourceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer
    search_fields = ['source_name']

class DemographicIndicatorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DemographicIndicator.objects.all().select_related('source')
    serializer_class = DemographicIndicatorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'region_type', 'region_identifier', 'reference_year', 'name']
    search_fields = ['name', 'region_identifier', 'region_name']
    ordering_fields = ['reference_year', 'value', 'name']

class DemographicTrendsView(views.APIView):
    def get(self, request):
        indicator_name = request.query_params.get('name')
        region_id = request.query_params.get('region_identifier')
        category = request.query_params.get('category')

        qs = DemographicIndicator.objects.all()
        if indicator_name:
            qs = qs.filter(name__iexact=indicator_name)
        if region_id:
            qs = qs.filter(region_identifier=region_id)
        if category:
            qs = qs.filter(category=category)

        trends = (
            qs.values('reference_year', 'name', 'unit')
            .annotate(
                avg_value=Avg('value'),
                min_value=Min('value'),
                max_value=Max('value'),
                count=Count('id')
            )
            .order_by('reference_year')
        )
        return Response(list(trends))

class AvailableIndicatorsView(views.APIView):
    def get(self, request):
        indicators = (
            DemographicIndicator.objects.values('name', 'category', 'unit')
            .distinct()
            .order_by('category', 'name')
        )
        return Response(list(indicators))

