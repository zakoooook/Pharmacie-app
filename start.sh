#!/bin/bash

echo "▶️ Démarrage des migrations..."
python manage.py migrate --noinput

echo "👤 Création du superuser..."
python manage.py shell < create_superuser.py

echo "🚀 Lancement du serveur Gunicorn..."
gunicorn pharmacie.wsgi:application --bind 0.0.0.0:$PORT
