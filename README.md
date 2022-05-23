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

The development shell might be used to execute arbitrary code in a fully
configured environment, without the need to manually configure the framework.

## Run migrations

Connected to the development container and running a pipenv shell, execute:

    python manage.py migrate

Migrations represents database changes created from our models classes, and are
managed by the framework.

## Run tests

Connected to the development container and running a pipenv shell, execute:

    python manage.py test

Tests help us to save time testing code manually, and are more reliable that
us developers.

## Run the server

Connected to the development container and running a pipenv shell, execute:

    python manage.py runserver

The development server is simple and can be used to test our application
locally.

## Run coverage

Connected to the development container and running a pipenv shell, execute:

    coverage run --include 'main/*' manage.py test
    coverage report --show-missing

The coverage helps us to track lines without tests, that might introduce bugs
in our application.

## Development workflow

01. Write models tests
    01. Create classes with `Test` suffix in `tests.py` module
    02. Create test methods (sorting, field validation, `__str__`)
    03. Run and fail the tests executing `python manage.py test`
02. Write models, pass
    01. Create classes in `models.py` module
    02. Create meta and fields definition
    03. Make migrations executing `python manage.py makemigrations`
03. Commit, push
    01. Executing `git add`, `git commit` and `git push`
04. Write forms tests
    01. Create classes with `Test` suffix in `tests.py` module
    02. Create test methods (form validation)
    03. Run and fail the tests executing `python manage.py test`
05. Write forms, pass
    01. Create classes in `forms.py` module
    02. Create forms definition 
06. Commit, push
    01. Executing `git add`, `git commit` and `git push`
07. Write views tests
    01. Create classes with `Test` suffix in `tests.py` module
    02. Create test methods (GET / POST requests, QuerySet)
    03. Run and fail the tests executing `python manage.py test`
08. Write views, pass
    01. Create classes in `views.py` module
    02. Create methods for GET / POST requests
09. Commit, push
    01. Executing `git add`, `git commit` and `git push`
10. Start over

# The MVT model

The Model View Template model is used by the framework to help us think and
organize code.

Models are classes that represents: (a) things in our domain, (b) validation
rules and (c) database read/write logic.

Views are functions and/or classes that defines what data should be presented
to users, and are responsible for: (a) receive a HTTP request and (b) return a
HTTP response, calling models, using templates, etc.

Templates are files that defines how data should be presented to users,
including using context variables defined in views.
