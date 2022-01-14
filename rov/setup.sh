#!/bin/bash

# To run the script :
: '

wget https://raw.githubusercontent.com/Nibathron/flaskapp/main/rov/setup.sh && chmod +x setup.sh && ./setup.sh

'



###
# The script can run on a fresh Raspberry Pi, everything is downloaded, installed and configured.
# Tested on RPi4 and Bullseye.

# Credits to :
# Ted Mielczarek https://github.com/luser/gamepadtest.git
# Nazmus Nasir https://github.com/naztronaut/RaspberryPi-RGBW-Control

: '
```
  Function        GPIO    40-Pin header
 ---------------------------------------
  Right Forward    24        18  
  Right Reverse    25        22
  Left Forward     20        38
  Left Reverse     18        12
```
'


sudo apt update
sudp apt upgrade -y

#sudo apt remove -y python2
#sudo apt remove -y python-is-python2
#sudo apt autoremove -y --purge
#sudo apt update

sudo apt install -y git vim

sudo apt install -y python3 python3-pip

sudo apt install -y apache2
sudo apt install -y libapache2-mod-wsgi-py3

#sudo apt-get install -y python-is-python3

# TODO investigate a bit regarding the pigpio https://abyz.me.uk/rpi/pigpio/download.html

sudo apt install -y pigpio
sudo apt install -y python3-pigpio

# Auto-/start the pigpio daemon
sudo systemctl enable pigpiod
sudo systemctl start pigpiod 

sudo pip3 install flask

# TODO: Check what/why
sudo a2enmod headers


git clone https://github.com/Nibathron/flaskapp.git

cd ~/flaskapp/rov

sudo rm /var/www/html/index.html

sudo mkdir /var/www/html/rov

sudo cp apache-rov.conf /etc/apache2/sites-available/

sudo cp gamepadtest.js /var/www/html/
sudo cp index.html /var/www/html/

sudo cp rov.py /var/www/html/rov/
sudo cp rov.wsgi /var/www/html/rov/


sudo chown -R pi:pi /var/www/html

# Start the pigpio daemon (Also added to crontab in the end)
#sudo pigpiod

#sudo a2dissite apache-rov.conf
sudo a2dissite 000-default.conf

sudo a2ensite apache-rov.conf
#sudo service apache2 restart

sudo systemctl reload apache2

# Debugging Apache2
# tail -f /var/log/apache2/other_vhosts_access.log
# tail -f /var/log/apache2/error.log
# tail -f /home/pi/record.log







# In case the crontab does not exist we need to catch and handle some errors
# For testing, delete the cronab for user pi with :
#  crontab -r -u pi
# In the crontab add
# @reboot sudo pigpiod

#cat <(crontab -l 2>/dev/null) <(echo "@reboot sudo pigpiod") | crontab -
