from rest_framework import views, status, permissions
from rest_framework.response import Response
from apps.constituencies.models import Constituency
from apps.elections.models import Election, ElectionResult, PoliticalParty
from apps.demographics.models import DemographicIndicator
from .services import compute_dashboard_metrics, compute_constituency_comparison
from django.db.models import Sum, Count, Avg

class DashboardAnalyticsView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        data = compute_dashboard_metrics()
        return Response(data)

class ConstituencyAnalyticsView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk=None):
        try:
            c = Constituency.objects.select_related('state', 'district').get(pk=pk)
        except Constituency.DoesNotExist:
            return Response({'error': 'Constituency not found'}, status=status.HTTP_404_NOT_FOUND)

        elections = c.elections.order_by('-election_year').prefetch_related('results__candidate__party')
        el_data = []
        for el in elections:
            results = [
                {
                    'position': r.position,
                    'candidate': r.candidate.name,
                    'party': r.candidate.party.abbreviation if r.candidate.party else 'IND',
                    'party_color': r.candidate.party.color_hex if r.candidate.party else '#6B7280',
                    'votes': r.votes_received,
                    'vote_share': r.vote_share
                }
                for r in el.results.all()
            ]
            el_data.append({
                'election_id': el.id,
                'year': el.election_year,
                'turnout_percentage': el.turnout_percentage,
                'total_electors': el.total_electors,
                'total_votes_polled': el.total_votes_polled,
                'results': results
            })

        indicators = list(
            DemographicIndicator.objects.filter(
                region_identifier__in=[c.constituency_code, c.district.district_code if c.district else '']
            ).values('id', 'name', 'category', 'value', 'unit', 'reference_year', 'region_type')
        )

        return Response({
            'constituency': {
                'id': c.id,
                'name': c.name,
                'code': c.constituency_code,
                'state': c.state.name,
                'district': c.district.name if c.district else '',
                'type': c.get_constituency_type_display(),
                'is_reserved': c.is_reserved,
                'latitude': c.latitude,
                'longitude': c.longitude,
                'boundary_reference': c.boundary_reference
            },
            'elections': el_data,
            'demographics': indicators
        })

class CompareConstituenciesView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        ids = request.data.get('constituency_ids', [])
        if not ids or not isinstance(ids, list):
            return Response({'error': 'Please provide a list of constituency_ids'}, status=status.HTTP_400_BAD_REQUEST)
        
        comparison = compute_constituency_comparison(ids)
        return Response(comparison)

class ElectionTrendsAnalyticsView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        trends = list(
            Election.objects.values('election_year')
            .annotate(
                avg_turnout=Avg('turnout_percentage'),
                total_votes=Sum('total_votes_polled'),
                elections_count=Count('id')
            )
            .order_by('election_year')
        )
        return Response(trends)

class PartyPerformanceAnalyticsView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        year = request.query_params.get('year')
        qs = ElectionResult.objects.all()
        if year:
            qs = qs.filter(election__election_year=year)

        performance = list(
            qs.values('candidate__party__abbreviation', 'candidate__party__name', 'candidate__party__color_hex')
            .annotate(
                total_votes=Sum('votes_received'),
                total_contested=Count('id'),
                avg_vote_share=Avg('vote_share')
            )
            .order_by('-total_votes')
        )
        return Response(performance)

