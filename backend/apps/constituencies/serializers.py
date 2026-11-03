from rest_framework import serializers
from .models import State, District, Constituency

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name', 'state', 'district_code', 'headquarters', 'latitude', 'longitude', 'created_at']

class StateSerializer(serializers.ModelSerializer):
    district_count = serializers.IntegerField(source='districts.count', read_only=True)
    constituency_count = serializers.IntegerField(source='constituencies.count', read_only=True)

    class Meta:
        model = State
        fields = ['id', 'name', 'state_code', 'capital', 'latitude', 'longitude', 'district_count', 'constituency_count', 'created_at']

class ConstituencySerializer(serializers.ModelSerializer):
    state_name = serializers.CharField(source='state.name', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True, default='')

    class Meta:
        model = Constituency
        fields = [
            'id', 'name', 'constituency_code', 'state', 'state_name',
            'district', 'district_name', 'constituency_type', 'boundary_reference',
            'latitude', 'longitude', 'is_reserved', 'geojson_data', 'created_at', 'updated_at'
        ]

class ConstituencyDetailSerializer(serializers.ModelSerializer):
    state = StateSerializer(read_only=True)
    district = DistrictSerializer(read_only=True)
    
    class Meta:
        model = Constituency
        fields = [
            'id', 'name', 'constituency_code', 'state', 'district',
            'constituency_type', 'boundary_reference', 'latitude', 'longitude',
            'is_reserved', 'geojson_data', 'created_at', 'updated_at'
        ]

