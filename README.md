# Promo System

## About

> **Brief** — You are required to design a promo system in which users are assigned various
promos and can use the promo points in a specific task of their choosing.

## Installation & Configuration

1. Set up the PostgreSQL database
    - `sudo apt-get update && sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib`
    - `sudo -u postgres psql`
        ```
        CREATE DATABASE <database_name>;

        CREATE USER <database_user> WITH PASSWORD '<database_use_password>';

        ALTER ROLE <database_user> SET client_encoding TO 'utf8';

        ALTER ROLE <database_user> SET default_transaction_isolation TO 'read committed';

        ALTER ROLE <database_user> SET timezone TO 'UTC';

        GRANT ALL PRIVILEGES ON DATABASE <database_name> TO <database_user>;

        \q
        ```


2. Set up the Django project
    - `git clone https://github.com/MShbana/promo-system.git`
    - `python3 -m venv promo-system-venv`
    - `source promo-system-venv/bin/activate`
    - `pip install -r requirements.txt`
    - `cd promo-system`
    - `nano ~/.bashrc`
        ```
        export DEBUG=True
        export SECRET_KEY=<placeholder>

        export DATABASE_ENGINE=django.db.backends.postgresql
        export DATABASE_NAME=<database_name>
        export DATABASE_HOST=localhost
        export DATABASE_PORT=5432
        export DATABASE_USER=<database_user>
        export DATABASE_PASSWORD=<database_use_password>
        ```
    - Open a new terminal.
    - `python manage.py shell`
        ```
        from django.core.management.utils import get_random_secret_key
        get_random_secret_key()
        exit()
        ```
    - `nano .env`
        ```
        SECRET_KEY=<secret_key_generated_in_the_step_above>
        ```
    - `python manage.py migrate`
    - `python manage runserver`
