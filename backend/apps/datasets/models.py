from django.db import models
from django.conf import settings
from apps.demographics.models import DataSource

class Dataset(models.Model):
    class ProcessingStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending Processing'
        PROCESSING = 'PROCESSING', 'Processing Ingestion'
        COMPLETED = 'COMPLETED', 'Successfully Imported'
        FAILED = 'FAILED', 'Import Failed'

    class DatasetType(models.TextChoices):
        ELECTIONS = 'ELECTIONS', 'Election Results'
        DEMOGRAPHICS = 'DEMOGRAPHICS', 'Demographic & Socioeconomic Indicators'
        CONSTITUENCIES = 'CONSTITUENCIES', 'Constituency & Boundary Records'
        NEWS = 'NEWS', 'Public Intelligence Feeds'

    dataset_name = models.CharField(max_length=200)
    dataset_type = models.CharField(max_length=30, choices=DatasetType.choices, default=DatasetType.ELECTIONS)
    source = models.ForeignKey(DataSource, on_delete=models.SET_NULL, null=True, blank=True, related_name='datasets')
    source_label = models.CharField(max_length=150, default='Official Statistical Archive')
    file = models.FileField(upload_to='datasets/%Y/%m/')
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=20, default='csv', help_text="csv, xlsx, json")
    geographical_coverage = models.CharField(max_length=100, default='Haryana, India')
    reference_year = models.IntegerField(default=2024)
    processing_status = models.CharField(max_length=20, choices=ProcessingStatus.choices, default=ProcessingStatus.PENDING)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='uploaded_datasets')
    row_count = models.IntegerField(default=0)
    validation_summary = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cl_datasets'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.dataset_name} ({self.processing_status})"

class DatasetImportJob(models.Model):
    class Status(models.TextChoices):
        QUEUED = 'QUEUED', 'Queued'
        PROCESSING = 'PROCESSING', 'Processing'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'

    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='import_jobs')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.QUEUED)
    total_records = models.IntegerField(default=0)
    successful_records = models.IntegerField(default=0)
    failed_records = models.IntegerField(default=0)
    error_log = models.JSONField(default=list, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'cl_dataset_import_jobs'
        ordering = ['-started_at']

    def __str__(self):
        return f"Job #{self.id} for {self.dataset.dataset_name} - {self.status}"

