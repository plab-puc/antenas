import RPi.GPIO as GPIO
import sys, tty, termios, time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Motores
mot1 = 15
mot2 = 14
mot3 = 3
mot4 = 2

GPIO.setup(mot1, GPIO.OUT)
GPIO.setup(mot2, GPIO.OUT)
GPIO.setup(mot3, GPIO.OUT)
GPIO.setup(mot4, GPIO.OUT)

def rodaEsqfrente():
	GPIO.output(mot1, 1)
	GPIO.output(mot2, 0)
	
def rodaDirtras():
	GPIO.output(mot3, 0)
	GPIO.output(mot4, 1)
	
def rodaEsqtras():
	GPIO.output(mot1, 0)
	GPIO.output(mot2, 1)
	
def rodaDirfrente():
	GPIO.output(mot3, 1)
	GPIO.output(mot4, 0)

def parar():
	GPIO.output(mot1, 1)
	GPIO.output(mot2, 1)
	GPIO.output(mot3, 1)
	GPIO.output(mot4, 1)
