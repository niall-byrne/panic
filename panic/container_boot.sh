#!/bin/bash

echo "Development Server Starting ..."

pushd "panic" || exit 127

./manage.py wait_for_db
./manage.py makemigrations
./manage.py migrate
./manage.py autoadmin
while true; do
    ./manage.py runserver 0.0.0.0:8080
done
