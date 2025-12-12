#!/usr/bin/env python
"""
Quick setup verification script for MusicMatch project
"""
import os
import sys

def check_django():
    """Check if Django is installed"""
    try:
        import django
        print(f"✓ Django {django.get_version()} is installed")
        return True
    except ImportError:
        print("✗ Django is not installed. Run: pip install -r requirements.txt")
        return False

def check_database():
    """Check database configuration"""
    use_sqlite = os.environ.get('USE_SQLITE', 'False') == 'True'
    if use_sqlite:
        print("✓ Using SQLite for database (local development)")
    else:
        print("✓ Using PostgreSQL for database (production)")
        db_host = os.environ.get('DB_HOST', 'localhost')
        print(f"  Database host: {db_host}")

def check_files():
    """Check if required files exist"""
    required_files = [
        'manage.py',
        'requirements.txt',
        'Dockerfile',
        'docker-compose.yml',
        'nginx.conf',
        'start.sh',
    ]
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} is missing")
            missing.append(file)
    return len(missing) == 0

def main():
    print("MusicMatch Setup Verification\n" + "=" * 40)
    
    django_ok = check_django()
    check_database()
    files_ok = check_files()
    
    print("\n" + "=" * 40)
    if django_ok and files_ok:
        print("✓ Setup looks good!")
        print("\nNext steps:")
        print("1. Set USE_SQLITE=True for local development")
        print("2. Run: python manage.py migrate")
        print("3. Run: python manage.py createsuperuser")
        print("4. Run: python manage.py runserver")
        return 0
    else:
        print("✗ Setup incomplete. Please fix the issues above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())

