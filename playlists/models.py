from django.db import models
from django.contrib.auth.models import User
from communities.models import Community


class Song(models.Model):
    """Song information from Spotify"""
    spotify_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255, blank=True)
    genre = models.CharField(max_length=100, blank=True)
    duration_ms = models.IntegerField(default=0)
    # Spotify audio features
    danceability = models.FloatField(null=True, blank=True)
    energy = models.FloatField(null=True, blank=True)
    valence = models.FloatField(null=True, blank=True)  # Positivity
    tempo = models.FloatField(null=True, blank=True)
    acousticness = models.FloatField(null=True, blank=True)
    instrumentalness = models.FloatField(null=True, blank=True)
    liveness = models.FloatField(null=True, blank=True)
    speechiness = models.FloatField(null=True, blank=True)
    spotify_url = models.URLField(blank=True)
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} by {self.artist}"


class Playlist(models.Model):
    """Playlists created by users or communities"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_playlists')
    community = models.ForeignKey(Community, on_delete=models.SET_NULL, null=True, blank=True, related_name='playlists')
    songs = models.ManyToManyField(Song, through='PlaylistSong', related_name='playlists')
    is_public = models.BooleanField(default=True)
    is_collaborative = models.BooleanField(default=False)
    collaborators = models.ManyToManyField(User, related_name='collaborated_playlists', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def song_count(self):
        return self.songs.count()


class PlaylistSong(models.Model):
    """Through model for Playlist-Song relationship with ordering"""
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    added_at = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'added_at']
        unique_together = ['playlist', 'song']
    
    def __str__(self):
        return f"{self.song.name} in {self.playlist.name}"


class Review(models.Model):
    """Reviews and ratings for songs/albums"""
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=RATING_CHOICES)
    review_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'song']
    
    def __str__(self):
        return f"{self.user.username}'s review of {self.song.name}"

