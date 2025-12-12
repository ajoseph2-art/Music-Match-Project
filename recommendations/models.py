from django.db import models
from django.contrib.auth.models import User
from playlists.models import Song


class RecommendationMode(models.Model):
    """Activity-based recommendation modes"""
    MODE_CHOICES = [
        ('focus', 'Focus Mode'),
        ('workout', 'Working Out'),
        ('driving', 'Driving'),
        ('dancing', 'Dancing'),
        ('singing', 'Sing Along'),
        ('relaxing', 'Relaxing'),
        ('party', 'Party'),
    ]
    
    name = models.CharField(max_length=50, choices=MODE_CHOICES, unique=True)
    description = models.TextField()
    
    # Preferred audio features for this mode
    min_danceability = models.FloatField(null=True, blank=True)
    max_danceability = models.FloatField(null=True, blank=True)
    min_energy = models.FloatField(null=True, blank=True)
    max_energy = models.FloatField(null=True, blank=True)
    min_valence = models.FloatField(null=True, blank=True)
    max_valence = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return self.get_name_display()


class UserRecommendation(models.Model):
    """Stored recommendations for users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    mode = models.ForeignKey(RecommendationMode, on_delete=models.SET_NULL, null=True, blank=True)
    reason = models.TextField(blank=True)
    score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    shown_at = models.DateTimeField(null=True, blank=True)
    user_action = models.CharField(max_length=20, blank=True)  # 'liked', 'skipped', 'added'
    
    class Meta:
        ordering = ['-score', '-created_at']
    
    def __str__(self):
        return f"Recommendation for {self.user.username}: {self.song.name}"

