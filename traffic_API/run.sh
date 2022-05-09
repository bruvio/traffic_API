#!/bin/bash
export ADMIN='admin'
export ADMIN_EMAIL='admin@admin.com'
export ADMIN_PASSWORD='secret'
export SYSTEM_ENV='DEVELOPMENT'
# export SYSTEM_ENV='NOPOSTGRES'
export DB_HOST='localhost'
export DB_NAME='traffic1'
export DB_PASSWORD='bruvio'
export DB_USER='postgres'
export SECRET_KEY='django-insecure-w=jp7h*^7occppycw4l6a*&ja%#=0_#_qwr=_&krq8e@@m*dkm'
# python manage.py wait_for_db
python3 manage.py makemigrations API
python3 manage.py migrate
python3 manage.py createsu
# python manage.py collectstatic --noinput
python manage.py flush
python3 manage.py runserver
