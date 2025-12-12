from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .models import Community, ListeningParty, MusicMatch


@login_required
def explore_view(request):
    """Explore page for finding communities"""
    communities = Community.objects.filter(is_public=True)
    
    # Filter by genre if provided
    genre = request.GET.get('genre', '')
    if genre:
        communities = communities.filter(genre__icontains=genre)
    
    # Search query
    search_query = request.GET.get('search', '')
    if search_query:
        communities = communities.filter(
            name__icontains=search_query
        ) | communities.filter(
            description__icontains=search_query
        )
    
    context = {
        'communities': communities,
        'genre': genre,
        'search_query': search_query,
    }
    return render(request, 'communities/explore.html', context)


@login_required
def community_detail_view(request, community_id):
    """Community detail page"""
    community = get_object_or_404(Community, id=community_id)
    is_member = request.user in community.members.all()
    playlists = community.playlists.all()
    listening_parties = community.listening_parties.filter(is_active=True)
    
    context = {
        'community': community,
        'is_member': is_member,
        'playlists': playlists,
        'listening_parties': listening_parties,
    }
    return render(request, 'communities/detail.html', context)


@login_required
def join_community_view(request, community_id):
    """Join a community"""
    community = get_object_or_404(Community, id=community_id)
    if request.user not in community.members.all():
        community.members.add(request.user)
        messages.success(request, f'You joined {community.name}!')
    else:
        messages.info(request, f'You are already a member of {community.name}.')
    return redirect('community_detail', community_id=community_id)


@login_required
def leave_community_view(request, community_id):
    """Leave a community"""
    community = get_object_or_404(Community, id=community_id)
    if request.user in community.members.all():
        community.members.remove(request.user)
        messages.success(request, f'You left {community.name}.')
    else:
        messages.info(request, f'You are not a member of {community.name}.')
    return redirect('explore')


@login_required
def music_matches_view(request):
    """Display music compatibility scores with other users"""
    user = request.user
    
    # Get all matches where user is user1 or user2
    matches_as_user1 = MusicMatch.objects.filter(user1=user)
    matches_as_user2 = MusicMatch.objects.filter(user2=user)
    
    # Combine and get the other user and score
    matches = []
    for match in matches_as_user1:
        matches.append({
            'other_user': match.user2,
            'score': match.compatibility_score,
            'calculated_at': match.calculated_at
        })
    for match in matches_as_user2:
        matches.append({
            'other_user': match.user1,
            'score': match.compatibility_score,
            'calculated_at': match.calculated_at
        })
    
    # Sort by score descending
    matches.sort(key=lambda x: x['score'], reverse=True)
    
    context = {
        'matches': matches,
    }
    return render(request, 'communities/music_matches.html', context)


@login_required
def calculate_match_view(request, user_id):
    """Calculate music compatibility score with another user"""
    other_user = get_object_or_404(User, id=user_id)
    
    if other_user == request.user:
        messages.error(request, "You cannot calculate a match with yourself!")
        return redirect('music_matches')
    
    # Simple compatibility calculation based on shared playlists and reviews
    from playlists.models import Playlist, Review
    
    # Get shared songs in playlists
    user1_playlists = Playlist.objects.filter(owner=request.user)
    user2_playlists = Playlist.objects.filter(owner=other_user)
    
    user1_songs = set()
    user2_songs = set()
    
    for playlist in user1_playlists:
        user1_songs.update(playlist.songs.all())
    for playlist in user2_playlists:
        user2_songs.update(playlist.songs.all())
    
    # Calculate similarity based on shared songs
    if user1_songs or user2_songs:
        shared_songs = user1_songs & user2_songs
        total_songs = user1_songs | user2_songs
        if total_songs:
            compatibility_score = len(shared_songs) / len(total_songs)
        else:
            compatibility_score = 0.0
    else:
        compatibility_score = 0.0
    
    # Get or create match
    match, created = MusicMatch.objects.get_or_create(
        user1=request.user if request.user.id < other_user.id else other_user,
        user2=other_user if request.user.id < other_user.id else request.user,
        defaults={'compatibility_score': compatibility_score}
    )
    
    if not created:
        match.compatibility_score = compatibility_score
        match.save()
    
    messages.success(request, f'Compatibility with {other_user.username}: {compatibility_score:.1%}')
    return redirect('music_matches')
