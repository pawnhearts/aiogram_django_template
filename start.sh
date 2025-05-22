#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset


#uv run ./manage.py collectstatic --noinput
uv run ./manage.py migrate
uv run gunicorn config.wsgi --bind 0.0.0.0:8000 --chdir=/app --reload