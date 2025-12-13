from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import OperationalError
from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create UserProfile when a User is created"""
    if created:
        try:
            UserProfile.objects.get_or_create(user=instance)
        except OperationalError:
            # Table doesn't exist yet - migrations haven't been run
            # This will be created after migrations run
            pass


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save UserProfile when User is saved"""
    if hasattr(instance, 'profile'):
        instance.profile.save()

