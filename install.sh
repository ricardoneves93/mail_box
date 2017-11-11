#!/bin/sh
sudo apt-get update
sudo apt-get install -y git
sudo apt-get install -y mongodb
sudo apt-get install -y pip
cd /home/pi
git clone https://github.com/ricardoneves93/mail_box.git
sudo pip install pymongo
sudo pip install pifcm
# Install nodejs for ARM Chips
wget http://node-arm.herokuapp.com/node_latest_armhf.deb 
sudo dpkg -i node_latest_armhf.deb
# Add crontab "@reboot sudo sh /home/pi/mail_box/launcher.sh > /home/pi/mail_box/logs/cronlog"
