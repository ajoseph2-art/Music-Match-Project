from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import RecommendationMode, UserRecommendation
from playlists.models import Song


@login_required
def recommendations_view(request):
    """Get personalized recommendations based on activity mode and filters"""
    user = request.user
    mode_id = request.GET.get('mode')
    min_danceability = request.GET.get('min_danceability')
    max_danceability = request.GET.get('max_danceability')
    min_energy = request.GET.get('min_energy')
    max_energy = request.GET.get('max_energy')
    genre = request.GET.get('genre')
    
    # Get all available modes
    modes = RecommendationMode.objects.all()
    selected_mode = None
    
    # Start with all songs
    songs = Song.objects.all()
    
    # Filter by mode if selected
    if mode_id:
        selected_mode = get_object_or_404(RecommendationMode, id=mode_id)
        if selected_mode.min_danceability is not None:
            songs = songs.filter(danceability__gte=selected_mode.min_danceability)
        if selected_mode.max_danceability is not None:
            songs = songs.filter(danceability__lte=selected_mode.max_danceability)
        if selected_mode.min_energy is not None:
            songs = songs.filter(energy__gte=selected_mode.min_energy)
        if selected_mode.max_energy is not None:
            songs = songs.filter(energy__lte=selected_mode.max_energy)
        if selected_mode.min_valence is not None:
            songs = songs.filter(valence__gte=selected_mode.min_valence)
        if selected_mode.max_valence is not None:
            songs = songs.filter(valence__lte=selected_mode.max_valence)
    
    # Apply manual filters
    if min_danceability:
        try:
            songs = songs.filter(danceability__gte=float(min_danceability))
        except ValueError:
            pass
    
    if max_danceability:
        try:
            songs = songs.filter(danceability__lte=float(max_danceability))
        except ValueError:
            pass
    
    if min_energy:
        try:
            songs = songs.filter(energy__gte=float(min_energy))
        except ValueError:
            pass
    
    if max_energy:
        try:
            songs = songs.filter(energy__lte=float(max_energy))
        except ValueError:
            pass
    
    if genre:
        songs = songs.filter(genre__icontains=genre)
    
    # Exclude songs user has already reviewed or added
    reviewed_songs = user.reviews.values_list('song_id', flat=True)
    songs = songs.exclude(id__in=reviewed_songs)
    
    # Limit results
    songs = songs[:20]
    
    context = {
        'songs': songs,
        'modes': modes,
        'selected_mode': selected_mode,
        'min_danceability': min_danceability or '',
        'max_danceability': max_danceability or '',
        'min_energy': min_energy or '',
        'max_energy': max_energy or '',
        'genre': genre or '',
    }
    return render(request, 'recommendations/recommendations.html', context)


@login_required
def discovery_swipe_view(request):
    """Discovery swipe mode for exploring new music"""
    user = request.user
    
    # Get songs user hasn't reviewed yet
    reviewed_songs = user.reviews.values_list('song_id', flat=True)
    songs = Song.objects.exclude(id__in=reviewed_songs)
    
    # Also exclude songs user has already swiped on
    swiped_songs = UserRecommendation.objects.filter(
        user=user,
        user_action__in=['liked', 'skipped']
    ).values_list('song_id', flat=True)
    songs = songs.exclude(id__in=swiped_songs)
    
    # Get a random song
    import random
    song_count = songs.count()
    if song_count > 0:
        random_index = random.randint(0, song_count - 1)
        song = songs[random_index]
    else:
        song = None
    
    if not song:
        messages.info(request, "No new songs to discover! Check back later or adjust your filters.")
        return redirect('recommendations')
    
    context = {
        'song': song,
    }
    return render(request, 'recommendations/discovery_swipe.html', context)


@login_required
def swipe_action_view(request, song_id, action):
    """Handle swipe actions (like/skip)"""
    song = get_object_or_404(Song, id=song_id)
    action = action.lower()
    
    if action not in ['like', 'skip']:
        messages.error(request, "Invalid action!")
        return redirect('discovery_swipe')
    
    # Record the action
    recommendation, created = UserRecommendation.objects.get_or_create(
        user=request.user,
        song=song,
        defaults={'user_action': 'liked' if action == 'like' else 'skipped'}
    )
    
    if not created:
        recommendation.user_action = 'liked' if action == 'like' else 'skipped'
        recommendation.save()
    
    if action == 'like':
        messages.success(request, f'Added {song.name} to your liked songs!')
    
    # Redirect to next song
    return redirect('discovery_swipe')

