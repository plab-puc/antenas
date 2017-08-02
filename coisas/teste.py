import RPi.GPIO as GPIO
import sys, tty, termios, time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Motores
mot1 = 15
mot2 = 14
mot3 = 3
mot4 = 2

#Controle
rot=0;
distance=0;
TS=0.06;

GPIO.setup(mot1, GPIO.OUT)
GPIO.setup(mot2, GPIO.OUT)
GPIO.setup(mot3, GPIO.OUT)
GPIO.setup(mot4, GPIO.OUT)

def pare():
	GPIO.output(mot1, 1)
	GPIO.output(mot2, 1)
	GPIO.output(mot3, 1)
	GPIO.output(mot4, 1)

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
	
def rotacionaEsq(tempo):
	global rot
	rodaEsqtras()
	rodaDirfrente()
	rot=rot-tempo
	time.sleep(tempo)
	pare()
	
def rotacionaDir(tempo):
	global rot
	rodaDirtras()
	rodaEsqfrente()
	rot=rot+tempo
	time.sleep(tempo)
	pare()
	
def desrotacionar():
	global rot
	
	if(rot>0):
		rotacionaEsq(rot)
	elif(rot<0):
		rotacionaDir(-rot)
	
def frente(tempo):
	global rot, distance
	
	if(tempo > distance):
		tempo = distance

	desrotacionar()

	rodaDirfrente()
	rodaEsqfrente()
	
	distance-=tempo
	time.sleep(tempo)
	pare()
	
def tras(tempo):
	global rot, distance
	
	desrotacionar()
	
	rodaDirtras()
	rodaEsqtras()
	
	distance=distance+tempo
	time.sleep(tempo)
	pare()
		
	
def reset():
	global rot, distance
	
	if(distance>0):
		frente(distance)
