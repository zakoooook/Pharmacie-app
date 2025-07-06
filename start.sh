#!/bin/bash

python manage.py migrate
python manage.py collectstatic --noinput

# Supprimer l'ancien superuser admin s'il existe, puis créer un nouveau
echo "from django.contrib.auth import get_user_model; User = get_user_model(); \
User.objects.filter(username='admin').delete(); \
User.objects.create_superuser('admin', 'admin@example.com', 'Admin2025')" | python manage.py shell

gunicorn pharmacie.wsgi:application --bind 0.0.0.0:$PORT
