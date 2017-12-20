from pox.core import core
from pox.lib.recoco import Timer
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr
import thread
import socket
import os

log = core.getLogger("Report: ")

HOST = '192.168.2.4'
PORT = 7777

# This stores a list of all current victim IPs
currentVictims = []

def ConfigurePort(portName, q1Rate):
	os.system("sudo ovs-vsctl -- set Port "+portName+" qos=@newqos -- \
--id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1 -- \
--id=@q0 create Queue other-config:min-rate=1000000000 other-config:max-rate=1000000000 -- \
--id=@q1 create Queue other-config:min-rate="+q1Rate+" other-config:max-rate="+q1Rate)

def SendFlowMod(port, event, src, dst, placeInThrottleQueue):
	log.debug("sending throttle message")
	msg = of.ofp_flow_mod()
	msg.priority = 100
	msg.idle_timeout = 60
	msg.hard_timeout = 60
	msg.match.dl_type = 0x0800
	msg.match.nw_src = src
	msg.match.nw_dst = dst
	if placeInThrottleQueue == True:
		msg.actions.append(of.ofp_action_enqueue(port=port, queue_id=1))
	elif placeInThrottleQueue == False:
		msg.actions.append(of.ofp_action_enqueue(port=port, queue_id=0))
	event.connection.send(msg)

def SendStatsRequest():
	for con in core.openflow.connections:
		con.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))

def HandleFlowStats(event):
	for flows in event.stats:				#should only be a single flow, with a destination of victimIPAddress, however there could also not be one
		for ip in currentVictims:
			if flows.match.nw_dst == ip:	#if destination of a flow matches the IP address of the current victim
				log.debug(flows.actions[0].port)
				port = flows.actions[0].port                 #out_port of packet to destination address of current victim
				
				#install q0 and q1 on this port (on the given switch), and throttle q1
				#this install will timeout/remove itself after a set amount of time
				ConfigurePort(port, 40000)

				#Send openflow command
				SendFlowMod(port, event, flows.match.nw_src, flows.match.nw_dst, True)
		if flows.match.nw_dst not in currentVictims:
			#Place the flow in queue 0 (dont throttle it)
			SendFlowMod(port, event, flows.match.nw_src, flows.match.nw_dst, False)


def HandleSignal(data):
	# Signal format <PANIC or STOP> / <victimIP> / <DELEGATOR or CLIENT>
	# ...last of which we don't care about here
	signalType, IP, doesntMatter = data.split('/')
	if signalType == 'PANIC':
		# Add to 'current victims' list
		currentVictims.append(IP)
	elif signalType == 'STOP':
		# Remove from list of current victims
		filter(lambda item: item != IP, currentVictims)

#Will listen for messages from delegators, runs in a thread so it doesnt block the program 
def Server():
	#Server
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
	thread.start_new_thread(server, ( , ))
	#Add ping all switches for requests every 1 second
	#This means our "update rate" is 1 second
	Timer(1, SendStatsRequest, recurring=True)