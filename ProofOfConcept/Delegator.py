import socket
import sys
import thread
import socket
import fcntl
import struct

printerIP = '192.168.2.4'
printerPORT = 8888

DelegatorList = ['10.0.0.3', '10.0.0.4']

def getIpForThis():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("10.0.0.5", 80))
    return s.getsockname()[0]

def printToServer(string):
	try:
		printer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		printer.connect((printerIP, printerPORT))
		printer.send(string)
		printer.close()
	except Exception as e:
		print 'Could not send panic! ' + e

def requestThrotttle(data):
	signalType, IP, sender = data.split('/')
	if signalType == 'PANIC':
		#request panic for ip
		printToServer('Requesting starting throttling for: ' + IP)
	elif signalType == 'STOP':
		#request stop for ip
		printToServer('Requesting stop throttle for: ' + IP)

#ONLY if the signal just came from a client
def sendToOtherDelegtors(data):
	signalType, IP, sender = data.split('/')
	if sender == 'CLIENT':
		#We change the message, so that it says it comes from a delegator now
		newData = signalType+'/'+IP+'/'+'DELEGATOR'
		for delegator in DelegatorList:
			if delegator != getIpForThis():		
				try:
					sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					sender.connect((delegator, 8008))
					sender.send(newData)
					sender.close()
				except Exception as e:
					printToServer('Could not send panic to other delegator: ' + delegator + 'ERROR: ' + str(e))

if __name__ == "__main__":
	# Host a server, listening for client messages.
	# When messages are heard, send to other delegator
	# and request start or stop throttling
	printToServer('Delegator: ' + getIpForThis() + ' started')
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.bind((getIpForThis(), 8008))
	serversocket.listen(100)
	while True:
		#Listen messages from client(s) or other delegators
		connectionSocket, addr = serversocket.accept()
		data = connectionSocket.recv(4096)
		printToServer('Delegator at: ' + getIpForThis() + ' has recived signal from: ' + str(addr) + '&DATA&: ' + data)
		
		thread.start_new_thread(requestThrotttle, (data, ))
		thread.start_new_thread(sendToOtherDelegtors, (data, ))