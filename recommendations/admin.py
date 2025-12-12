from django.contrib import admin
from .models import RecommendationMode, UserRecommendation


@admin.register(RecommendationMode)
class RecommendationModeAdmin(admin.ModelAdmin):
    list_display = ['name', 'min_danceability', 'max_danceability', 'min_energy', 'max_energy']
    search_fields = ['name', 'description']


@admin.register(UserRecommendation)
class UserRecommendationAdmin(admin.ModelAdmin):
    list_display = ['user', 'song', 'mode', 'score', 'user_action', 'created_at']
    list_filter = ['mode', 'user_action', 'created_at']
    search_fields = ['user__username', 'song__name']

