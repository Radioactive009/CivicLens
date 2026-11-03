from django.contrib import admin
from .models import PoliticalParty, Candidate, Election, ElectionResult

@admin.register(PoliticalParty)
class PoliticalPartyAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation', 'party_code', 'color_hex')
    search_fields = ('name', 'abbreviation')

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'party', 'created_at')
    list_filter = ('party',)
    search_fields = ('name',)

class ElectionResultInline(admin.TabularInline):
    model = ElectionResult
    extra = 0

@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ('election_name', 'constituency', 'election_year', 'election_type', 'turnout_percentage')
    list_filter = ('election_year', 'election_type', 'state')
    search_fields = ('election_name', 'constituency__name')
    inlines = [ElectionResultInline]

