from django.contrib import admin
from .models import DataSource, DemographicIndicator

@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    list_display = ('source_name', 'source_type', 'license_information', 'created_at')
    search_fields = ('source_name',)

@admin.register(DemographicIndicator)
class DemographicIndicatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'region_type', 'region_identifier', 'value', 'unit', 'reference_year')
    list_filter = ('category', 'region_type', 'reference_year')
    search_fields = ('name', 'region_identifier', 'region_name')

