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

## Backend

- Write unittests for management commands, views, serializers, and models
- There should be coverage for these 5 components
- The kitchen app contains examples of how to name your components and test files:
    - `test_[models|serializers|views|management]_[component_name].py`
- Please use the linter as a style guide, and ensure you're in compliance before submitting a PR.
- It's basically PEP, but with a two space indent for readability

## Frontend

We're going to build a django app, that will contain the React piece.
Integration is similar to what's shown here:
[React Integration with Django](https://www.valentinog.com/blog/drf/)

(The frontend isn't setup yet, so there is room here to influence the design and arrangement.)
