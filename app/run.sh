#!/usr/bin/env bash

set -e

if [ "$ENV" = 'DEV' ]; then
    echo "EXECUTANDO SERVIDOR DE DESENVOLVIMENTO"
    exec python "run.py"
else
    echo "EXECUTANDO SERVIDOR DE PRODUCAO"
    exec uwsgi --http 0.0.0.0:9090 --wsgi-file /app/run.py \
                --callable app --stats 0.0.0.0:9191
fi
