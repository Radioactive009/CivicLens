from rest_framework import serializers
from .models import PoliticalParty, Candidate, Election, ElectionResult

class PoliticalPartySerializer(serializers.ModelSerializer):
    class Meta:
        model = PoliticalParty
        fields = ['id', 'name', 'abbreviation', 'party_code', 'color_hex', 'description']

class CandidateSerializer(serializers.ModelSerializer):
    party_name = serializers.CharField(source='party.name', read_only=True)
    party_abbrev = serializers.CharField(source='party.abbreviation', read_only=True)
    party_color = serializers.CharField(source='party.color_hex', read_only=True, default='#6B7280')

    class Meta:
        model = Candidate
        fields = ['id', 'name', 'party', 'party_name', 'party_abbrev', 'party_color', 'candidate_reference', 'created_at']

class ElectionResultSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(source='candidate.name', read_only=True)
    party_name = serializers.CharField(source='candidate.party.name', read_only=True, default='Independent')
    party_abbreviation = serializers.CharField(source='candidate.party.abbreviation', read_only=True, default='IND')
    party_color = serializers.CharField(source='candidate.party.color_hex', read_only=True, default='#6B7280')

    class Meta:
        model = ElectionResult
        fields = [
            'id', 'election', 'candidate', 'candidate_name', 'party_name',
            'party_abbreviation', 'party_color', 'votes_received', 'vote_share',
            'position', 'total_valid_votes', 'created_at'
        ]

class ElectionSerializer(serializers.ModelSerializer):
    constituency_name = serializers.CharField(source='constituency.name', read_only=True)
    district_name = serializers.CharField(source='constituency.district.name', read_only=True, default='')
    state_name = serializers.CharField(source='state.name', read_only=True)
    winner_name = serializers.SerializerMethodField()
    winner_party = serializers.SerializerMethodField()
    winning_margin = serializers.SerializerMethodField()

    class Meta:
        model = Election
        fields = [
            'id', 'election_name', 'election_type', 'election_year', 'state',
            'state_name', 'constituency', 'constituency_name', 'district_name',
            'election_date', 'data_source', 'total_electors', 'total_votes_polled',
            'turnout_percentage', 'winner_name', 'winner_party', 'winning_margin'
        ]

    def get_winner_name(self, obj):
        res = obj.results.filter(position=1).select_related('candidate').first()
        return res.candidate.name if res else 'N/A'

    def get_winner_party(self, obj):
        res = obj.results.filter(position=1).select_related('candidate__party').first()
        if res and res.candidate.party:
            return res.candidate.party.abbreviation
        return 'IND'

    def get_winning_margin(self, obj):
        winner = obj.results.filter(position=1).first()
        runner_up = obj.results.filter(position=2).first()
        if winner and runner_up:
            return winner.votes_received - runner_up.votes_received
        return 0

class ElectionDetailSerializer(ElectionSerializer):
    results = ElectionResultSerializer(many=True, read_only=True)

    class Meta(ElectionSerializer.Meta):
        fields = ElectionSerializer.Meta.fields + ['results']

