from rest_framework import serializers
from .models import NewsArticle

class NewsArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsArticle
        fields = [
            'id', 'title', 'description', 'content', 'source_name',
            'article_url', 'published_at', 'category', 'sentiment_label',
            'sentiment_score', 'geographic_reference', 'keywords', 'created_at'
        ]

