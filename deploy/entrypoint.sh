#!/usr/bin/env bash

abort()
{
    echo -e "\e[1;31m
    --------------------------------------------
    Some errors occurred, HBUOJ failed to start.
    --------------------------------------------
    \e[0m"
    exit 1
}
trap 'abort' ERR

echo -e "\e[1;32m
  _   _ ____  _   _  ___      _
 | | | | __ )| | | |/ _ \    | |
 | |_| |  _ \| | | | | | |_  | |
 |  _  | |_) | |_| | |_| | |_| |
 |_| |_|____/ \___/ \___/ \___/
\e[0m"

echo -e "\e[1;32m 1. Initializing configuration \e[0m"

if [[ -z $MAX_WORKER_NUM ]]; then
    export CPU_CORE_NUM=$(grep --count ^processor /proc/cpuinfo)
    if [[ $CPU_CORE_NUM -gt 4 ]]; then
        export MAX_WORKER_NUM=4
    else
        export MAX_WORKER_NUM=$((CPU_CORE_NUM))
    fi
fi

export SUPERVISOR_LOGS_SIZE=10240000
export SUPERVISOR_LOGS_BACKUPS=5
export SUPERVISOR_STARTSECS=5
export SUPERVISOR_STARTRETRIES=10

ln -sf "$SITE_BASE/deploy/supervisord.conf" /etc/supervisord.conf
ln -sf "$SITE_BASE/deploy/local_settings.py" site/hbuoj/local_settings.py
ln -sf "$SITE_BASE/deploy/config.js" site/websocket/config.js
rm /etc/nginx/sites-enabled/*
ln -sf "$SITE_BASE/deploy/nginx.conf" /etc/nginx/site-enabled
service nginx reload

echo -e "\e[1;32m 2. Migrating database \e[0m"

cd $SITE_BASE
sh make_style.sh
python3 manage.py collectstatic
python3 manage.py compilemessages
python3 manage.py compilejsi18n
python3 manage.py migrate

echo -e "\e[1;32m 3. Initializing database \e[0m"

python3 manage.py loaddata navbar
python3 manage.py loaddata language_small
python3 manage.py loaddata demo

echo -e "\e[1;32m 4. Starting services \e[0m"

exec supervisord -c "$SITE_BASE/deploy/supervisor/supervisord.conf"

abort