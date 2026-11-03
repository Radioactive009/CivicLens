import pandas as pd
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Dataset, DatasetImportJob
from .serializers import DatasetSerializer, DatasetImportJobSerializer
from .services import process_dataset_file
from apps.accounts.permissions import IsAnalystOrAdmin

class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all().prefetch_related('import_jobs')
    serializer_class = DatasetSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['dataset_type', 'processing_status', 'reference_year']
    search_fields = ['dataset_name', 'file_name', 'geographical_coverage']
    ordering_fields = ['created_at', 'reference_year', 'row_count']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'reprocess']:
            return [IsAnalystOrAdmin()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        f = self.request.FILES.get('file')
        file_name = f.name if f else 'unnamed'
        file_type = file_name.split('.')[-1].lower() if '.' in file_name else 'csv'
        user = self.request.user if self.request.user.is_authenticated else None
        dataset = serializer.save(uploaded_by=user, file_name=file_name, file_type=file_type)
        # Execute immediate processing for responsive local demo
        process_dataset_file(dataset.id)

    @action(detail=True, methods=['get'])
    def preview(self, request, pk=None):
        dataset = self.get_object()
        try:
            path = dataset.file.path
            if dataset.file_type == 'csv' or path.endswith('.csv'):
                df = pd.read_csv(path, nrows=10)
            elif dataset.file_type in ['xlsx', 'xls'] or path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(path, nrows=10)
            elif dataset.file_type == 'json' or path.endswith('.json'):
                df = pd.read_json(path)
                df = df.head(10)
            else:
                df = pd.read_csv(path, nrows=10)

            # Convert non-serializable elements to string or null
            records = df.fillna('').to_dict(orient='records')
            return Response({
                'columns': list(df.columns),
                'total_rows_estimate': dataset.row_count,
                'preview_rows': records
            })
        except Exception as e:
            return Response({'error': f"Failed to preview dataset: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def reprocess(self, request, pk=None):
        dataset = self.get_object()
        success, message = process_dataset_file(dataset.id)
        return Response({'success': success, 'message': message})

class DatasetImportJobViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DatasetImportJob.objects.all().select_related('dataset')
    serializer_class = DatasetImportJobSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['dataset', 'status']
    ordering_fields = ['started_at', 'completed_at']

