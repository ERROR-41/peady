#!/bin/bash
# Install dependencies
pip install -r requirements.txt

# Make sure the static directory exists
mkdir -p staticfiles

# Collect static files
python manage.py collectstatic --noinput

echo "Build completed successfully"
