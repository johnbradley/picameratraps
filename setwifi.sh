#!bin/bash
SSID=TODO
PASSWORD=TODO
echo "Setting WiFi to $SSID"
for HOST in $(./traplist.sh $1)
do
    echo "----------------------"
    echo "$HOST"
    echo "----------------------"
    ssh pi@$HOST sudo raspi-config nonint do_wifi_ssid_passphrase $SSID $PASSWORD
done
