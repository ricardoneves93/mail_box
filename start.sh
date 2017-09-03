#!/bin/bash

echo "Starting webserver..."
gunicorn app:app --worker-class gevent -b 0.0.0.0:8090 --log-file=/home/pi/Desktop/log.log --daemon
echo "Starting GPIO script..."
python beam.py &
