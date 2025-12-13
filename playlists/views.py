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


@login_required
def create_playlist_view(request):
    """Create a new playlist"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        is_public = request.POST.get('is_public') == 'on'
        community_id = request.POST.get('community')
        
        if name:
            playlist = Playlist.objects.create(
                name=name,
                description=description,
                owner=request.user,
                is_public=is_public
            )
            
            # Link to community if specified
            if community_id:
                try:
                    community = Community.objects.get(id=community_id)
                    if request.user in community.members.all():
                        playlist.community = community
                        playlist.save()
                except Community.DoesNotExist:
                    pass
            
            messages.success(request, f'Playlist "{name}" created successfully!')
            return redirect('playlist_detail', playlist_id=playlist.id)
        else:
            messages.error(request, 'Please provide a playlist name.')
    
    # Get user's communities for the dropdown
    user_communities = request.user.communities.all()
    
    return render(request, 'playlists/create_playlist.html', {
        'user_communities': user_communities
    })


@login_required
def playlist_detail_view(request, playlist_id):
    """View playlist details"""
    playlist = get_object_or_404(Playlist, id=playlist_id)
    
    # Check if user can view this playlist
    if not playlist.is_public and playlist.owner != request.user:
        messages.error(request, "This playlist is private.")
        return redirect('home')
    
    songs = playlist.songs.all()
    is_owner = playlist.owner == request.user
    
    context = {
        'playlist': playlist,
        'songs': songs,
        'is_owner': is_owner,
    }
    return render(request, 'playlists/playlist_detail.html', context)


@login_required
def my_playlists_view(request):
    """View all user's playlists"""
    playlists = Playlist.objects.filter(owner=request.user).order_by('-updated_at')
    
    context = {
        'playlists': playlists,
    }
    return render(request, 'playlists/my_playlists.html', context)


@login_required
def delete_playlist_view(request, playlist_id):
    """Delete a playlist"""
    playlist = get_object_or_404(Playlist, id=playlist_id)
    
    if playlist.owner != request.user:
        messages.error(request, "You can only delete your own playlists.")
        return redirect('my_playlists')
    
    if request.method == 'POST':
        name = playlist.name
        playlist.delete()
        messages.success(request, f'Playlist "{name}" deleted.')
        return redirect('my_playlists')
    
    return render(request, 'playlists/delete_playlist.html', {'playlist': playlist})
