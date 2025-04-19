#!/bin/sh
set -e

# Install dependencies to handle potential container reuse
pip install --no-cache-dir -r requirements.txt

# Run the application
exec "$@"