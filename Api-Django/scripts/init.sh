#!/bin/bash
# Initialization script for deployment

echo "Running Django migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Deployment initialization completed!"
