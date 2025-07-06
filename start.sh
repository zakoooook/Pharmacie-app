#!/bin/bash

python manage.py migrate
python manage.py collectstatic --noinput

# Création automatique du superuser si inexistant
echo "from django.contrib.auth import get_user_model; User = get_user_model(); \
if not User.objects.filter(username='admin').exists(): \
    User.objects.create_superuser('Admin', 'admin@example.com', 'Admin2025')" | python manage.py shell

gunicorn pharmacie.wsgi:application --bind 0.0.0.0:$PORT
