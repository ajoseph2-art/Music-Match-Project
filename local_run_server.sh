#!/bin/bash
# Local development server script
# Collects static files and runs Django development server

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Django development server..."
python manage.py runserver

