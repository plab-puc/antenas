import RPi.GPIO as GPIO
import sys, tty, termios, time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

mot1 = 14
mot2 = 15

GPIO.setup(mot1, GPIO.OUT)
GPIO.setup(mot2, GPIO.OUT)

def rodaEsq:
	GPIO.output(mot1, 1)
	GPIO.output(mot2, 0)
	time.sleep(1)

while True:
	rodaEsq()
		
	GPIO.output(mot1, 0)
	GPIO.output(mot2, 1)


	GPIO.output(mot1, 1)
	GPIO.output(mot2, 1)
