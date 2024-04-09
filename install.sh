#!/bin/bash
#install.sh installs all the necessary libraries for testing and running the code.
#Raspbian image can be found here: https://downloads.raspberrypi.org/raspios_full_armhf/images/raspios_full_armhf-2021-05-28/2021-05-07-raspios-buster-armhf-full.zip
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get -y dist-upgrade

sudo chmod +x /home/pi/Desktop/RPiProject_Firebase/veye_raspivid

sudo apt-get -y install python3-pip python3-dev python3-setuptools i2c-tools python3-smbus python3-serial gpac supervisor speedtest-cli

sudo apt-get -y clean
sudo apt -y autoremove

sudo pip3 install setuptools
sudo pip3 install coverage
sudo pip3 install google-crc32c==1.0.0
sudo pip3 install pyparsing==2.4.7
sudo pip3 install getmac
sudo pip3 install wheel
sudo pip3 install numpy
sudo pip3 install google-auth-oauthlib
sudo pip3 install google-cloud-storage
sudo pip3 install firebase-admin
sudo pip3 install tzlocal

sudo cp /usr/share/zoneinfo/America/New_York /etc/localtime

mkdir -p /home/pi/Camera
cd /home/pi/Camera && git clone https://github.com/veyeimaging/raspberrypi.git
cd /home/pi/Camera/raspberrypi/i2c_cmd/bin && chmod ugo+x * && ./enable_i2c_vc.sh

cat /home/pi/Desktop/RPiProject_Firebase/rc.local | sudo tee /etc/rc.local

#sudo reboot
