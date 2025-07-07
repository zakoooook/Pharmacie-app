release: python manage.py migrate
web: gunicorn pharmacie.wsgi
web: python manage.py migrate && gunicorn tonprojet.wsgi
