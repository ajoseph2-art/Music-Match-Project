from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Community, ListeningParty, MusicMatch, CommunityMessage


@login_required
def create_community_view(request):
    """Create a new community"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        genre = request.POST.get('genre', '')
        is_public = request.POST.get('is_public') == 'on'
        
        if name and description:
            community = Community.objects.create(
                name=name,
                description=description,
                genre=genre,
                created_by=request.user,
                is_public=is_public
            )
            community.members.add(request.user)
            messages.success(request, f'Community "{name}" created successfully!')
            return redirect('community_detail', community_id=community.id)
        else:
            messages.error(request, 'Please provide both name and description.')
    
    return render(request, 'communities/create.html')


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
    """Community detail page with chat"""
    community = get_object_or_404(Community, id=community_id)
    is_member = request.user in community.members.all()
    
    # Only members can see the community details
    if not is_member and not community.is_public:
        messages.error(request, "You must be a member to view this community.")
        return redirect('explore')
    
    # Get community data
    playlists = community.playlists.all()
    listening_parties = community.listening_parties.filter(is_active=True)
    
    # Get recent chat messages (last 50)
    messages_list = community.messages.select_related('user').all()[:50]
    
    context = {
        'community': community,
        'is_member': is_member,
        'playlists': playlists,
        'listening_parties': listening_parties,
        'messages_list': messages_list,
    }
    return render(request, 'communities/detail.html', context)


@login_required
def send_message_view(request, community_id):
    """Send a message in community chat"""
    if request.method == 'POST':
        community = get_object_or_404(Community, id=community_id)
        
        # Check if user is a member
        if request.user not in community.members.all():
            messages.error(request, "You must be a member to send messages.")
            return redirect('community_detail', community_id=community_id)
        
        message_text = request.POST.get('message', '').strip()
        if message_text:
            CommunityMessage.objects.create(
                community=community,
                user=request.user,
                message=message_text
            )
        
        return redirect('community_detail', community_id=community_id)
    
    return redirect('explore')


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
def delete_community_view(request, community_id):
    """Delete a community (only the creator can delete)"""
    community = get_object_or_404(Community, id=community_id)
    
    # Only the creator can delete the community
    if community.created_by != request.user:
        messages.error(request, "Only the community creator can delete it.")
        return redirect('community_detail', community_id=community_id)
    
    if request.method == 'POST':
        name = community.name
        community.delete()
        messages.success(request, f'Community "{name}" has been deleted.')
        return redirect('explore')
    
    return render(request, 'communities/delete.html', {'community': community})


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
