# MusicMatch - Social Music Discovery Platform

A full-stack web application for social music discovery, community building, and personalized music recommendations.

## Features

- **Community Groups**: Connect with music lovers who share your taste
- **Listening Parties**: Join live listening rooms with community members
- **Collaborative Playlists**: Create and contribute to community playlists
- **Reviews & Ratings**: Share your thoughts on songs and albums
- **Music Matching**: See compatibility scores with other users
- **Smart Recommendations**: Get personalized recommendations based on activity mode and song attributes

## Technology Stack

- **Backend**: Django 5.0.7, Python 3.11+
- **Frontend**: Bootstrap 5.3, HTML5, CSS3, JavaScript
- **Database**: PostgreSQL (production), SQLite (development)
- **Deployment**: Docker, nginx, gunicorn, Google Cloud Platform
- **Other**: Requests library for external API calls

## Project Structure

```
musicmatch/
├── accounts/          # User authentication and profiles
├── communities/       # Community groups and listening parties
├── playlists/         # Playlists, songs, and reviews
├── recommendations/   # Recommendation engine and modes
├── musicmatch/        # Django project settings
├── templates/         # HTML templates
├── staticfiles/       # Collected static files
└── media/            # User-uploaded media
```

## Models

The application includes the following models (beyond Django's built-in User model):

1. **UserProfile** (accounts) - Extended user profile with music preferences
2. **Badge** (accounts) - Badges earned by users
3. **Community** (communities) - Music communities
4. **ListeningParty** (communities) - Live listening rooms
5. **MusicMatch** (communities) - Compatibility scores between users
6. **Song** (playlists) - Song information from Spotify
7. **Playlist** (playlists) - User and community playlists
8. **Review** (playlists) - Reviews and ratings for songs
9. **RecommendationMode** (recommendations) - Activity-based recommendation modes
10. **UserRecommendation** (recommendations) - Stored recommendations

## Setup Instructions

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "serverside final project"
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   export USE_SQLITE=True  # Use SQLite for local development
   export DEBUG=True
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

### Docker Development

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Run migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

3. **Create superuser**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

## Deployment to Google Cloud Platform

### Prerequisites

- Google Cloud Platform account
- Domain name registered
- Docker installed locally

### Deployment Steps

1. **Build Docker image**
   ```bash
   docker build -t gcr.io/[PROJECT-ID]/musicmatch:latest .
   ```

2. **Push to Google Container Registry**
   ```bash
   docker push gcr.io/[PROJECT-ID]/musicmatch:latest
   ```

3. **Set up PostgreSQL database in GCP**
   - Create Cloud SQL PostgreSQL instance
   - Note connection details

4. **Deploy to Compute Engine**
   - Create managed instance group with at least 2 instances
   - Configure load balancer
   - Set up SSL/HTTPS with your domain
   - Configure environment variables for database connection

5. **Configure environment variables**
   - `DB_NAME`: PostgreSQL database name
   - `DB_USER`: PostgreSQL user
   - `DB_PASSWORD`: PostgreSQL password
   - `DB_HOST`: Cloud SQL instance IP
   - `DB_PORT`: 5432
   - `SECRET_KEY`: Django secret key
   - `DEBUG`: False (for production)
   - `USE_SQLITE`: False

## Endpoints

- `/` - Home page
- `/accounts/join/` - User registration
- `/accounts/login/` - User login
- `/accounts/logout/` - User logout
- `/accounts/about/` - About page
- `/explore/` - Explore communities
- `/profile/` - User profile
- `/server_info/` - Server and Django configuration info
- `/admin/` - Django admin interface

## Requirements

See `requirements.txt` for complete list of dependencies.

Key dependencies:
- Django==5.0.7
- requests==2.22.0
- psycopg2-binary==2.9.9
- gunicorn==21.2.0
- whitenoise==6.6.0

## Authors

- Joey Lu
- Aaron Joseph

## License

This project is for educational purposes (CSCI 565 - Server-Side Web Development).

