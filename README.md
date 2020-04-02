# Project Documentation

## Don't Panic!

A pandemic grocery management app.

[![panic-automation](https://github.com/niall-byrne/panic/workflows/panic%20Automation/badge.svg)](https://github.com/niall-byrne/panic/actions)

## OpenAPI Specification

Once the development container is running, you can interact with the OpenApi Interface.

Launch the container (instructions below) then create an admin user so you can login:
- `cd /app/panic`
- `python manage.py autoadmin`
- Login via the admin interface: 
  - http://localhost:8080/admin  (admin/admin)
- View the OpenAPI interface: 
  - http://localhost:8080/swagger/

## Development Dependencies

You'll need to install:
 - [Docker](https://www.docker.com/) 
 - [Docker Compose](https://docs.docker.com/compose/install/)

## Setup the Development Environment

Build the development environment container (this takes a few minutes):
- `docker-compose build`

Start the environment container:
- `docker-compose up -d`

Spawn a shell inside the container:
- `./container`

## Install the Project Packages on your Host Machine
This is useful for making your IDE aware of what's installed in a venv.

- `pip install pipenv`
- `source scripts/dev`
- `dev setup` (Installs the requirements.txt in the `assets` folder.)
- `pipenv --venv` (To get the path of the virtual environment for your IDE.)

## Environment
The [local.env](environments/local.env) file can be modified to inject environment variable content into the container.

You can override the values set in this file by setting shell ENV variables prior to starting the container:
- `export GIT_HOOKS_PROTECTED_BRANCHES='.*'`
- `docker-compose kill` (Kill the current running container.)
- `docker-compose rm` (Remove the stopped container.)
- `docker-compose up -d` (Restart the dev environment, with a new container, containing the override.)
- `./container`

## Git Hooks
Git hooks are installed that will enforce linting and unit-testing on the specified branches.
The following environment variables can be used to customize this behavior:

- `GIT_HOOKS` (Set this value to 1 to enable the pre-commit hook)
- `GIT_HOOKS_PROTECTED_BRANCHES` (Customize this regex to specify the branches that should enforce the Git Hook on commit.)

## CLI Reference
The CLI is enabled by default inside the container, and is also available on the host machine.
Run the CLI without arguments to see the complete list of available commands: `$ dev`

## Installing Dev CLI on a OSX host (outside the container)

You need the Postgresql CLI installed, [here's](https://www.compose.com/articles/postgresql-tips-installing-the-postgresql-client/
) how on a Mac.

If you're on Mojave, you should run this command, prior to running `dev setup`:
- `export LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib"`

