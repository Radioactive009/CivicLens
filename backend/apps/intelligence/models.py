from django.db import models

class NewsArticle(models.Model):
    class Category(models.TextChoices):
        EDUCATION = 'EDUCATION', 'Education & Schools'
        HEALTHCARE = 'HEALTHCARE', 'Healthcare & Medical'
        EMPLOYMENT = 'EMPLOYMENT', 'Employment & Industry'
        AGRICULTURE = 'AGRICULTURE', 'Agriculture & Farming'
        INFRASTRUCTURE = 'INFRASTRUCTURE', 'Infrastructure & Roads'
        ENVIRONMENT = 'ENVIRONMENT', 'Environment & Water'
        TRANSPORTATION = 'TRANSPORTATION', 'Transportation & Transit'
        PUBLIC_SERVICES = 'PUBLIC_SERVICES', 'Public Services & Governance'

    class SentimentLabel(models.TextChoices):
        POSITIVE = 'POSITIVE', 'Constructive / Positive'
        NEUTRAL = 'NEUTRAL', 'Neutral / Informational'
        CONCERN = 'CONCERN', 'Public Concern / Critical'

    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, default='')
    content = models.TextField(blank=True, default='')
    source_name = models.CharField(max_length=150, default='The Tribune / Regional Press')
    article_url = models.URLField(max_length=800, unique=True)
    published_at = models.DateTimeField(db_index=True)
    category = models.CharField(max_length=30, choices=Category.choices, default=Category.PUBLIC_SERVICES)
    sentiment_label = models.CharField(max_length=20, choices=SentimentLabel.choices, default=SentimentLabel.NEUTRAL)
    sentiment_score = models.FloatField(default=0.0, help_text="Range: -1.0 (Critical) to +1.0 (Positive)")
    geographic_reference = models.CharField(max_length=100, default='Haryana', help_text="State or District name")
    keywords = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cl_news_articles'
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['category', 'sentiment_label']),
            models.Index(fields=['geographic_reference', 'published_at']),
        ]

    def __str__(self):
        return f"[{self.category}] {self.title[:60]}... ({self.source_name})"

