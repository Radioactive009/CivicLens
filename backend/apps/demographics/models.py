from django.db import models

class DataSource(models.Model):
    source_name = models.CharField(max_length=150, unique=True)
    source_url = models.URLField(blank=True, default='')
    source_type = models.CharField(max_length=50, default='Official Government / Open Data')
    license_information = models.CharField(max_length=100, default='Open Government Data License - India')
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cl_data_sources'
        ordering = ['source_name']

    def __str__(self):
        return self.source_name

class DemographicIndicator(models.Model):
    class Category(models.TextChoices):
        DEMOGRAPHICS = 'DEMOGRAPHICS', 'Population & Demographics'
        LITERACY = 'LITERACY', 'Literacy & Education'
        EMPLOYMENT = 'EMPLOYMENT', 'Employment & Workforce'
        HEALTHCARE = 'HEALTHCARE', 'Healthcare & Wellbeing'
        INFRASTRUCTURE = 'INFRASTRUCTURE', 'Infrastructure & Public Services'
        SOCIOECONOMIC = 'SOCIOECONOMIC', 'Socioeconomic & Living Standards'

    class RegionType(models.TextChoices):
        STATE = 'STATE', 'State Level'
        DISTRICT = 'DISTRICT', 'District Level'
        CONSTITUENCY = 'CONSTITUENCY', 'Constituency Level'

    name = models.CharField(max_length=150, help_text="e.g. Total Population, Literacy Rate, Female Workforce Ratio")
    category = models.CharField(max_length=30, choices=Category.choices, default=Category.DEMOGRAPHICS)
    region_type = models.CharField(max_length=20, choices=RegionType.choices, default=RegionType.CONSTITUENCY)
    region_identifier = models.CharField(max_length=100, db_index=True, help_text="Constituency code, district code, or state code")
    region_name = models.CharField(max_length=150, blank=True, default='')
    value = models.FloatField(help_text="Numeric indicator value")
    unit = models.CharField(max_length=50, default='Count', help_text="%, Count, Per 1000, etc.")
    reference_year = models.IntegerField(db_index=True)
    source = models.ForeignKey(DataSource, on_delete=models.SET_NULL, null=True, blank=True, related_name='indicators')
    methodology = models.TextField(blank=True, default='Census of India / Directorate of Economics and Statistics statistical survey estimates.')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cl_demographic_indicators'
        unique_together = ('name', 'region_identifier', 'reference_year')
        ordering = ['-reference_year', 'name']
        indexes = [
            models.Index(fields=['category', 'region_type']),
            models.Index(fields=['region_identifier', 'reference_year']),
        ]

    def __str__(self):
        return f"{self.name}: {self.value} {self.unit} ({self.region_identifier}, {self.reference_year})"

