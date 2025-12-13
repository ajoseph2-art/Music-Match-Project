# MusicMatch - Social Music Discovery Platform

A full-stack web application for social music discovery, community building, and personalized music recommendations powered by the Spotify API.

## Features

### 🎵 Spotify Integration
- **Search Songs**: Search for any song or artist on Spotify
- **Similar Songs**: Discover songs similar to your favorites
- **Genre Recommendations**: Browse music by genre (Pop, Rock, Hip-Hop, etc.)
- **Audio Previews**: Listen to 30-second previews directly in the app

### 🎧 Playlist Management
- **Create Playlists**: Build your own custom playlists
- **Add Songs**: Add songs from Spotify search results to any playlist
- **Remove Songs**: Remove songs from playlists you own
- **Share to Communities**: Share your playlists with communities
- **View Details**: See who added each song and when

### 👥 Community Features
- **Create Communities**: Build communities around genres or shared interests
- **Real-Time Chat**: Discord-style messaging within communities
- **Community Playlists**: View and contribute to shared playlists
- **Join/Leave**: Easily manage your community memberships
- **Delete Communities**: Creators can remove their communities

### 👤 User Features
- **User Profiles**: View your profile and activity
- **Authentication**: Secure login/logout system
- **Personalized Experience**: See your playlists and communities

## Technology Stack

- **Backend**: Django 5.0.7, Python 3.11+
- **Frontend**: Bootstrap 5.3, HTML5, CSS3, JavaScript
- **Database**: PostgreSQL (production), SQLite (development)
- **API**: Spotify Web API for music data
- **Deployment**: Docker, nginx, gunicorn, Google Cloud Platform
- **Other**: Requests library for API calls, WhiteNoise for static files

## Quick Start

### Local Development

1. **Clone the repository:**
```bash
git clone https://github.com/ajoseph2-art/Music-Match-Project.git
cd Music-Match-Project
```

2. **Run the quick setup script:**
```bash
./quick_local_server.sh
```

3. **Or set up manually:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export USE_SQLITE=True
export SPOTIFY_CLIENT_ID="your_client_id"
export SPOTIFY_CLIENT_SECRET="your_client_secret"
python3 manage.py migrate
python3 manage.py runserver
```

4. **Access the app:**
Visit http://127.0.0.1:8000

## Spotify API Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Get your Client ID and Client Secret
4. Set environment variables:
```bash
export SPOTIFY_CLIENT_ID="your_client_id"
export SPOTIFY_CLIENT_SECRET="your_client_secret"
```

See `SPOTIFY_SETUP.md` for detailed instructions.

## Deployment

### Google Cloud Platform

1. **Build and push Docker image:**
```bash
./CLOUD_BUILD.sh
```

2. **Create a VM instance** in GCP Console:
   - Region: `us-west1`
   - Machine type: `e2-small`
   - Boot disk: Container-Optimized OS
   - Firewall: Allow HTTP traffic
   - Use `vm_startup_script.sh` as startup script

3. **Access your app** at the VM's external IP

### Docker (Local)

```bash
docker-compose up --build
```

Visit http://localhost:8000

## Project Structure

```
Music-Match-Project/
├── accounts/          # User authentication and profiles
├── communities/       # Community groups and chat
├── playlists/         # Playlist and song management
├── recommendations/   # Spotify integration and recommendations
├── templates/         # HTML templates
├── musicmatch/        # Django project settings
├── staticfiles/       # Static files (CSS, JS, images)
├── Dockerfile         # Docker image definition
├── docker-compose.yml # Docker compose configuration
├── requirements.txt   # Python dependencies
└── manage.py          # Django management script
```

## API Endpoints

### Public
- `/` - Landing page
- `/accounts/login/` - User login
- `/accounts/join/` - User registration

### Authenticated
- `/home/` - User dashboard
- `/communities/explore/` - Browse communities
- `/playlists/` - View your playlists
- `/recommendations/` - Get music recommendations
- `/recommendations/spotify/search/` - Search Spotify
- `/profile/` - View your profile

## Environment Variables

Required:
- `SPOTIFY_CLIENT_ID` - Spotify API client ID
- `SPOTIFY_CLIENT_SECRET` - Spotify API client secret

Optional:
- `USE_SQLITE=True` - Use SQLite instead of PostgreSQL
- `DEBUG=False` - Disable debug mode in production
- `SECRET_KEY` - Django secret key
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts

## Database Models

- **User**: Built-in Django user model
- **UserProfile**: Extended user information
- **Community**: Music communities with chat
- **CommunityMessage**: Chat messages within communities
- **Playlist**: User-created playlists
- **Song**: Song information from Spotify
- **PlaylistSong**: Many-to-many relationship with ordering
- **Review**: User reviews and ratings

## Contributing

This is a course project. For issues or suggestions, please contact the authors.

## Authors

- **Joey Lu**
- **Aaron Joseph**

## License

This project was created for educational purposes as part of a server-side web development course.

## Acknowledgments

- Spotify Web API for music data
- Bootstrap for UI components
- Django community for the excellent framework
- Google Cloud Platform for hosting

---

**Live Demo**: http://34.53.53.240  
**Repository**: https://github.com/ajoseph2-art/Music-Match-Project
