from rest_framework import viewsets, filters, views
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Sum, Count, F
from .models import PoliticalParty, Candidate, Election, ElectionResult
from .serializers import PoliticalPartySerializer, CandidateSerializer, ElectionSerializer, ElectionDetailSerializer, ElectionResultSerializer

class PoliticalPartyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PoliticalParty.objects.all()
    serializer_class = PoliticalPartySerializer
    search_fields = ['name', 'abbreviation']
    ordering_fields = ['name']

class CandidateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Candidate.objects.all().select_related('party')
    serializer_class = CandidateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['party']
    search_fields = ['name', 'candidate_reference']

class ElectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Election.objects.all().select_related('state', 'constituency', 'constituency__district').prefetch_related('results__candidate__party')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['election_year', 'election_type', 'state', 'constituency']
    search_fields = ['election_name', 'constituency__name']
    ordering_fields = ['election_year', 'turnout_percentage']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ElectionDetailSerializer
        return ElectionSerializer

class ElectionResultViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ElectionResult.objects.all().select_related('election', 'candidate', 'candidate__party')
    serializer_class = ElectionResultSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['election', 'election__election_year', 'candidate__party', 'position']
    ordering_fields = ['position', 'votes_received', 'vote_share']

class TurnoutAnalyticsView(views.APIView):
    def get(self, request):
        state_id = request.query_params.get('state')
        election_type = request.query_params.get('election_type')
        qs = Election.objects.all()
        if state_id:
            qs = qs.filter(state_id=state_id)
        if election_type:
            qs = qs.filter(election_type=election_type)

        turnout_by_year = (
            qs.values('election_year')
            .annotate(
                avg_turnout=Avg('turnout_percentage'),
                total_votes=Sum('total_votes_polled'),
                total_electors=Sum('total_electors'),
                constituencies_count=Count('id')
            )
            .order_by('election_year')
        )
        return Response(list(turnout_by_year))

class WinningMarginsView(views.APIView):
    def get(self, request):
        election_year = request.query_params.get('year')
        qs = Election.objects.all()
        if election_year:
            qs = qs.filter(election_year=election_year)
        
        results = []
        for election in qs.select_related('constituency', 'state').prefetch_related('results__candidate__party')[:50]:
            res = list(election.results.all())
            if len(res) >= 2:
                margin = res[0].votes_received - res[1].votes_received
                margin_share = round((margin / res[0].total_valid_votes * 100) if res[0].total_valid_votes else 0, 2)
                results.append({
                    'election_id': election.id,
                    'constituency_name': election.constituency.name,
                    'winner': res[0].candidate.name,
                    'winner_party': res[0].candidate.party.abbreviation if res[0].candidate.party else 'IND',
                    'runner_up': res[1].candidate.name,
                    'runner_up_party': res[1].candidate.party.abbreviation if res[1].candidate.party else 'IND',
                    'winning_margin_votes': margin,
                    'margin_percentage': margin_share,
                    'year': election.election_year
                })
        return Response(results)

