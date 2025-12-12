from django.contrib import admin
from .models import Song, Playlist, PlaylistSong, Review


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['name', 'artist', 'album', 'genre', 'danceability', 'energy']
    list_filter = ['genre', 'created_at']
    search_fields = ['name', 'artist', 'album', 'genre']


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'community', 'is_public', 'is_collaborative', 'song_count', 'created_at']
    list_filter = ['is_public', 'is_collaborative', 'created_at']
    search_fields = ['name', 'description', 'owner__username']
    filter_horizontal = ['collaborators']


@admin.register(PlaylistSong)
class PlaylistSongAdmin(admin.ModelAdmin):
    list_display = ['playlist', 'song', 'added_by', 'order', 'added_at']
    list_filter = ['added_at']
    search_fields = ['playlist__name', 'song__name', 'added_by__username']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'song', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'song__name', 'review_text']

