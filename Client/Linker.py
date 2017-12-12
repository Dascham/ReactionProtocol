#This will recieve attack detection from the Forwarder, and pass the information on to the local delegator.
#The Linker will run within Mininet


#Server, listening for messages from the forwarder

import socket
import thread
import sys

def Handler(clientsock, addr):
	try:
		delegator = ('10.0.0.56', 8888) #Placeholder address/port
		data = clientsock.recv(1024)
		print 'recived: ' + data

		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect(delegator)
		print 'parsing: ' + data + ' on to the delegator...'
		clientsock.send(data)
		clientsock.close()
		print 'parsed to delegator successfully!'
	except Exception as e:
		print e
		print 'failed to connect to delegator'
		
#Host a server, listening for messages from the forwarder
if __name__=='__main__':
	host = socket.gethostbyname(socket.gethostname())
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.bind((host, 1337))
	serversocket.listen(99)
	while 1:
	    clientsock, addr = serversocket.accept()
	    thread.start_new_thread(Handler, (clientsock, addr))

