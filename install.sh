#!/bin/bash

#Step 1) Check if root--------------------------------------
if [[ $EUID -ne 0 ]]; then
   echo "Please execute script as root." 
   exit 1
fi
#-----------------------------------------------------------

#Step 2) enable UART----------------------------------------
cd /boot/
File=config.txt
if grep -q "#enable_uart=1" "$File";
        then
                sed -i '/#enable_uart=1/c\enable_uart=1' "$File"
fi
if grep -q "enable_uart=1" "$File";
	then
		echo "UART already enabled. Doing nothing."
	else
		echo "enable_uart=1" >> "$File"
		echo "UART enabled."
fi
# Enable additional settings-------------------------------
if grep -q "#hdmi_drive=2" "$File";
        then
                sed -i '/#hdmi_drive=2/c\hdmi_drive=2' "$File";
fi
if grep -q "hdmi_drive=2" "$File";
	then
		echo "HDMI Sound already enabled. Doing nothing."
	else
		echo "hdmi_drive=2" >> "$File"
		echo "HDMI Sound enabled."
fi

#-----------------------------------------------------------

#Step 3) Update repository----------------------------------
sudo apt-get update -y
#-----------------------------------------------------------

#Step 4) Install gpiozero module----------------------------
sudo apt-get install -y python-dev python-pip python-gpiozero
sudo pip install psutil pyserial
sudo apt-get install wiringpi
#-----------------------------------------------------------

##Remove downloaded package files in order to free up space-
echo Remove downloaded package files
sudo apt-get clean
#-----------------------------------------------------------

#Step 5) Download Python script-----------------------------
cd /opt/
sudo mkdir PanelCtrl
cd /opt/PanelCtrl
script=panelctrl.py

if [ -e $script ];
	then
		echo "Script panelctrl.py already exists. Updating..."
                rm -r $script
		wget "https://raw.githubusercontent.com/mafe72/Manual-Pick-and-Place-Automatic-Tape-Feeder/scripts/panelctrl.py"
		echo "Update complete."
	else
		wget "https://raw.githubusercontent.com/mafe72/Manual-Pick-and-Place-Automatic-Tape-Feeder/scripts/panelctrl.py"
		echo "Download complete."
fi
#-----------------------------------------------------------

#Step 6) Enable Python script to run on start up------------
cd /etc/
RC=rc.local

#Adding script configuration-----------------------------------
echo Adding script configuration files to rc.local 
if grep -q "sudo python \/opt\/PanelCtrl\/panelctrl.py \&" "$RC";
	then
		echo "File /etc/rc.local already configured. Doing nothing."
	else
		sed -i -e "s/^exit 0/sudo python \/opt\/PanelCtrl\/panelctrl.py \&\n&/g" "$RC"
		echo "File /etc/rc.local configured."
fi
#-----------------------------------------------------------
#Step 7)  Reboot to apply changes----------------------------
echo "Installation done. Will now reboot after 3 seconds."
sleep 4
sudo reboot
#-----------------------------------------------------------
