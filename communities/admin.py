from django.contrib import admin
from .models import Community, ListeningParty, MusicMatch


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ['name', 'genre', 'created_by', 'member_count', 'is_public', 'created_at']
    list_filter = ['is_public', 'genre', 'created_at']
    search_fields = ['name', 'description', 'genre']
    filter_horizontal = ['members']


@admin.register(ListeningParty)
class ListeningPartyAdmin(admin.ModelAdmin):
    list_display = ['name', 'community', 'host', 'start_time', 'is_active']
    list_filter = ['is_active', 'start_time', 'created_at']
    search_fields = ['name', 'community__name', 'host__username']
    filter_horizontal = ['participants']


@admin.register(MusicMatch)
class MusicMatchAdmin(admin.ModelAdmin):
    list_display = ['user1', 'user2', 'compatibility_score', 'calculated_at']
    list_filter = ['calculated_at']
    search_fields = ['user1__username', 'user2__username']

