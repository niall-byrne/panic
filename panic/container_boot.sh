#!/bin/bash

echo "Development Server Starting ..."

pushd "panic" || exit 127
while true; do
    ./manage.py wait_for_db
    ./manage.py runserver 0.0.0.0:8080
done
