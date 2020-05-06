#!/bin/sh

set -e

host="$1"
shift
cmd="$@"

>&2 echo "Waiting for postgres to be available"
until PGPASSWORD=$SQL_PASSWORD psql -h "postgresdb" -U "django" -c '\q'; do
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd

# if [ "$DATABASE" = "postgres" ]
# then
#     echo "Waiting for postgres..."

#     while ! nc -z 'postgres' '5432'; do
#       sleep 1
#     done

#     echo "PostgreSQL started"
# # fi

# python manage.py create_db

# exec "$@"