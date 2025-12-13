from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import requests
import base64


def get_spotify_token():
    """Get Spotify API access token"""
    client_id = getattr(settings, 'SPOTIFY_CLIENT_ID', None)
    client_secret = getattr(settings, 'SPOTIFY_CLIENT_SECRET', None)
    
    if not client_id or not client_secret:
        return None
    
    # Encode credentials
    credentials = f"{client_id}:{client_secret}"
    credentials_b64 = base64.b64encode(credentials.encode()).decode()
    
    # Get token
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {credentials_b64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    
    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        if response.status_code == 200:
            return response.json().get('access_token')
    except:
        pass
    
    return None


@login_required
def spotify_recommendations_view(request):
    """Get music recommendations from Spotify API using search"""
    token = get_spotify_token()
    
    if not token:
        messages.warning(request, "Spotify API not configured. Please set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET environment variables.")
        return render(request, 'recommendations/recommendations.html', {'spotify_tracks': [], 'genre': 'pop'})
    
    # Popular genres to search for
    valid_genres = [
        'pop', 'rock', 'hip-hop', 'electronic', 'jazz', 'classical', 
        'country', 'r&b', 'indie', 'metal', 'punk', 'blues', 'reggae',
        'folk', 'soul', 'funk', 'disco', 'house', 'techno', 'trance',
        'edm', 'ambient', 'latin', 'reggaeton', 'k-pop', 'afrobeat'
    ]
    
    # Get parameters
    genre = request.GET.get('genre', 'pop').lower().strip()
    
    # Validate genre
    if not genre or genre not in valid_genres:
        genre = 'pop'
    
    # Use Search API to find songs by genre
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    
    # Build search query with genre
    search_query = f"genre:{genre}"
    
    # Add year filter for newer music
    year = request.GET.get('year', '')
    if year:
        search_query += f" year:{year}"
    
    params = {
        "q": search_query,
        "type": "track",
        "limit": 20,
        "market": "US"
    }
    
    from playlists.models import Playlist
    user_playlists = Playlist.objects.filter(owner=request.user).order_by('-updated_at')
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            spotify_tracks = data.get('tracks', {}).get('items', [])
            
            context = {
                'spotify_tracks': spotify_tracks,
                'genre': genre,
                'valid_genres': valid_genres,
                'user_playlists': user_playlists,
            }
            return render(request, 'recommendations/recommendations.html', context)
        else:
            messages.error(request, f"Spotify API error: {response.status_code}")
    except Exception as e:
        messages.error(request, f"Error connecting to Spotify: {str(e)}")
    
    # Return empty page on error instead of redirect loop
    return render(request, 'recommendations/recommendations.html', {
        'spotify_tracks': [],
        'genre': genre,
        'user_playlists': user_playlists
    })


@login_required
def search_spotify_view(request):
    """Search for songs on Spotify"""
    from playlists.models import Playlist
    
    query = request.GET.get('q', '')
    token = get_spotify_token()
    user_playlists = Playlist.objects.filter(owner=request.user).order_by('-updated_at')
    
    if not token:
        messages.warning(request, "Spotify API not configured.")
        return render(request, 'recommendations/spotify_search.html', {
            'results': [],
            'error': 'Spotify not configured',
            'user_playlists': user_playlists
        })
    
    if not query:
        return render(request, 'recommendations/spotify_search.html', {
            'results': [],
            'user_playlists': user_playlists
        })
    
    # Search Spotify
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "q": query,
        "type": "track",
        "limit": 20,
        "market": "US"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            tracks = data.get('tracks', {}).get('items', [])
            
            context = {
                'results': tracks,
                'query': query,
                'user_playlists': user_playlists,
            }
            return render(request, 'recommendations/spotify_search.html', context)
    except Exception as e:
        messages.error(request, f"Error searching Spotify: {str(e)}")
    
    return render(request, 'recommendations/spotify_search.html', {
        'results': [],
        'user_playlists': user_playlists
    })


@login_required
def spotify_similar_view(request):
    """Find songs similar to a given track using Spotify's search with artist"""
    track_id = request.GET.get('track_id', '')
    track_name = request.GET.get('track_name', '')
    
    token = get_spotify_token()
    
    if not token:
        messages.warning(request, "Spotify API not configured.")
        return redirect('spotify_search')
    
    if not track_id:
        messages.error(request, "No track specified.")
        return redirect('spotify_search')
    
    similar_tracks = []
    original_track = None
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        # First, get the original track info
        track_url = f"https://api.spotify.com/v1/tracks/{track_id}"
        track_response = requests.get(track_url, headers=headers, timeout=10)
        
        if track_response.status_code == 200:
            original_track = track_response.json()
            artist_name = original_track['artists'][0]['name'] if original_track.get('artists') else ''
            
            # Search for more songs by the same artist
            search_url = "https://api.spotify.com/v1/search"
            search_params = {
                "q": f"artist:{artist_name}",
                "type": "track",
                "limit": 20,
                "market": "US"
            }
            
            search_response = requests.get(search_url, headers=headers, params=search_params, timeout=10)
            
            if search_response.status_code == 200:
                search_data = search_response.json()
                all_tracks = search_data.get('tracks', {}).get('items', [])
                # Filter out the original track
                similar_tracks = [t for t in all_tracks if t['id'] != track_id]
        
        from playlists.models import Playlist
        user_playlists = Playlist.objects.filter(owner=request.user).order_by('-updated_at')
        
        context = {
            'original_track': original_track,
            'similar_tracks': similar_tracks,
            'track_name': track_name or (original_track['name'] if original_track else 'Unknown'),
            'user_playlists': user_playlists,
        }
        return render(request, 'recommendations/spotify_similar.html', context)
        
    except Exception as e:
        messages.error(request, f"Error finding similar songs: {str(e)}")
    
    return redirect('spotify_search')

