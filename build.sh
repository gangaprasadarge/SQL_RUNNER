#!/bin/bash
set -e

echo "=== Starting build process ==="
echo "Current directory: $(pwd)"

cd backend

echo "=== Installing dependencies ==="
pip install -r requirements.txt

echo "=== Running Django migrations ==="
python manage.py migrate --noinput

echo "=== Initializing database ==="
python init_db.py

echo "=== Collecting static files ==="
python manage.py collectstatic --noinput

echo "=== Build complete! ==="
