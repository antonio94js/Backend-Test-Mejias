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