# picameratraps
This software allows management of multiple Raspberry Pi camera traps.

## SSH Key
To avoid entering a password many times you should have a SSH key setup.
See GitHub's documentation on [Checking for an existing SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/checking-for-existing-ssh-keys) 
and [Creating a SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent).
You will need the contents of your public key (~/.ssh/*.pub).

## Features
- Installs packages and camera trap scripts
- Setup a schedule for camera trap activities
  - Capture images/video
  - Set Alarms and Shutdown Raspberry Pi to conserve battery power
- Check status of all camera traps
- Download images/videos from the camera traps
- Purge old images/videos from the camera traps
- Stream video from a single camera trap to enable camera positioning

## Camera Trap Hardware
The camera trap hardware is based on [PICT (plant–insect interactions camera trap)](https://besjournals.onlinelibrary.wiley.com/doi/full/10.1111/2041-210X.13618).

The hardware we are currently using
- [Raspberrypi Zero W](https://www.raspberrypi.com/products/raspberry-pi-zero-w/)
- [Raspberry Pi Camera Module 3](https://www.raspberrypi.com/products/camera-module-3/)
- [PiJuice zero hat](https://uk.pi-supply.com/products/pijuice-zero)
- [PiJuice compatible battery](https://uk.pi-supply.com/products/pijuice-12000mah-battery?pr_prod_strat=copurchase&pr_rec_id=94106ed08&pr_rec_pid=2470820282449&pr_ref_pid=3189411381329&pr_seq=uniform)
- (optional) [PiJuice Solar Panel](https://uk.pi-supply.com/products/pijuice-solar-panel-6-watt)
- Case and mounting hardware

## Camera Trap Manual Setup
Each Raspberry Pi needs an SD card with the Raspberry Pi OS installed.
This is done by using [Raspbery Pi Imager](https://www.raspberrypi.com/software/).
Steps:
- Plug the SD card into your computer
- Launch Raspberry Pi Imager
- Choose `RASPBERRY PI OS LITE (32BIT)` for `Operating System`
- Choose your SD card for the `Storage`
- Click the Gear Icon
  - Check `Set hostname` and enter a unique name for the camera trap (eg `ct1-1`)
  - Check `Enable SSH` and choose `Allow public-key authentication` and set `authorized_keys` to your public key
  - Check Set username and password - Username must be set to `pi`
  - Check Configure wireless LAN and enter your WiFi information
- Click Write

## Edit Camera Trap settings
Before running the scripts you may need to edit:
- `cameratraps.txt` - this file contains the list of all camera trap host names (eg `ct1-1.local`)
- `remote-files/crontab.txt` - this file contains a schedule of when to run scripts in crontab format. See [crontab guru](https://crontab.guru/) for explation about the syntax.
- `remote-files/alarms.ini` - this file contains PiJuice settings for named alarms

## One-Time Initialization
Before you can perform the one-time init step the camera traps they must be turned on and accessible via WiFi.

Run the setup script to copy scripts and install software.
```
./init.sh
```
The first time you run this command on a Raspberry Pi you will be prompted to accept the key fingerprint.
Something like the following:
```
The authenticity of host 'ct1-1.local (...)' can't be established.
ED25519 key fingerprint is ....
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
```
As shown above enter yes.
The raspberry pi will likely be rebooted to handle a configuration change for the RTC.

## Setup Recording
Before you can run this script the camera traps they must be turned on and accessible via WiFi.
This script will copy scripts and update the job scheduler (crontab).
```
./setup.sh
```

## Check Camera Trap Status
```
./status.sh
```

## Stream Video from Camera Trap
This step requires that you have installed [VLC](https://www.videolan.org/vlc/) and uses two terminals.
You need pass the hostname of the camera trap to stream from.

So to start streaming video from trap `ct1-1.local` run the following:
```
./streamvid.sh ct1-1.local
```
Then in another terminal run the command printed bin a new termial to open VLC.
When through press Ctrl-C in the first terminal and close VLC.


## Update RTC from System clock
The RTC must be set initially and if the battery is depleted or disconnected from the PiJuice.
To sync the RTC clock from the system clock on the raspberry pi run:
```
./syncrtc.sh
```

## Retrieve images/videos
```
./fetch.sh
```

## Delete images/videos
```
./purge.sh
```


