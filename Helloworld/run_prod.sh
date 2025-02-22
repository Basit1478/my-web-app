#!/bin/bash
export FLASK_ENV=production
export FLASK_APP=wsgi.py
gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 120 wsgi:app 