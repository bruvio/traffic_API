#!/bin/bash
python manage.py wait_for_db
python3 manage.py makemigrations
python3 manage.py migrate
# python manage.py flush
python import_csv.py
python3 manage.py runserver 0.0.0.0:8000
