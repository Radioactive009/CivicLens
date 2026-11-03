from django.db import models
from django.conf import settings

class GeneratedReport(models.Model):
    class ReportType(models.TextChoices):
        CONSTITUENCY_PROFILE = 'CONSTITUENCY_PROFILE', 'Constituency Analytical Profile'
        ELECTION_SUMMARY = 'ELECTION_SUMMARY', 'Historical Election Summary'
        COMPARISON = 'COMPARISON', 'Constituency Comparison Dossier'
        DEMOGRAPHIC_OVERVIEW = 'DEMOGRAPHIC_OVERVIEW', 'Demographic & Socioeconomic Digest'
        INTELLIGENCE_BRIEF = 'INTELLIGENCE_BRIEF', 'Public Issue Intelligence Brief'

    class FileFormat(models.TextChoices):
        PDF = 'pdf', 'PDF Document'
        CSV = 'csv', 'CSV Spreadsheets'
        XLSX = 'xlsx', 'Excel Workbook'

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        GENERATING = 'GENERATING', 'Generating'
        READY = 'READY', 'Ready for Download'
        FAILED = 'FAILED', 'Generation Failed'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='generated_reports')
    title = models.CharField(max_length=255)
    report_type = models.CharField(max_length=40, choices=ReportType.choices, default=ReportType.CONSTITUENCY_PROFILE)
    file_format = models.CharField(max_length=10, choices=FileFormat.choices, default=FileFormat.PDF)
    report_parameters = models.JSONField(default=dict, help_text="Filters and parameters used for generating report")
    file_path = models.CharField(max_length=500, blank=True, default='')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.READY)
    file_size_bytes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cl_generated_reports'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.report_type} - {self.file_format})"

