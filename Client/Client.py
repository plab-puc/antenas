import socket
import select
import sys
import thread
from threading import Thread

connected = False
connectCallback = None
disconnectCallback = None

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def ConnectThreaded():
	global connected
	global connectCallback
	
	if(connected == False):
		print("connect")
		
		try:
			# Connect the socket to the port where the server is listening
			server_address = ('127.0.0.1', 10008)
			print('connecting to %s port %s' % server_address)
			sock.connect(server_address)
			connected = True
			connectCallback()
		except socket.error, msg:
			print(msg)
			return
			

# Thread de conexao 
t = Thread(target=ConnectThreaded)

def Connect():
	global connected
	global t

	if(t.is_alive() == False and connected == False):
		t = Thread(target=ConnectThreaded)
		t.start()

def Send(message):
	sock.send(message)

def SendAndWait(message):
	Send(message)
	
	print("Enviou. Esperando resposta...")
	
	recebido = sock.recv(500)
	
	data = recebido.split("|")
	
	print(data)
				
	if(data != ""):
		return(data)
	else:
		print ("NOOOOO")
		
# Send data
#message = sys.stdin.readline()
#sock.send(message)

# Look for the response
#amount_received = 0
#amount_expected = len(message)

#while amount_received < amount_expected:
#data = sock.recv(16)
#amount_received += len(data)
#print >>sys.stderr, 'received "%s"' % data

#if(message == 'c'):
#	break

def Close():
	global connected
	global disconnectCallback

	print('sending close message')
	Send('c')
	print('closing socket')
	sock.close()
	connected = False
	disconnectCallback()
