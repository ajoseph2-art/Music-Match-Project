from django.contrib import admin
from .models import Community


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ['name', 'genre', 'created_by', 'member_count', 'is_public', 'created_at']
    list_filter = ['is_public', 'genre', 'created_at']
    search_fields = ['name', 'description', 'genre']
    filter_horizontal = ['members']

