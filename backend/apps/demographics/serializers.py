from rest_framework import serializers
from .models import DataSource, DemographicIndicator

class DataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        fields = ['id', 'source_name', 'source_url', 'source_type', 'license_information', 'description', 'created_at']

class DemographicIndicatorSerializer(serializers.ModelSerializer):
    source_name = serializers.CharField(source='source.source_name', read_only=True, default='Official Statistical Surveys')

    class Meta:
        model = DemographicIndicator
        fields = [
            'id', 'name', 'category', 'region_type', 'region_identifier',
            'region_name', 'value', 'unit', 'reference_year', 'source',
            'source_name', 'methodology', 'created_at'
        ]

