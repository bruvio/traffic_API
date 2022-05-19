#!/bin/bash
export SYSTEM_ENV='NOPOSTGRES'
export SECRET_KEY='django-insecure-w=jp7h*^7occppycw4l6a*&ja%#=0_#_qwr=_&krq8e@@m*dkm'
python manage.py wait_for_db
python3 manage.py makemigrations API
python3 manage.py migrate
python manage.py populate_db --num 999 --print true
python3 manage.py runserver 0.0.0.0:8000
