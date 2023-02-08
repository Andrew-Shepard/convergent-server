#!/bin/bash
set -o nounset -o errexit -o xtrace

echo "Waiting for db..."
while ! nc -z "$POSTGRES_HOST" 5432
    do
        echo sleeping
        sleep 1
    done
echo "Response from db!"

if [[ "$CREATEDB" == 'true' ]]; then 
    echo "Setting up database..."
    cd /app/utility
    python3 /app/utility/manage_db.py create
fi

cd /app
alembic upgrade head
