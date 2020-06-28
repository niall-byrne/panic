#!/bin/bash

echo "Development Server Starting ..."

pushd "panic" || exit 127

if [[ $1 == "admin" ]]; then
  cloud_sql_proxy --instances=${CLOUDSQLINSTANCE}=tcp:5432 &
else
  ./manage.py wait_for_db
  ./manage.py makemigrations
  ./manage.py migrate
  ./manage.py autoadmin
fi

while true; do
    ./manage.py runserver 0.0.0.0:8080
done
