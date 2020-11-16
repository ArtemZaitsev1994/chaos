#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
  echo "Waiting for postgres..."

  while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
  done
fi
  echo "PostgreSQL started"


python manage.py migrate_all
python manage.py initadmin
python manage.py collectstatic --no-input --clear


exec "$@"