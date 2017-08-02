import socket
import sys
import DistanceSensor
import MotorCarrinho
import CheckWifi

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('', 10008)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

distancias = [20, 30, 40, 60]
distAtual = 0

def median(lst):
    lst = sorted(lst)
    if len(lst) < 1:
            return None
    elif len(lst) %2 == 1:
            return lst[((len(lst)+1)/2)-1]
    else:
            return float(sum(lst[(len(lst)/2)-1:(len(lst)/2)+1]))/2.0

def MoveTo(d):
	global distAtual
	global distancias

	if(d < 0 or d >= len(distancias)):
		return
		
	terminou = False

	while(terminou == False):
		medicoes = []
		
		for i in range(0,10):
			medicoes.append(DistanceSensor.TestDistance())

		mediana = median(medicoes)
		print mediana

		if(mediana > distancias[d] + 2):
			print "frente"
			MotorCarrinho.rodaEsqfrente()
			MotorCarrinho.rodaDirfrente()
			#Mover pra frente!
		elif(mediana < distancias[d] - 2):
			print "tras"
			MotorCarrinho.rodaEsqtras()
			MotorCarrinho.rodaDirtras()
			#Mover pra tras!
		else:
			MotorCarrinho.parar()
			terminou = True
			#Parar!

	distAtual = d

while True:
	MoveTo(0)
	MotorCarrinho.parar()
	
	# Wait for a connection
	print >>sys.stderr, 'waiting for a connection'
	connection, client_address = sock.accept()

	try:
		print >>sys.stderr, 'connection from', client_address

		while True:
			data = connection.recv(1)

			if data!="":
				print >>sys.stderr, 'received "%s"' % data
				
				if(data == 'u'):
					print >>sys.stderr, 'Frente'
					MoveTo(distAtual+1)
				elif(data == 'd'):
					print >>sys.stderr, 'Tras'
					MoveTo(distAtual-1)
				elif(data == 'c'):
					print >>sys.stderr, 'Closing: ', client_address
					break
				elif(data=='s'):
					mensagem = ""
					
					for i in range(0,10):
						signal= CheckWifi.Do()

						mensagem += str(signal)
						
						if(i!=9): mensagem += "|"
						
					connection.send(mensagem)
			else:
				print("cliente desconectado")
				MoveTo(0)
				MotorCarrinho.parar()
				break			
	finally:
		connection.close()
