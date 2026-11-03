from rest_framework import serializers
from .models import GeneratedReport

class GeneratedReportSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True, default='Anonymous')

    class Meta:
        model = GeneratedReport
        fields = [
            'id', 'title', 'report_type', 'file_format', 'report_parameters',
            'file_path', 'status', 'file_size_bytes', 'user', 'user_name', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'file_path', 'status', 'file_size_bytes', 'created_at']

