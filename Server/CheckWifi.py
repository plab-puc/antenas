import os, struct, array
import sys
import subprocess
import signal
import time
import math

def Do ():
	p = subprocess.Popen("iwlist wlan1 scan", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

	ret = p.stdout.read()

	posNome = ret.find('RaspberryPi')

	if(posNome == -1):
		print("Nao encontrou a rede");
		return("Err");
	else:
		posDbm = ret[0:posNome].rfind('Signal level=')
		fimDbm = ret[0:posNome].rfind('dBm')
		
		leitura = int(ret[posDbm+13:fimDbm]);
		
		print("Signal level: "+str(leitura)+"dBm");
		return(leitura)
