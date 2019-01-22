#!/bin/bash

#Step 1) Check if root--------------------------------------
if [[ $EUID -ne 0 ]]; then
   echo "Please execute script as root." 
   exit 1
fi
#-----------------------------------------------------------

#Step 2) Remove Installation directory ---------------------

sudo rm -r PanelCtrl

#-----------------------------------------------------------

#Step 3) Remove configuration script ------------
cd /etc/
RC=rc.local

#Cleaning rc.local configration files --------------------
echo Cleaning configration files from rc.local
if grep -q "sudo python3 \/opt\/PanelCtrl\/panelctrl.py \&" "$RC";
        then
               sed -i '/sudo python3 \/opt\/PanelCtrl\/panelctrl.py \&/c\' "$RC";

#-----------------------------------------------------------
#Step 4) Reboot to apply changes----------------------------
echo "Script un-install complete. Will now shutdown after 3 seconds."
sleep 4
sudo shutdown -h now
#-----------------------------------------------------------
