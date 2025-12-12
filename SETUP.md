# Quick Setup Guide

## Local Development Setup

### Option 1: Using SQLite (Easiest for local testing)

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variable for SQLite**
   ```bash
   export USE_SQLITE=True
   export DEBUG=True
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - Open http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

### Option 2: Using Docker Compose

1. **Start services**
   ```bash
   docker-compose up --build
   ```

2. **Run migrations** (in another terminal)
   ```bash
   docker-compose exec web python manage.py migrate
   ```

3. **Create superuser**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

4. **Access the application**
   - Open http://localhost:8000/

## Key URLs

- `/` - Landing page (redirects authenticated users to /home/)
- `/home/` - User dashboard (requires login)
- `/accounts/join/` - User registration
- `/accounts/login/` - User login
- `/accounts/logout/` - User logout
- `/accounts/about/` - About page
- `/explore/` - Explore communities (requires login)
- `/profile/` - User profile (requires login)
- `/server_info/` - Server configuration info
- `/admin/` - Django admin interface

## Testing the Application

1. **Create a test user**
   - Go to `/accounts/join/`
   - Register a new account

2. **Create test data** (via admin or shell)
   ```bash
   python manage.py shell
   ```
   ```python
   from django.contrib.auth.models import User
   from communities.models import Community
   from accounts.models import UserProfile
   
   # Create a community
   user = User.objects.first()
   community = Community.objects.create(
       name="Rock Music Lovers",
       description="A community for rock music enthusiasts",
       genre="Rock",
       created_by=user,
       is_public=True
   )
   community.members.add(user)
   ```

## Notes

- The application uses PostgreSQL in production (GCP) but can use SQLite locally
- Static files are collected automatically in production
- Media files are stored in the `media/` directory
- All models are registered in Django admin for easy management

