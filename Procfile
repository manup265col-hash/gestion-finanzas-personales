release: cd web && python manage.py migrate && python manage.py collectstatic --noinput
web: cd web && gunicorn web.wsgi --log-file -

