#!/bin/bash

echo "Starting GPIO script..."
python /home/pi/mail_box/beam.py &
echo "Starting webserver..."
node /home/pi/mail_box/web_server/index.js &
