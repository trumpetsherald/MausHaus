#!/bin/sh
# wait-for-postgres.sh
#
# set -e
#
# host="$1"
# shift
# cmd="$@"
#
# until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -U "maus_der_verwalter" -c '\q'; do
#   >&2 echo "Postgres is unavailable - sleeping"
#   sleep 1
# done
#
# >&2 echo "Postgres is up - executing command"
# exec $cmd

echo "Sleeping for 10 seconds while postgres comes up"
sleep 10
cd /var/opt/MausHaus/src
exec python manage.py runserver 0.0.0.0:8000
