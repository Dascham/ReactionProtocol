'''
This is the Delegator, which will run on 1...n number of hosts in
a Mininet topology. Each delegator is responsible for listening for
panic signals from their own clients - to then pass on the data to
other delegators. Each delegator will request throttling (start or stop)
from a single ThrottleManager (POX module).
'''

import socket
import sys
import thread
import socket
import fcntl
import struct

# Connection details for the Print Server
# Runs outside of Mininet
printerIP = '192.168.2.4'
printerPORT = 8888

# Conncetion details for the ThrottleManager
# Runs outside of Mininet, as a POX module
throttleManagerIP = '192.168.2.4'
throttleManagerPORT = 7777

# A hardcoded list of delegators
DelegatorList = ['10.0.0.3', '10.0.0.4']

# Gets the proper IP for a host, like: 10.0.0.4
def getIpForThis():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("10.0.0.5", 80))
    return s.getsockname()[0]

# For ease of use, we print to a Print Server
def printToServer(string):
	try:
		printer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		printer.connect((printerIP, printerPORT))
		printer.send(string)
		printer.close()
	except Exception as e:
		print 'Could not send panic! ' + str(e)

def SendToThrottleManager(string):
	try:
		throttleManager = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		throttleManager.connect((throttleManagerIP, throttleManagerPORT))
		throttleManager.send(string)
		throttleManager.close()
	except Exception as e:
		print 'Could not send signal to ThrottleManager! ' + str(e)

# Request either a start- or stop-throttling from the ThrottleManager
def requestThrotttle(data):
	signalType, IP, sender = data.split('/')
	if signalType == 'PANIC':
		# Request start for the IP
		printToServer('Delegator '+getIpForThis()+' is requesting starting throttling for: ' + IP)
		SendToThrottleManager('START'+'/'+IP)
	elif signalType == 'STOP':
		# Request stop for the IP
		printToServer('Requesting '+getIpForThis()+'stop throttle for: ' + IP)
		SendToThrottleManager('STOP'+'/'+IP)

# This function sends the recieved data, onwards onto the
# other delegators, from 'DelegatorList'
# A delegator only forwards a signal if it came directly a client.
# Therefore the end of the data string is changed to indicate to other 
# delegators that this message comes from another delegator, and not a client
def sendToOtherDelegtors(data):
	signalType, IP, sender = data.split('/')
	if sender == 'CLIENT':
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
	# When messages are heard, we send to other delegator(s)
	# and request start- or stop-throttling from the ThrottleManager
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.bind((getIpForThis(), 8008))
	serversocket.listen(100)
	printToServer('Delegator: ' + getIpForThis() + ' started...')
	while True:
		connectionSocket, addr = serversocket.accept()
		data = connectionSocket.recv(4096)
		
		printToServer('Delegator at: ' + getIpForThis() + ' has recieved signal from: ' + str(addr) + ' DATA: ' + data)
		
		thread.start_new_thread(requestThrotttle, (data, ))
		thread.start_new_thread(sendToOtherDelegtors, (data, ))