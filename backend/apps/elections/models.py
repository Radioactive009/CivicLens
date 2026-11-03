from django.db import models
from apps.constituencies.models import State, Constituency

class PoliticalParty(models.Model):
    name = models.CharField(max_length=150, unique=True)
    abbreviation = models.CharField(max_length=30, unique=True)
    party_code = models.CharField(max_length=30, blank=True, default='')
    color_hex = models.CharField(max_length=10, default='#3B82F6')
    description = models.TextField(blank=True, default='')

    class Meta:
        db_table = 'cl_political_parties'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.abbreviation})"

class Candidate(models.Model):
    name = models.CharField(max_length=150)
    party = models.ForeignKey(PoliticalParty, on_delete=models.SET_NULL, null=True, blank=True, related_name='candidates')
    candidate_reference = models.CharField(max_length=100, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cl_candidates'
        ordering = ['name']

    def __str__(self):
        party_str = self.party.abbreviation if self.party else 'IND'
        return f"{self.name} ({party_str})"

class Election(models.Model):
    class ElectionType(models.TextChoices):
        ASSEMBLY = 'VIDHAN_SABHA', 'State Legislative Assembly (Vidhan Sabha)'
        PARLIAMENTARY = 'LOK_SABHA', 'Parliamentary General Election (Lok Sabha)'

    election_name = models.CharField(max_length=200)
    election_type = models.CharField(max_length=30, choices=ElectionType.choices, default=ElectionType.ASSEMBLY)
    election_year = models.IntegerField(db_index=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='elections')
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE, related_name='elections')
    election_date = models.DateField(null=True, blank=True)
    data_source = models.CharField(max_length=150, default='Election Commission of India (ECI)')
    total_electors = models.PositiveIntegerField(default=0, help_text="Total registered eligible electors")
    total_votes_polled = models.PositiveIntegerField(default=0, help_text="Total votes polled")
    turnout_percentage = models.FloatField(default=0.0)

    class Meta:
        db_table = 'cl_elections'
        unique_together = ('election_year', 'election_type', 'constituency')
        ordering = ['-election_year', 'constituency__name']
        indexes = [
            models.Index(fields=['election_year', 'election_type']),
            models.Index(fields=['state', 'election_year']),
        ]

    def __str__(self):
        return f"{self.election_name} - {self.constituency.name} ({self.election_year})"

class ElectionResult(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='results')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='election_results')
    votes_received = models.PositiveIntegerField(default=0)
    vote_share = models.FloatField(default=0.0, help_text="Percentage of total valid votes")
    position = models.PositiveIntegerField(default=1)
    total_valid_votes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cl_election_results'
        unique_together = ('election', 'candidate')
        ordering = ['election', 'position']
        indexes = [
            models.Index(fields=['election', 'position']),
        ]

    def __str__(self):
        return f"Rank #{self.position}: {self.candidate.name} ({self.votes_received} votes) in {self.election}"

