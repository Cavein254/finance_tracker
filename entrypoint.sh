#!/bin/sh

echo "Starting entrypoint script..."

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate
