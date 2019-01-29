#####################################
# RetroFlag NESPi Control Board Script
#####################################
# Hardware:
# Board by Eladio Martinez
# http://mini-mods.com
#
#####################################
# Wiring:
#  GPIO 2  Reset Button (INPUT)
#  GPIO 3  Power Button (INPUT)
#  GPIO 4  Fan on signal (OUTPUT)
#  GPIO 14 LED on signal (OUTPUT)
#
#####################################
#  Required python libraries
#  sudo apt-get update
#  sudo apt-get install python-dev python-pip python-gpiozero
#  sudo pip install psutil pyserial
#
#####################################
# Basic Usage:
#  POWER ON
#    While powered off
#    Press (LATCH) POWER button
#	 LED will turn ON
#    Wait for Raspberry Pi to boot
#  POWER OFF
#    While powered on
#    Press (Unlatch) POWER button
#	 LED will turn OFF
#    Wait for Raspberry Pi to shutdown
#  Press RESET 
#	 LED will BLINK
#    Wait for Raspberry Pi to reboot
#  Fan control
#	 FAN will turn ON if CPU temp exceeded 55C and turn OFF when CPU temp is under 40C

import time
import os
import socket
from gpiozero import Button, LED, DigitalOutputDevice

resetButton = Button(2)
powerButton = Button(3)
fan = DigitalOutputDevice(4)
ledPin = LED(14)


#Get CPU Temperature
def getCPUtemp():
	res = os.popen('vcgencmd measure_temp').readline()
	return (res.replace("temp=","").replace("'C\n",""))
	
while True:
	#Power / LED Control
	#When power button is unlatched turn off LED and initiate shutdown
	if not powerButton.is_pressed:
		print ("Shutting down...")
		os.system("shutdown -h now")
		break
	else:
		ledPin.on()  #Take control of LED instead of relying on TX pin
		
	#RESET Button pressed
	#When Reset button is presed system reboot
	if resetButton.is_pressed:
                print ("Rebooting...")
		ledPin.blink(.2,.2)
		os.system("reboot")

	#Fan control
	#Adjust MIN and MAX TEMP as needed to keep the FAN from kicking
	#on and off with only a one second loop
	cpuTemp = int(float(getCPUtemp()))
	fanOnTemp = 55  #Turn on fan when exceeded
	fanOffTemp = 40  #Turn off fan when under
	if cpuTemp >= fanOnTemp:
		fan.on()
	if cpuTemp < fanOffTemp:
		fan.off()
	time.sleep(1.00)
