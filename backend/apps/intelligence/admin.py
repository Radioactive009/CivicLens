from django.contrib import admin
from .models import NewsArticle

@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'sentiment_label', 'sentiment_score', 'geographic_reference', 'published_at')
    list_filter = ('category', 'sentiment_label', 'geographic_reference')
    search_fields = ('title', 'description', 'keywords')

