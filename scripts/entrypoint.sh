#!/bin/sh

set -e
python manage.py wait_for_db
python manage.py makemigrations API
python manage.py migrate --run-syncdb
# python import_csv.py
uwsgi --socket :9000 --workers 4 --master --enable-threads --module traffic_API.wsgi
