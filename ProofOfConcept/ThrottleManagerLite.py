from pox.core import core
from pox.lib.recoco import Timer
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr
import thread
from threading import Thread
import socket
import os

log = core.getLogger("Report: ")

HOST = '192.168.2.4'
PORT = 7777

printerIP = '192.168.2.4'
printerPORT = 8888

# This stores a list of all current victim IPs
currentVictims = []

def printToServer(string):
	try:
		printer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		printer.connect((printerIP, printerPORT))
		printer.send(string)
		printer.close()
	except Exception as e:
		print 'Could not send to Print Server! ' + str(e)
'''
def ConfigureQueues(portName, q1Rate):
	os.system("sudo ovs-vsctl -- set Port "+str(portName)+" qos=@newqos -- \
--id=@newqos create QoS type=linux-htb other-config:max-rate=10000000 queues=0=@q0,1=@q1 -- \
--id=@q0 create Queue other-config:min-rate=10000000 other-config:max-rate=10000000 -- \
--id=@q1 create Queue other-config:min-rate="+str(q1Rate)+" other-config:max-rate="+str(q1Rate))
'''
def SendFlowMod(port, event, src, dst, placeInThrottleQueue):
	log.debug("sending throttle message")
	msg = of.ofp_flow_mod()
	msg.priority = 100
	msg.idle_timeout = 0
	msg.hard_timeout = 0 #10 minutes, hard timeout - this flowmod will expire after 10 mins
	msg.match.dl_type = 0x0800 #ipv4 traffic code
	msg.match.nw_src = src
	msg.match.nw_dst = dst
	if placeInThrottleQueue == True:
		msg.actions = [of.ofp_action_enqueue(port=port, queue_id=1)]
	elif placeInThrottleQueue == False:
		#msg.actions = [of.ofp_action_enqueue(port=port, queue_id=0)]
		msg.actions.append(of.ofp_action_enqueue(port=port, queue_id=0))
		#printToServer("removing actions!")
		#msg = None
		#msg = of.ofp_flow_mod(command=of.OFPFC_DELETE)
		printToServer("added to shitshitshit")
	event.connection.send(msg)

def SendStatsRequest():
	for con in core.openflow.connections:
		con.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))

def fuckItAll():
	msg = of.ofp_flow_mod(command=of.OFPFC_DELETE)
	for con in core.openflow.connections:
		con.send(msg)
		printToServer("REMOVED FUCKING EVERYTHING!!!")

def HandleFlowStats(event):
	for flows in event.stats:				#should only be a single flow, with a destination of victimIPAddress, however there could also not be one
		port = flows.actions[0].port
		for ip in currentVictims:
			if flows.match.nw_dst == ip:	#if destination of a flow matches the IP address of the current victim
				log.debug(flows.actions[0].port)
				SendFlowMod(port, event, flows.match.nw_src, flows.match.nw_dst, True)
		if flows.match.nw_dst not in currentVictims:
			SendFlowMod(port, event, flows.match.nw_src, flows.match.nw_dst, False)

def HandleSignal(data):
	# Signal format <START or STOP> / <victimIP>
	printToServer("ThrottleManager recieved signal: " + data)
	signalType, IP = data.split('/')
	if signalType == 'START':
		# Add to 'current victims' list
		currentVictims.append(IP)
		printToServer("Added to the currenct victims list: " + IP)
	elif signalType == 'STOP':
		# Remove from list of current victims
		for victim in currentVictims:
			if victim == IP:
				currentVictims.remove(victim)
				printToServer("Removed from current victims list: " + IP)

		for victim in currentVictims:
			printToServer("victim: " + victim)
		if not currentVictims:
			printToServer("List of victims is empty!")

#Will listen for messages from delegators, runs in a thread so it doesnt block the program 
def Server():
	#Server
	printToServer("ThrottleManager server started.")
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
	serversocket.bind((HOST, PORT))
	serversocket.listen(5)

	while 1:
		connectionSocket, addr = serversocket.accept()
		thread.start_new_thread(HandleSignal, (connectionSocket.recv(4096), ))

def launch():
	#Add listener
	core.openflow.addListenerByName("FlowStatsReceived", HandleFlowStats)
	#Start listening server on thread 
	#thread.start_new_thread(Server, ( , ))
	printToServer("ThrottleManager started")
	t1 = Thread(target=Server)
	t1.start()
	#Add ping all switches for requests every 1 second
	#This means our "update rate" is 1 second
	Timer(1, SendStatsRequest, recurring=True)