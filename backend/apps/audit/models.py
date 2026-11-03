from django.db import models
from django.conf import settings

class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    action = models.CharField(max_length=50)
    resource_type = models.CharField(max_length=50)
    resource_id = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'cl_audit_logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['action', 'resource_type']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"[{self.timestamp}] {self.user} - {self.action} on {self.resource_type}:{self.resource_id}"

