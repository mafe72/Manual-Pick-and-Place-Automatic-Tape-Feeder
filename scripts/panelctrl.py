#####################################
# Panel Control Board Script
#####################################
# Hardware:
# Board by Eladio Martinez
# http://mini-mods.com
#
#####################################
# Wiring:
#  GPIO 5  Power Button (INPUT)
#  GPIO 8  LED on signal (OUTPUT)
#  GPIO 12 Fan on signal (OUTPUT)
#  GPIO 16 Reset Button (INPUT)
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

import RPi.GPIO as GPIO
import time
import os
import socket
from gpiozero import Button, LED
GPIO.setmode(GPIO.BCM)

resetButton = 16
powerButton = Button(5)

GPIO.setup(12, GPIO.OUT)
fan = GPIO.PWM(12, 50) #PWM frequency set to 50Hz

led = LED(8)
hold = 2

rebootBtn = Button(resetButton, hold_time=hold)
GPIO.setup(resetButton,GPIO.IN, pull_up_down=GPIO.PUD_UP)

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
		led.on()  #Take control of LED instead
		
	#RESET Button pressed
		led.blink(.2,.2)
		os.system("reboot")

	#Fan control
	#Adjust MIN and MAX TEMP as needed to control the FAN state
	cpuTemp = int(float(getCPUtemp()))
	fanOnTemp = 55  #Turn on fan when exceeded
	fanOffTemp = 40  #Turn off fan when under
	if cpuTemp >= fanOnTemp:
		fan.start(90) #90% duty cycle
	if cpuTemp < fanOffTemp:
		fan.stop()
	time.sleep(1.00)
