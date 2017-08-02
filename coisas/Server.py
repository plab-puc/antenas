import socket
import sys
import teste

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 1000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    try:
        print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(1)

			if data:
				print >>sys.stderr, 'received "%s"' % data
				ProcessarEntrada(data)

			#connection.sendall(data)
            
    finally:
        # Clean up the connection
        connection.close()

def ProcessarEntrada(data):
	if(data == 'u'):
		print >>sys.stderr, 'Frente'
		teste.frente(2*teste.TS)
	elif(data == 'd'):
		print >>sys.stderr, 'Tras'
		teste.tras(2*teste.TS)
	elif(data == 'l'):
		print >>sys.stderr, 'Esq'
		teste.rotacionaEsq(2*teste.TS)
	elif(data == 'r'):
		print >>sys.stderr, 'Dir'
		teste.rotacionaDir(2*teste.TS)
	elif(data == 'c'):
		teste.reset
		print >>sys.stderr, 'Closing: ', client_address
		break
