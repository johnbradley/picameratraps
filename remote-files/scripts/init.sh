#!/bin/bash
set -e

echo "Install software for pi camera v3"
sudo apt-get update -y
sudo apt-get upgrade -y

echo "Install software for pijuice"
sudo apt-get install pijuice-base units -y

echo "Creating logs/ directory"
mkdir -p logs

echo "Setup automatically set system clock from RTC on boot"
sudo cp rc.local /etc/rc.local

echo "Ensuring PiJuice RTC is properly setup"
if grep 'dtoverlay=i2c-rtc,ds1307=1' /boot/config.txt
then
    echo "The PiJuice RTC overlay is already setup in /boot/config.txt"
else
    echo "Adding PiJuice RTC overlay to /boot/config.txt."
    sudo sh -c "echo 'dtoverlay=i2c-rtc,ds1307=1' >> /boot/config.txt"
    echo "!! Rebooting for RTC overlay to take effect !!"
    sudo shutdown -r now
fi