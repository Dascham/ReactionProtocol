import socket
import thread
import sys
import time
import threading

# Pox module, responsible for listening for and acting upon throttle messages from delegators
ThrottleManager = ('192.168.2.2', 5001)

# Delegators are read in from a file
Delegators = []
# Switches are ???
Switches = []

# To keep track of shit
PanicSignals = []
StopSignals = []

#get IPs from file, and place into list of delegtors
def getOtherDelegatorsListFromFile():
	try:
		file = open("~/Desktop/delegatorIPs", "r")
		for line in file
			Delegators.append(line)
		file.close()
	except Exception as e:
		print 'Could not find delegtorsIPs file!'

# Get switches, from file, with filename <this delegator ip>
def getSwitchesForThisDelegator():
	thisDelegatorIP = socket.gethostbyname(socket.gethostname())
	try:
		file = open("$HOME/Desktop/Switches/" + thisDelegatorIP , "r")
		for line in file:
			Switches.append(line)
		file.close
	except Exception as e:
		print 'File containing switches for delegator: ' + thisDelegatorIP + ' could not be found!'

def printList(list):
	if list:
		for i in list:
			i.printer()
	else:
		print 'list is empty'

class Signal():
	isPanic = False
	isStop = False
	incidentNumber = None
	victimIP = None
	timestamp = None
	TTL = None # Time to Live - expressed in seconds

	# This will start in a thread, when a signal object is created.
	# If it ever expires (TTL has passed), it removes itself from the list
	'''
	def TTLDestroyer(self):
		while 1:
			if time.time() > self.timestamp + self.TTL: #If shit is outdated
				SendStringToThrottleManager(self.victimIP + '/' + 'STOP') #Request a it to sthap
				print 'signal from: ' + self.victimIP + ' has expired, and has been removed'
				# Remove self from lists
				if self in PanicSignals:
					PanicSignals.remove(self)
				elif self in StopSignals:
					StopSignals.remove(self)
				break
				#Delete entry in list, after send to ThrottleManager instead
	'''

	def printer(self):
		print '-------Signal Recieved-------' + '\nisPanic: ' + str(self.isPanic) + '\nisStop: ' + str(self.isStop) + '\nincNo: ' + str(self.incidentNumber) + '\nvictimIP: ' + str(self.victimIP) + '\ntimestmp: ' + str(self.timestamp) + '\nTLL: ' + str(self.TTL) + '\n-----------------------------'

	def __init__(self, signalType, victimIP, TTL, timestamp):
		if signalType is 'P':
			self.isPanic = True
		elif signalType is 'S':
			self.isStop = True

		self.incidentNumber = len(PanicSignals)+1
		self.victimIP = victimIP
		self.timestamp = time.time()
		self.TTL = TTL
		#thread.start_new_thread(self.TTLDestroyer, ())
		self.printer()

# Decide what to do with a signal
def ProcessSignal(data):
	signal = SignalParser(data)
	if signal.isPanic is True:
		PanicSignals.append(signal)

		# Request some throttle action!
		SendStringToThrottleManager(signal.victimIP + '/' + 'START' + '/' + signal.TTL)

	elif signal.isStop is True:
		StopSignals.append(signal)
		for entry in PanicSignals:
			if entry.incidentNumber is signal.incidentNumber:
				PanicSignals.remove(entry)
		
		#request throttling to stop
		SendStringToThrottleManager(signal.victimIP + '/' + 'STOP')

#Takes a signal string, and makes a usable object out of it
def SignalParser(data):
	signal = None

	#Extract data to variables
	signalType, IP, TTL, timestamp = data.split('/')
	TTL = int(TTL)

	#Make object
	signal = Signal(signalType, IP, TTL, timestamp)
	return signal

# Should do same for both panic- and stop-signal
def PropergateToOthers(data):
	thisDelegator = socket.gethostbyname(socket.gethostname())
	for delegator in Delegators:
		if delegator != thisDelegator:
			thread.start_new_thread(SendSignalToDelegator, (data, delegator))

def SendSignalToDelegator(data, targetIP):
	try:
		print 'Forwarding to delegator at: ' + targetIP + ' ...'
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((targetIP, 8085))
		sock.send(data)
		sock.close()
	except Exception as e:
		print 'Delegator at: ' + targetIP + ' could not be reached.'

def SendStringToThrottleManager(str):
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect(Pox)
		print 'Sending: ' + str + ' to ThrottleManager...'
		sock.send(str)
		print 'Successfully sent: ' + str + ' to ThrottleManager' 
		sock.close()
	except Exception as e:
		#print e
		print 'Could not connect to ThrottleManager!'

# Host a server, listening for signals on port: 8085
if __name__=='__main__':
	# Read in addresses of other delegators, and a list of switches assigned to this delegator
	DelegatorID = int(sys.argv[1])
	getOtherDelegatorsListFromFile()
	getSwitchesForThisDelegator()
	host = socket.gethostbyname(socket.gethostname()) #Gets the IP of the machine (not the localhost address)
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.bind((host, 8085))
	serversocket.listen(999)
	while 1:
		# Accept socket
		connectionSocket, addr = serversocket.accept()
		
		# Read in data 
		data = connectionSocket.recv(1024)
		print 'data recieved: ' + data
		
		# Dispatch thread to send signal to delegators
		thread.start_new_thread(PropergateToOthers, (data,) )

		# Handle the panic signal locally
		thread.start_new_thread(ProcessSignal, (data,) )