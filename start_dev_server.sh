#!/bin/bash

# Start Django development server with HTTP settings
echo "Starting Django development server with HTTP-only configuration..."
cd "$(dirname "$0")"

# Ensure we use HTTP
export PYTHONHTTPSVERIFY=0
export HTTPS=0

# Run the server
python manage.py runserver 0.0.0.0:8000
