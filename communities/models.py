from django.db import models
from django.contrib.auth.models import User


class Community(models.Model):
    """Music communities based on genre or shared interests"""
    name = models.CharField(max_length=255)
    description = models.TextField()
    genre = models.CharField(max_length=100, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_communities')
    members = models.ManyToManyField(User, related_name='communities', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    def member_count(self):
        return self.members.count()


class ListeningParty(models.Model):
    """Live listening rooms within communities"""
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='listening_parties')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_parties')
    participants = models.ManyToManyField(User, related_name='joined_parties', blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.community.name}"


class MusicMatch(models.Model):
    """Music compatibility score between users"""
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_user2')
    compatibility_score = models.FloatField(default=0.0)  # 0.0 to 1.0
    calculated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user1', 'user2']
    
    def __str__(self):
        return f"{self.user1.username} & {self.user2.username}: {self.compatibility_score:.2%}"


class CommunityMessage(models.Model):
    """Chat messages within a community"""
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='community_messages')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.user.username} in {self.community.name}: {self.message[:50]}"

