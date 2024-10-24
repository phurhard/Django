#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e
pip install -r requirements.txt

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Create superuser if it does not exist
echo "Creating superuser..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()

# Customize these credentials as needed
SUPERUSER_EMAIL = 'admin@example.com'
SUPERUSER_PASSWORD = 'password'

if not User.objects.filter(email=SUPERUSER_EMAIL).exists():
    User.objects.create_superuser(SUPERUSER_EMAIL, SUPERUSER_PASSWORD)
    print('Superuser created.')
else:
    print('Superuser already exists.')

import seed
EOF

# Seed the database with initial data
echo "Build script completed successfully."
