from django.contrib import admin
from .models import Dataset, DatasetImportJob

class ImportJobInline(admin.TabularInline):
    model = DatasetImportJob
    extra = 0
    readonly_fields = ('started_at', 'completed_at', 'status', 'total_records', 'successful_records', 'failed_records')

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ('dataset_name', 'dataset_type', 'geographical_coverage', 'reference_year', 'processing_status', 'uploaded_by', 'created_at')
    list_filter = ('dataset_type', 'processing_status', 'reference_year')
    search_fields = ('dataset_name', 'file_name')
    inlines = [ImportJobInline]

@admin.register(DatasetImportJob)
class DatasetImportJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'dataset', 'status', 'total_records', 'successful_records', 'failed_records', 'started_at')
    list_filter = ('status',)

