from rest_framework import viewsets, filters, views
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Avg
from .models import NewsArticle
from .serializers import NewsArticleSerializer

class NewsArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'sentiment_label', 'geographic_reference']
    search_fields = ['title', 'description', 'keywords', 'geographic_reference']
    ordering_fields = ['published_at', 'sentiment_score']

class IntelligenceTrendsView(views.APIView):
    def get(self, request):
        geo = request.query_params.get('geographic_reference')
        qs = NewsArticle.objects.all()
        if geo:
            qs = qs.filter(geographic_reference__icontains=geo)

        by_category = (
            qs.values('category')
            .annotate(
                article_count=Count('id'),
                avg_sentiment=Avg('sentiment_score')
            )
            .order_by('-article_count')
        )

        by_sentiment = (
            qs.values('sentiment_label')
            .annotate(count=Count('id'))
        )

        return Response({
            'by_category': list(by_category),
            'by_sentiment': list(by_sentiment),
            'total_articles': qs.count()
        })

class GeographicDistributionView(views.APIView):
    def get(self, request):
        dist = (
            NewsArticle.objects.values('geographic_reference')
            .annotate(
                count=Count('id'),
                avg_sentiment=Avg('sentiment_score')
            )
            .order_by('-count')
        )
        return Response(list(dist))

class CategoriesListView(views.APIView):
    def get(self, request):
        return Response([
            {'key': choice[0], 'label': choice[1]}
            for choice in NewsArticle.Category.choices
        ])

