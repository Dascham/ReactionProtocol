from mininet.node import (Host, RemoteController, OVSSwitch)
from mininet.net import Mininet
from mininet.cli import CLI
import time, os, sys
from threading import Thread

sys.path.append("/home/user/Desktop/P5ReactionProtocol")
from MininetTopologies.topologyFunctions import * 

#sequence of things to happen:
	#1: start pox controller, with l2_multi and throttle manager 			Done
	#2: start mininet with a topology 										Done
	#3: ensure full connectivity in the mininet -> run pingall 				Done
	#4: install queues in all switches and gateway switches 				Done
	#5: Assign delegators (runs delegator code) 							Done
	#6: Assign victim(s) (runs client code "Linker")						Done
	#7: select victim buddy (runs client code "Linker")						Skip 
	#8: Initiate IDS fastnetmon to start monitoring future victim 			Frederik Do
	#9: Start forwarder 													Done				
	#10: Assign Attackers													Done

	#11: Perform test of reaction protocol, by having attackers run Hping_3

#1
def StartController():
	def StartInThread():
		pypy = "~/Desktop/poxDart/pox/pypy/bin/pypy"
		gephiData = "misc.gephi_topo"

		os.system("%s ~/Desktop/poxDart/pox/pox.py log.level --DEBUG forwarding.l2_multi openflow.discovery PoxModule.ThrottleManager" %(pypy))
		#PoxModule.ThrottleManager
	thread1 = Thread(target=StartInThread, args=())
	thread1.start()

def InitializeTopology(net):
	ISPs = []
	for i in range(0, 4):
		isp = ISP(net, randint(4,10), 2, 2)
		ISPs.append(isp)

	for i in range(0, len(ISPs)):
		if len(ISPs) != i+1:
			ConnectTwoISPs(net, ISPs[i], ISPs[i+1])
		else:
			ConnectTwoISPs(net, ISPs[0], ISPs[-1]) #connect last with first -> probably adds cycle to network

	net.build()
	nodes = net.values()
	print(nodes)
	net.start()

	return ISPs
#3
def TestConnectivity(net):
	print("-------------------")
	result = net.pingAll()
	#if result[:10] != "0% dropped"
	#means there is not full connectivity
	print(result)

#4
def InstallQueues(ISPs)
	switches = GetAllSwitches(ISPs)
	for switch in switches:
		interfaces = switch.defaultDpid()
			for i in range(1, len(interfaces))
				InitializeThrottleQueue(interfaces[i])
#5
def AssignDelegators(allISPs, participatingISPs):
	def RunDelegatorCode(host):
		host.mininetHost.cmd("sudo python ~/Desktop/P5ReactionProtocol/Delegator/Delegator.py")

	if len(allISPs) < participatingISPs:
		for ISP in allISPs:
			ḧost = IPS.listOfHosts[randint(0, len(ISP.listOfHosts))]
			thread1 = Thread(target=RunDelegatorCode, args=(host))
			thread1.start()
	else:
		for i in range(0, len(allISPs))
			host = allISPs[i].listOfHosts[randint(0, len(allISPs[i].listOfHosts))]
			thread1 = Thread(target=RunDelegatorCode, args=(host))
			thread1.start()

#6
def Assign(listOfHosts, numberOfHosts, programPath):
	def RunClientCode(host, programPath):
		host.mininetHost.cmd(programPath)

	victims = []
	for i in range(0, numberOfVictims)
		host = listOfHosts[randint(0, len(listOfHosts)-1)]
		while host.HasAssignment == True #becomes infinite loop, if there are no hosts left without an assignment
			host = listOfHosts[randint(0, len(listOfHosts)-1)] #randomly select another host, until a host is found that has not yet been assigned
		host.HasAssignment = True
		victims.append(host)
		thread1 = Thread(target=RunClientCode, args=(host, programPath))
		thread1.start()
	return victims 

#7
#skip for now

#8
#skip for now

#9
def StartForwarder():
	def StartInThread():
		os.system("sudo python ~/Desktop/P5ReactionProtocol/Client/Forwarder.py")
	thread1 = Thread(target=StartInThread, args=())
	thread1.start()
#10
def AssignAttackers(listOfHosts, numberOfAttackers):

StartController()
net = AddPoxController()
ISPs = InitializeTopology(net) #currently without a NAT device
TestConnectivity(net)
InstallQueues(ISPs)
AssignDelegators(ISPs, 3)
programPath = "sudo python ~/Desktop/P5ReactionProtocol/Client/Linker.py"
Assign(GetAllHosts(ISPs), 1, programPath) #assign victims

StartForwarder()
programPath = "sudo python ~/Desktop/P5ReactionProtocol/hpingsomething.py"
Assign(GetAllHosts(ISPs), 5, programPath) #assign attackers

'''
thread1 = Thread(target=StartController)
thread1.start()

time.sleep(2)

print(switches[0].defaultDpid())
'''