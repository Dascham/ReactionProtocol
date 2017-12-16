#This will recieve attack detection from the Forwarder, and pass the information on to the local delegator.
#The Linker will run within Mininet

#this file should probably be called "Client"

#Run as: python Linker.py <delegator-IP> <delegator-Port>

import socket
import thread
import sys
import time

#This should be changed so that it comes in as args
#delegator = ('10.0.0.56', 80085) #Placeholder address
delegator = None

def SendPanic(clientsock, addr):
	try:
		data = clientsock.recv(1024)
		TTL = 10
		print 'recived: ' + data

		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect(delegator)
		data = 'P'+'/'+data+'/'+str(TTL)+'/'+str(time.time())
		print 'parsing: ' + data + ' on to the delegator...'
		sock.send(data) #Send Panic signal, P for Panic
		sock.close()
		print 'parsed to delegator successfully!'
	except Exception as e:
		print e
		print 'failed to connect to delegator'

def SendStop(clientsock, addr):
	try:
		sock.connect(delegator)
		print 'sending stop for data: ' + data
		data = clientsock.recv(1024)
		clientsock.send('S'+data)
		print 'stop sent!'
		clientsock.close()
	except Exception as e:
		print e

#Host a server, listening for messages from the forwarder
if __name__=='__main__':
	delegator = (sys.argv[1], int(sys.argv[2]))
	host = socket.gethostbyname(socket.gethostname())
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.bind((host, 1337))
	serversocket.listen(99)
	while 1:
	    clientsock, addr = serversocket.accept()
	    thread.start_new_thread(SendPanic, (clientsock, addr))
	    #time.sleep(120)
	    #thread.start_new_thread(SendStop, (clientsock, addr))
