from django.contrib import admin
from .models import State, District, Constituency

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'state_code', 'capital', 'created_at')
    search_fields = ('name', 'state_code')

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'district_code', 'headquarters')
    list_filter = ('state',)
    search_fields = ('name', 'district_code')

@admin.register(Constituency)
class ConstituencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'constituency_code', 'state', 'district', 'constituency_type', 'is_reserved')
    list_filter = ('state', 'constituency_type', 'is_reserved')
    search_fields = ('name', 'constituency_code')

