from django.db import models

class State(models.Model):
    name = models.CharField(max_length=100, unique=True)
    state_code = models.CharField(max_length=10, unique=True)
    capital = models.CharField(max_length=100, blank=True, default='')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cl_states'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.state_code})"

class District(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='districts')
    district_code = models.CharField(max_length=20, unique=True)
    headquarters = models.CharField(max_length=100, blank=True, default='')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cl_districts'
        ordering = ['name']
        unique_together = ('state', 'name')

    def __str__(self):
        return f"{self.name}, {self.state.name}"

class Constituency(models.Model):
    class ConstituencyType(models.TextChoices):
        ASSEMBLY = 'AC', 'Assembly Constituency (Vidhan Sabha)'
        PARLIAMENTARY = 'PC', 'Parliamentary Constituency (Lok Sabha)'

    name = models.CharField(max_length=150)
    constituency_code = models.CharField(max_length=50, unique=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='constituencies')
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, related_name='constituencies')
    constituency_type = models.CharField(max_length=10, choices=ConstituencyType.choices, default=ConstituencyType.ASSEMBLY)
    boundary_reference = models.CharField(max_length=100, blank=True, default='')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    geojson_data = models.JSONField(blank=True, null=True, help_text="GeoJSON boundary polygon if available")
    is_reserved = models.CharField(max_length=20, default='GEN', help_text="GEN, SC, or ST")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cl_constituencies'
        ordering = ['name']
        indexes = [
            models.Index(fields=['state', 'district']),
            models.Index(fields=['constituency_type']),
        ]

    def __str__(self):
        return f"{self.name} ({self.constituency_code}) - {self.state.name}"

