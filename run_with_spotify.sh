#!/bin/bash
# Quick server startup with Spotify API enabled

cd "/Users/aaronjoseph/serverside final project"
source venv/bin/activate

# Set environment variables
export USE_SQLITE=True
export SPOTIFY_CLIENT_ID="f3d8eeede32842ee8139616214cedd3f"
export SPOTIFY_CLIENT_SECRET="c5764d0ce4cc44d089787f604d7fa60c"

echo "Starting MusicMatch with Spotify API enabled..."
echo "Spotify features will be available at:"
echo "  - Recommendations: http://127.0.0.1:8000/recommendations/spotify/"
echo "  - Search: http://127.0.0.1:8000/recommendations/spotify/search/"
echo ""

python3 manage.py runserver

