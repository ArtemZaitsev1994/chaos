#!/bin/sh


python3 manage.py makemigrations
python3 manage.py makemigrations authentication
python3 manage.py migrate
python3 manage.py migrate --database=auth_db
