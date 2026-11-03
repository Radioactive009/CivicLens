import os
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import FileResponse, Http404
from django_filters.rest_framework import DjangoFilterBackend
from .models import GeneratedReport
from .serializers import GeneratedReportSerializer
from .services import build_pdf_report, build_excel_report, build_csv_report
from apps.accounts.permissions import IsResearcherOrHigher

class GeneratedReportViewSet(viewsets.ModelViewSet):
    queryset = GeneratedReport.objects.all()
    serializer_class = GeneratedReportSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['report_type', 'file_format', 'status']
    ordering_fields = ['created_at']

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        report = serializer.save(user=user, status=GeneratedReport.Status.GENERATING)
        try:
            if report.file_format == GeneratedReport.FileFormat.PDF:
                build_pdf_report(report)
            elif report.file_format == GeneratedReport.FileFormat.XLSX:
                build_excel_report(report)
            elif report.file_format == GeneratedReport.FileFormat.CSV:
                build_csv_report(report)
            else:
                build_pdf_report(report)
        except Exception as e:
            report.status = GeneratedReport.Status.FAILED
            report.save()

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        report = self.get_object()
        if not report.file_path or not os.path.exists(report.file_path):
            # Try to build on the fly if missing
            try:
                if report.file_format == 'xlsx':
                    build_excel_report(report)
                elif report.file_format == 'csv':
                    build_csv_report(report)
                else:
                    build_pdf_report(report)
            except Exception:
                raise Http404("Report file not found or could not be generated")

        content_types = {
            'pdf': 'application/pdf',
            'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'csv': 'text/csv'
        }
        ct = content_types.get(report.file_format, 'application/octet-stream')
        filename = os.path.basename(report.file_path)
        response = FileResponse(open(report.file_path, 'rb'), content_type=ct)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

