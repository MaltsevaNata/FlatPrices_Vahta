#!/bin/sh

gunicorn -c gunicorn_conf.py wsgi_app:app --worker-class eventlet --reload
exec "$@"