from django.db.models import Avg, Sum, Count, F, Q
from apps.constituencies.models import State, District, Constituency
from apps.elections.models import Election, ElectionResult, PoliticalParty
from apps.demographics.models import DemographicIndicator
from apps.datasets.models import Dataset
from apps.intelligence.models import NewsArticle

def compute_dashboard_metrics():
    total_constituencies = Constituency.objects.count()
    total_states = State.objects.count()
    total_elections = Election.objects.count()
    total_results = ElectionResult.objects.count()
    total_datasets = Dataset.objects.count()
    total_indicators = DemographicIndicator.objects.count()
    total_articles = NewsArticle.objects.count()

    # Voter Turnout overview
    turnout_data = list(
        Election.objects.values('election_year')
        .annotate(
            avg_turnout=Avg('turnout_percentage'),
            total_votes=Sum('total_votes_polled'),
            total_electors=Sum('total_electors')
        )
        .order_by('election_year')
    )

    # Party-wise seat wins across latest election year
    latest_year = Election.objects.order_by('-election_year').values_list('election_year', flat=True).first()
    party_seats = []
    if latest_year:
        winning_results = ElectionResult.objects.filter(
            election__election_year=latest_year,
            position=1
        ).values('candidate__party__abbreviation', 'candidate__party__name', 'candidate__party__color_hex').annotate(
            seats_won=Count('id'),
            total_votes=Sum('votes_received')
        ).order_by('-seats_won')

        for ps in winning_results:
            party_seats.append({
                'party_abbrev': ps['candidate__party__abbreviation'] or 'IND',
                'party_name': ps['candidate__party__name'] or 'Independent',
                'color': ps['candidate__party__color_hex'] or '#6B7280',
                'seats_won': ps['seats_won'],
                'total_votes': ps['total_votes']
            })

    # Recent datasets
    recent_datasets = list(
        Dataset.objects.values(
            'id', 'dataset_name', 'dataset_type', 'processing_status', 'row_count', 'created_at'
        ).order_by('-created_at')[:5]
    )

    # Geographic distribution breakdown
    districts_summary = list(
        District.objects.values('name')
        .annotate(constituency_count=Count('constituencies'))
        .order_by('-constituency_count')[:10]
    )

    return {
        'overview': {
            'total_constituencies': total_constituencies,
            'total_states': total_states,
            'total_elections': total_elections,
            'total_results': total_results,
            'total_datasets': total_datasets,
            'total_demographic_records': total_indicators,
            'total_public_intelligence_articles': total_articles,
            'latest_election_year': latest_year or 2024,
        },
        'turnout_trends': turnout_data,
        'party_seat_share': party_seats,
        'districts_breakdown': districts_summary,
        'recent_datasets': recent_datasets,
    }

def compute_constituency_comparison(constituency_ids):
    constituencies = list(Constituency.objects.filter(id__in=constituency_ids).select_related('state', 'district'))
    comparison = []

    for c in constituencies:
        # Elections
        elections = list(c.elections.order_by('-election_year')[:3])
        el_history = []
        for e in elections:
            w = e.results.filter(position=1).select_related('candidate__party').first()
            r = e.results.filter(position=2).select_related('candidate__party').first()
            margin = (w.votes_received - r.votes_received) if (w and r) else 0
            el_history.append({
                'year': e.election_year,
                'turnout': e.turnout_percentage,
                'winner': w.candidate.name if w else 'N/A',
                'party': w.candidate.party.abbreviation if (w and w.candidate.party) else 'IND',
                'votes': w.votes_received if w else 0,
                'vote_share': w.vote_share if w else 0,
                'runner_up': r.candidate.name if r else 'N/A',
                'margin': margin,
            })

        # Demographics
        demo_indicators = list(
            DemographicIndicator.objects.filter(
                Q(region_identifier=c.constituency_code) | 
                Q(region_identifier=c.district.district_code if c.district else '')
            ).values('name', 'category', 'value', 'unit', 'reference_year')
        )

        comparison.append({
            'id': c.id,
            'name': c.name,
            'code': c.constituency_code,
            'state': c.state.name,
            'district': c.district.name if c.district else 'N/A',
            'type': c.get_constituency_type_display(),
            'is_reserved': c.is_reserved,
            'latitude': c.latitude,
            'longitude': c.longitude,
            'election_history': el_history,
            'demographics': demo_indicators
        })

    return comparison

