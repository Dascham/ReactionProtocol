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
'''
def StartController():
	def StartInThread():
		pypy = "~/Desktop/poxDart/pox/pypy/bin/pypy"
		gephiData = "misc.gephi_topo"

		os.system("%s ~/Desktop/poxDart/pox/pox.py log.level --DEBUG forwarding.l2_multi openflow.discovery PoxModule.ThrottleManager" %(pypy))
		#PoxModule.ThrottleManager
	thread1 = Thread(target=StartInThread, args=())
	thread1.start()
'''

#2
def InitializeTopology(net):
	ISPs = []
	for i in range(0, 3):
		isp = ISP(net, 3, 2, 2)
		ISPs.append(isp)

	for i in range(0, len(ISPs)):
		if len(ISPs) != i+1:
			ConnectTwoISPs(net, ISPs[i], ISPs[i+1])
		#else:
			#ConnectTwoISPs(net, ISPs[0], ISPs[-1]) #connect last with first -> probably adds cycle to network

	net.build()
	nodes = net.values()
	print(nodes)

	net.addNAT().configDefault()
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
def InstallQueues(ISPs):
	switches = GetAllSwitches(ISPs)
	counter = 1
	for switch in switches:
		interfaces = switch.intfNames()
		for i in range(1, len(interfaces)):
			InitializeThrottleQueue(interfaces[i])
		#print queues that have just been created
		os.system("sudo ovs-ofctl -O openflow10 queue-stats s%d"%(counter))
		counter += 1
#5
def AssignDelegators(allISPs, participatingISPs):
	if len(allISPs) < participatingISPs:
		for ISP in allISPs:
			host = IPS.listOfHosts[randint(0, len(ISP.listOfHosts))]
			host.mininetHost.cmd("python $HOME/Desktop/P5ReactionProtocol/Delegator/Delegator.py")
	else:
		for i in range(0, len(allISPs)):
			host = allISPs[i].listOfHosts[randint(0, len(allISPs[i].listOfHosts))]
			host.mininetHost.cmd("python $HOME/Desktop/P5ReactionProtocol/Delegator/Delegator.py")
	'''
	def RunDelegatorCode(host):
		host.mininetHost.cmd("sudo python $HOME/Desktop/P5ReactionProtocol/Delegator/Delegator.py")

	if len(allISPs) < participatingISPs:
		for ISP in allISPs:
			host = IPS.listOfHosts[randint(0, len(ISP.listOfHosts))]
			thread1 = Thread(target=RunDelegatorCode, args=(host))
			thread1.start()
		host.mininetHost.cmd("sudo python ~/Desktop/P5ReactionProtocol/Delegator/Delegator.py"))
	def WriteToFile(delegators):
		try:
			file_object = open("~/Desktop/delegatorIPs", "w")
				for delegator in delegators
					file_object.write(delegator.mininetHost.IP()+"\n")
				file_object.close()
		except: Exception as e:
			print("Could not write delegator IP to file")

	delegators = []
	if len(allISPs) < participatingISPs:
		for ISP in allISPs:
			ḧost = IPS.listOfHosts[randint(0, len(ISP.listOfHosts))]
			delegators.append(host)
	else:
		for i in range(0, len(allISPs)):
			host = allISPs[i].listOfHosts[randint(0, len(allISPs[i].listOfHosts))]
			thread1 = Thread(target=RunDelegatorCode, args=(host))
			thread1.start()
	'''
			delegators.append(host)
	WriteToFile(delegators)

	for delegator in delegators:
		thread1 = Thread(target=RunDelegatorCode, args=(host))
		thread1.start()
#6
def Assign(listOfHosts, numberOfHosts, programPath):
	def RunClientCode(host, programPath):
		host.mininetHost.cmd(programPath)
	victims = []
	for i in range(0, numberOfVictims):
		host = listOfHosts[randint(0, len(listOfHosts)-1)]
		while host.HasAssignment == True: #becomes infinite loop, if there are no hosts left without an assignment
			host = listOfHosts[randint(0, len(listOfHosts)-1)] #randomly select another host, until a host is found that has not yet been assigned
		host.HasAssignment = True
		victims.append(host)
		thread1 = Thread(target=RunClientCode, args=(host, programPath))
		thread1.start()
	return victims 

#Takes IPs from mininet, and puts them into the file, where FNM
#looks for IPs to listen to
def FastNetMonConfigurator(iplist):
	try:
		file = open("/etc/networks_list", "w")
		for item in iplist:
			file.write(item + '/32 \n')
		file.close()
	except Exception as e:
		print('FastNetMons networks_list file not found!')

'''
def StartForwarder():
	def StartInThread():
		os.system("sudo python ~/Desktop/P5ReactionProtocol/Client/Forwarder.py")
	thread1 = Thread(target=StartInThread, args=())
	thread1.start()
'''
print("Adding controller")
net = AddPoxController()
print("Done")
time.sleep(3)

print("Initiating mininet")
ISPs = InitializeTopology(net) #currently with a NAT device
print("Done")
time.sleep(3)

print("Ping test")
TestConnectivity(net)
print("Done")
time.sleep(3)

print("Installing queues")
InstallQueues(ISPs)
print("Done")
time.sleep(3)

print("Assigning delegators")
AssignDelegators(ISPs, 3)
print("Done")
time.sleep(3)

var = raw_input("Speak friend, and enter..")
os.system("sudo mn -c")


'''
programPath = "sudo python ~/Desktop/P5ReactionProtocol/Client/Linker.py"
Assign(GetAllHosts(ISPs), 1, programPath) #assign victims

programPath = "sudo python ~/Desktop/P5ReactionProtocol/hpingsomething.py"
Assign(GetAllHosts(ISPs), 5, programPath) #assign attackers

FastNetMonConfigurator()
'''

'''
thread1 = Thread(target=StartController)
thread1.start()

time.sleep(2)

print(switches[0].defaultDpid())
'''
