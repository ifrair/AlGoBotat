#!/bin/sh
set -e
alembic upgrade heads
exec python main.py
