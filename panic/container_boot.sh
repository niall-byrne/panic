#!/bin/bash

echo "Development Server Starting ..."

pushd "panic" || exit 127
while true; do
    ./manage.py runserver 0.0.0.0:8080
done
