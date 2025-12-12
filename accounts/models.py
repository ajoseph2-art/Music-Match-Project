from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Extended user profile with music preferences and Spotify integration"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    spotify_id = models.CharField(max_length=255, blank=True, null=True)
    favorite_genre = models.CharField(max_length=100, blank=True)
    favorite_artist = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


class Badge(models.Model):
    """Badges earned by users based on listening hours"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='🏆')  # Emoji or icon name
    hours_required = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name


class UserBadge(models.Model):
    """Association between users and badges they've earned"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'badge']
    
    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"

