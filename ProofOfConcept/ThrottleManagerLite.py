'''
This is a POX module, acting as a ThrottleManager.
Along with this module, will need to be run a typical controller
module, implementing switch behavior (like a learning switch).

This module will launch a TCP server, which listens for messages from
delegators. When messages are received, 
'''

from pox.core import core
from pox.lib.recoco import Timer
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr
import thread
from threading import Thread
import socket
import os

# Hosting details for the ThrottleManager listening server
HOST = '192.168.2.4'
PORT = 7777

# Connection details for the Print Server
printerIP = '192.168.2.4'
printerPORT = 8888

# List of all current victims, who should be throttled
currentVictims = []

# For ease of use, we print output to a remote Print Server
def printToServer(string):
	try:
		printer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		printer.connect((printerIP, printerPORT))
		printer.send(string)
		printer.close()
	except Exception as e:
		print 'Could not send to Print Server! ' + str(e)

# This function constructs and sends a FlowMod message to a switch.
# This is what will control if flows go through queue 0 (default, non-throttled)
# or through queue 1 (throttled)
def SendFlowMod(port, event, src, dst, placeInThrottleQueue):
	msg = of.ofp_flow_mod()			# msg is a flow modification (openflow)
	msg.priority = 100
	msg.idle_timeout = 0			# Timeout the flow rule, if no traffic is happening during x seconds
	msg.hard_timeout = 0			# Timeout the flow rule after X seconds
	msg.match.dl_type = 0x0800 		# ipv4 traffic code - the rule will only affect ipv4
	msg.match.nw_src = src 			# Source IP
	msg.match.nw_dst = dst 			# Destination IP
	if placeInThrottleQueue == True:
		# Place in the throttled queue
		msg.actions = [of.ofp_action_enqueue(port=port, queue_id=1)]
	elif placeInThrottleQueue == False:
		# Place in the non-throttled queue
		msg.actions.append(of.ofp_action_enqueue(port=port, queue_id=0))
	# Send message to the switch, responsible for the flow
	event.connection.send(msg)

# Request stats from all switches
def SendStatsRequest():
	for con in core.openflow.connections:
		con.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))

# This function, for each flow in the event-object, checks if it
# should be throttled or not, based on whether it exists in
# the 'currentVictim' list
def HandleFlowStats(event):
	for flows in event.stats:
		port = flows.actions[0].port
		for ip in currentVictims:
			if flows.match.nw_dst == ip:
				SendFlowMod(port, event, flows.match.nw_src, flows.match.nw_dst, True)
		if flows.match.nw_dst not in currentVictims:
			SendFlowMod(port, event, flows.match.nw_src, flows.match.nw_dst, False)

# This function handles the management of the 'currentVictim' list,
# adding and removing entries in the list, depending on received data
def HandleSignal(data):
	# Signal format: <START or STOP> / <victimIP>
	printToServer("ThrottleManager recieved signal: " + data)
	signalType, IP = data.split('/')
	if signalType == 'START':
		# Add to 'current victims' list
		currentVictims.append(IP)
		printToServer("ThrottleManager added to the currenctVictims list: " + IP)
	elif signalType == 'STOP':
		# Remove from list of current victims
		for victim in currentVictims:
			if victim == IP:
				currentVictims.remove(victim)
				printToServer("ThrottleManager removed from current victims list: " + IP)

# Will listen for messages from delegators.
# Runs in a thread so it doesnt block the program 
def Server():
	printToServer("ThrottleManager server has started.")
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
	serversocket.bind((HOST, PORT))
	serversocket.listen(5)
	printToServer("ThrottleManager server listening on: " + HOST + ' : ' + str(PORT))

	# When a connection from a delegator is establised, dispatch a thread
	# to handle its data
	while 1:
		connectionSocket, addr = serversocket.accept()
		thread.start_new_thread(HandleSignal, (connectionSocket.recv(4096), ))

# The launch function is where the ThrottleManager module starts its execution
def launch():
	# Add an event listener
	# The function 'HandleFlowStats' will be called, with an 'event' as
	# an argument, when the event 'FlowStatsReceived' is triggered.
	core.openflow.addListenerByName("FlowStatsReceived", HandleFlowStats)
	
	# Start listening server on thread
	printToServer("ThrottleManager started.")
	serv = Thread(target=Server)
	serv.start()

	# Request stats from switches every second
	# This means our "update rate" is 1 second
	Timer(1, SendStatsRequest, recurring=True)