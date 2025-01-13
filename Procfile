web: gunicorn wolfe_emporium.wsgi:application --log-file -
python manage.py collectstatic --noinput
manage.py migrate