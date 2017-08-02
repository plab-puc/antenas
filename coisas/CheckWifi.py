import os, struct, array
import sys
import subprocess
import signal
import time

p = subprocess.Popen("sudo iwlist wlan5 scan", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

ret = p.stdout.read()

posNome = ret.find('RaspberryPi')

if(posNome == -1):
	print("Nao encontrou a rede");
else:
	print(">>RaspberryPi")

	posDbm = ret[0:posNome].rfind('Signal level')

	fimDbm = ret[0:posNome].rfind('dBm')

	print("\t"+ret[posDbm:fimDbm+3])
