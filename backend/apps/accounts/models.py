from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrator'
        ANALYST = 'ANALYST', 'Analyst'
        RESEARCHER = 'RESEARCHER', 'Researcher'
        VIEWER = 'VIEWER', 'Viewer'

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.VIEWER)
    department = models.CharField(max_length=100, blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'cl_users'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.role})"

