import socket
import thread
import sys
import time

Pox = ('192.168.2.2', 6634)

# We assume this list of delegators also contains IP to this delegator
Delegators = ['10.0.0.56', '10.0.0.87']
switches = []

# To keep track of shit
# If a stop signal is recieved, the coresponding panic entries should be removed 
PanicSignals = []
StopSignals = []

class Signal():
	isPanic = false
	isStop = false
	incidentNumber = None
	victimIP = None
	timestamp = None
	TTL = None #Expressed in seconds

	def __init__(self, isPanic, isStop, incidentNumber, victimIP, TTL):
        self.isPanic = isPanic
        self.isStop = isStop
        self.incidentNumber = incidentNumber
        self.victimIP = victimIP
        self.timestamp = time.now()
        self.TTL = TTL

# Host a server, listening for signals on port: 80085
if __name__=='__main__':
	host = socket.gethostbyname(socket.gethostname()) #Gets the IP of the machine (not the localhost address)
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.bind((host, 80085))
	serversocket.listen(99)
	while 1:
		# Accept socket
	    clientsock, addr = serversocket.accept()
	    # Read signal
	    data = clientsock.recv(1024)
	    # Dispatch thread to send signal to delegators
	    thread.start_new_thread(Propergate, data)
	    # Handle the panic signal locally
	    thread.start_new_thread(ProcessSignal, data)

#Decide what to do with a signal
def ProcessSignal(data):
	signal = SignalParser(data)
    if signal.isPanic is true
    	PanicSignals.append(signal)

    	#request some throttle action!
    	SendStringToPox(signal.victimIP + '/' + 'start')

    elif signal.isStop is true
    	StopSignals.append(signal)
    	for entry in PanicSignals:
    		if entry.incidentNumber is signal.incidentNumber
    			PanicSignals.remove(entry)
    	
    	#request throttling to stop
    	SendStringToPox(signal.victimIP + '/' + 'stop')

#Takes a signal string, and makes a usable object out of it
def SignalParser(data):
	signal = None
	if data[:1] is 'P':
		signal = Signal(true, false, len(PanicSignals)+1, data[1:], 300)
	elif data [:1] is 'S'
		signal = Signal(false, true, len(StopSignals)+1, data[1:], 0)
	return signal

# Should do same for both panic- and stop-signal
def Propergate(data):
	thisDelegator = socket.gethostbyname(socket.gethostname())
	for delegator in Delegators:
		if delegator not thisDelegator
			thread.start_new_thread(SendSignalToDelegator, (data, delegator))

def SendSignalToDelegator(data, targetIP):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((targetIP, 80085))
	sock.send(data)
	sock.close()


def SendStringToPox(str):
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect(Pox)
		print 'Sending: ' + str + ' to POX'
		sock.send(str)
		print 'Successfully sent!'
		sock.close()
	except Exception as e:
		print e