from django.contrib import admin
from .models import GeneratedReport

@admin.register(GeneratedReport)
class GeneratedReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'report_type', 'file_format', 'status', 'user', 'file_size_bytes', 'created_at')
    list_filter = ('report_type', 'file_format', 'status')
    search_fields = ('title', 'user__username')

