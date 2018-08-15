#!/usr/bin/env bash
set -e

docker-compose up -d redis db
sleep 10
flake8 .
python manage.py check
./make_style.sh
python manage.py collectstatic
python manage.py compilemessages
python manage.py compilejsi18n
python manage.py migrate
python manage.py loaddata initial_data
