#!/bin/bash

if grep 'dtoverlay=disable-bt' /boot/config.txt
then
    echo "Bluetooth is already disabled!!"
else
    echo "Adding disable-bt overlay to /boot/config.txt."
    sudo sh -c "echo 'dtoverlay=disable-bt' >> /boot/config.txt"\

    echo "Disabling bluetooth services."
    sudo systemctl disable hciuart.service
    sudo systemctl disable bluealsa.service
    sudo systemctl disable bluetooth.service

    echo "!! Rebooting for RTC overlay to take effect !!"
    sudo shutdown -r now
fi
