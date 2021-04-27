#!/bin/sh

# python manage.py flush --no-input
python manage.py collectstatic --settings=config.settings.deploy --no-input
python manage.py migrate --settings=config.settings.deploy
gunicorn config.wsgi.deploy -b 0.0.0.0:8000

exec "$@"