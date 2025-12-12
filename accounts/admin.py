from django.contrib import admin
from .models import UserProfile, Badge, UserBadge


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'favorite_genre', 'favorite_artist', 'created_at']
    list_filter = ['created_at', 'favorite_genre']
    search_fields = ['user__username', 'favorite_genre', 'favorite_artist']


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'hours_required', 'icon']
    search_fields = ['name', 'description']


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'earned_at']
    list_filter = ['badge', 'earned_at']
    search_fields = ['user__username', 'badge__name']

