from rest_framework import serializers
from .models import Dataset, DatasetImportJob
from apps.accounts.serializers import UserSerializer

class DatasetImportJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetImportJob
        fields = ['id', 'dataset', 'status', 'total_records', 'successful_records', 'failed_records', 'error_log', 'started_at', 'completed_at']

class DatasetSerializer(serializers.ModelSerializer):
    uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True)
    import_jobs = DatasetImportJobSerializer(many=True, read_only=True)

    class Meta:
        model = Dataset
        fields = [
            'id', 'dataset_name', 'dataset_type', 'source', 'source_label',
            'file', 'file_name', 'file_type', 'geographical_coverage',
            'reference_year', 'processing_status', 'uploaded_by', 'uploaded_by_username',
            'row_count', 'validation_summary', 'import_jobs', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'uploaded_by', 'processing_status', 'row_count', 'validation_summary', 'created_at', 'updated_at']

