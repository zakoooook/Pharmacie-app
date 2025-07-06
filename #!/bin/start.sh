#!/bin/bash

echo "📦 Migration de la base de données..."
python manage.py migrate

echo "👤 Création du superutilisateur (si nécessaire)..."
python manage.py shell < create_superuser.py

echo "🚀 Lancement de Gunicorn..."
gunicorn pharmacie.wsgi --bind 0.0.0.0:$PORT
