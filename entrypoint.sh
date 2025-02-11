#!/bin/bash

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