#!/usr/bin/python
# Import required libraries
import sys
import time
import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
 
# Define GPIO signals to use
# Physical pins 11,15,16,18
# GPIO17,GPIO22,GPIO23,GPIO24
StepPins = [10,9,11,25]
 
# Set all pins as output
for pin in StepPins:
	print "Setup pins"
	GPIO.setup(pin,GPIO.OUT)
	GPIO.output(pin, False)
 
# Define advanced sequence
# as shown in manufacturers datasheet
Seq = [[1,0,0,1],
			 [1,0,0,0],
			 [1,1,0,0],
			 [0,1,0,0],
			 [0,1,1,0],
			 [0,0,1,0],
			 [0,0,1,1],
			 [0,0,0,1]]
				
StepCount = len(Seq)
StepDir = 1 # Set to 1 or 2 for clockwise
						# Set to -1 or -2 for anti-clockwise

VoltaCompleta = 4076

SomatorioPassos = 0
 
# Read wait time from command line
if len(sys.argv)>1:
	WaitTime = int(sys.argv[1])/float(1000)
else:
	WaitTime = 4/float(1000)
 
# Initialise variables
StepCounter = 0

def RodarDir(angulo):
	global StepDir, VoltaCompleta
	StepDir = 1
	Rodar((angulo/float(360)) * VoltaCompleta)

def RodarEsq(angulo):
	global StepDir, VoltaCompleta
	StepDir = -1
	Rodar((angulo/float(360)) * VoltaCompleta)

def AnguloRodado():
	global SomatorioPassos, VoltaCompleta
	return(SomatorioPassos/VoltaCompleta * 360)

def Rodar(steps):
	global Seq, StepCounter, StepCount, StepDir, WaitTime, SomatorioPassos
	
	contador = 0
	
	while(contador < steps):
		for pin in range(0,4):
			xpin=StepPins[pin]# Get GPIO
			if Seq[StepCounter][pin]!=0:
				print " Enable GPIO %i" %(xpin)
				GPIO.output(xpin, True)
			else:
				GPIO.output(xpin, False)
	 
		StepCounter += StepDir

		SomatorioPassos+=StepDir
		contador+=1
	 
		# If we reach the end of the sequence
		# start again
		if (StepCounter>=StepCount):
			StepCounter = 0
		if (StepCounter<0):
			StepCounter = StepCount+StepDir
	 
		# Wait before moving on
		time.sleep(WaitTime)
