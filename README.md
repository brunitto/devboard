# DEVBOARD

A simple developers discussion board, where you can share knowledge about
software development.

# Development environment

This project uses containers for the development environment, using Docker and
the VS Code Remote Container extension.

## Requirements

1. Docker
2. VS Code
3. Remote Container extension
4. Git

## Setup

Open Visual Studio Code, it will detect the `.devcontainer.json` file within
the `.devcontainer` directory and builds the development environment, using the
`Dockerfile`.

Connect to the development container and execute:

    pipenv install
    pipenv install --dev

## Run development shell

Connected to the container, run a pipenv shell:

    pipenv shell

## Run migrations

Connected to the development container and running a pipenv shell, execute:

    python manage.py migrate

## Run tests

Connected to the development container and running a pipenv shell, execute:

    python manage.py test

## Run the server

Connected to the development container and running a pipenv shell, execute:

    python manage.py runserver

## Run coverage

Connected to the development container and running a pipenv shell, execute:

    coverage run --include 'main/*' manage.py test
    coverage report --show-missing

## Development workflow

1. Write models tests
2. Write models, pass
3. Commit, push
4. Write forms tests
5. Write forms, pass
6. Commit, push
7. Write views tests
8. Write views, pass
9. Commit, push
