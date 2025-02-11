#!/bin/bash

echo "Waiting for the database to start..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database is up!"

if [ "$AUTO_GENERATE_MIGRATIONS" = "true" ]; then
  echo "Generating migrations..."
  prisma migrate deploy
  echo "Applying migrations..."
fi

echo "Starting Bot..."
python3 bot.py &

echo "Starting wait_transaction script..."
python3 ton_monitor.py &

wait