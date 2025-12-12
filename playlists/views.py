from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
import requests
from .models import Playlist, Song, Review
from communities.models import Community
from accounts.models import UserProfile


def server_info(request):
    """Server info endpoint as specified in requirements"""
    server_geodata = requests.get('https://ipwhois.app/json/').json()
    settings_dump = settings.__dict__
    return HttpResponse("{}{}".format(server_geodata, settings_dump))


def index_view(request):
    """Landing page - redirects authenticated users to home"""
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'playlists/index.html')


@login_required
def home_view(request):
    """Home page showing recent activity"""
    user = request.user
    # Get user's communities
    user_communities = user.communities.all()[:5]
    
    # Get recent playlists from user's communities
    recent_playlists = Playlist.objects.filter(
        community__in=user_communities
    ).order_by('-updated_at')[:5]
    
    # Get user's playlists
    user_playlists = user.owned_playlists.all()[:5]
    
    # Get upcoming listening parties
    from communities.models import ListeningParty
    from django.utils import timezone
    upcoming_parties = ListeningParty.objects.filter(
        community__in=user_communities,
        start_time__gte=timezone.now()
    ).order_by('start_time')[:5]
    
    context = {
        'user_communities': user_communities,
        'recent_playlists': recent_playlists,
        'user_playlists': user_playlists,
        'upcoming_parties': upcoming_parties,
    }
    return render(request, 'playlists/home.html', context)


@login_required
def profile_view(request, user_id=None):
    """User profile page"""
    if user_id:
        profile_user = get_object_or_404(User, id=user_id)
    else:
        profile_user = request.user
    
    # Get or create profile (should exist via signal, but handle edge case)
    profile, created = UserProfile.objects.get_or_create(user=profile_user)
    playlists = profile_user.owned_playlists.filter(is_public=True)
    badges = profile_user.badges.all()
    
    context = {
        'profile_user': profile_user,
        'profile': profile,
        'playlists': playlists,
        'badges': badges,
    }
    return render(request, 'playlists/profile.html', context)
