release: python web/manage.py migrate && python web/manage.py collectstatic --noinput
web: gunicorn web.web.wsgi --log-file -
