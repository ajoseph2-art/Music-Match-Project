# Spotify API Setup Guide

This guide explains how to set up Spotify API integration for music recommendations.

## Getting Spotify API Credentials

1. **Go to Spotify Developer Dashboard**
   - Visit: https://developer.spotify.com/dashboard
   - Log in with your Spotify account (or create one)

2. **Create an App**
   - Click "Create an App"
   - App name: "MusicMatch" (or any name)
   - App description: "Music discovery and community platform"
   - Check the boxes to agree to terms
   - Click "Create"

3. **Get Your Credentials**
   - You'll see your app dashboard
   - Click "Settings"
   - Copy your **Client ID**
   - Click "View client secret" and copy your **Client Secret**
   - **Keep these secret!** Never commit them to Git

## Setting Up Credentials

### For Local Development

Add these to your environment:

```bash
export SPOTIFY_CLIENT_ID="your_client_id_here"
export SPOTIFY_CLIENT_SECRET="your_client_secret_here"
export USE_SQLITE=True
```

Or create a `.env` file (don't commit this!):

```bash
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
USE_SQLITE=True
```

### For Docker

Add to your `docker-compose.yml` under the `web` service environment:

```yaml
environment:
  SPOTIFY_CLIENT_ID: "your_client_id_here"
  SPOTIFY_CLIENT_SECRET: "your_client_secret_here"
```

### For Production (GCP)

Set environment variables in your deployment:

```bash
export SPOTIFY_CLIENT_ID="your_client_id_here"
export SPOTIFY_CLIENT_SECRET="your_client_secret_here"
```

## Using Spotify Features

Once configured, you can:

1. **Get Spotify Recommendations**
   - Go to `/recommendations/spotify/`
   - Filter by genre, energy, danceability
   - Preview tracks and open in Spotify

2. **Search Spotify**
   - Go to `/recommendations/spotify/search/`
   - Search for any song, artist, or album
   - Preview and open tracks in Spotify

## Features

- **Personalized Recommendations**: Based on user's favorite genre
- **Advanced Filtering**: Filter by energy, danceability, and more
- **Track Previews**: Listen to 30-second previews
- **Direct Spotify Links**: Open tracks in Spotify app/web

## Without Spotify API

If you don't configure Spotify credentials:
- The app will still work with local song database
- Spotify features will redirect to local recommendations
- A warning message will show when trying to access Spotify features

## Troubleshooting

**"Spotify API not configured" message**
- Check that environment variables are set correctly
- Restart the server after setting environment variables

**API errors**
- Verify your credentials are correct
- Check that your Spotify app is active in the dashboard
- Ensure you're not exceeding rate limits (unlikely for development)

## API Limits

Spotify's free tier includes:
- Client Credentials flow (what we use)
- Rate limit: ~180 requests per minute
- More than enough for development and small-scale apps

## Learn More

- [Spotify Web API Documentation](https://developer.spotify.com/documentation/web-api)
- [Get Recommendations Endpoint](https://developer.spotify.com/documentation/web-api/reference/get-recommendations)
- [Search Endpoint](https://developer.spotify.com/documentation/web-api/reference/search)

