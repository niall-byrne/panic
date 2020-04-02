# Contributing Guide

## Design

There are some UI sketches available, and a design doc on google drive.
Please reach out to `niall-byrne` and I'll connect you with resources.

## API Spec

https://app.swaggerhub.com/apis/niall-byrne/panic/1.0.0

## Branching

- Please create feature branches for your work.
- Send PR's for a merge to develop.
- Master will contain releases.
- Use [commitizen](https://github.com/commitizen/cz-cli) for all commits. (It's installed in the container.)

## Authentication

## Registration
https://django-allauth.readthedocs.io/en/latest/

## Social Logins
https://github.com/jazzband/dj-rest-auth

## Backend

- Write unittests for management commands, views, serializers, and models
- There should be coverage for these 5 components
- The kitchen app contains examples of how to name your components and test files:
    - `test_[models|serializers|views|management]_[component_name].py`
- Please use the linter as a style guide, and ensure you're in compliance before submitting a PR.
- It's basically PEP, but with a two space indent for readability

## Frontend

The frontend is embedded inside the django project, as the `frontend` app.

To get started, from the top level directory of your cloned repository:
- `cd panic/frontend`
- `npm install` to install all node dependencies.
- `npm run watch` to watch the files, and rebuild as needed.

The frontend source folder is located at 'panic/frontend/src'.

This integration is based off this article: [React Integration with Django](https://www.valentinog.com/blog/drf/)

