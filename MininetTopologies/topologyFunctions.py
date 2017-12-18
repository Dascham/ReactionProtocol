from mininet.node import ( Host, CPULimitedHost, Controller, OVSController,
                           Ryu, NOX, RemoteController, findController,
                           DefaultController, NullController,
                           UserSwitch, OVSSwitch, OVSBridge,
                           IVSSwitch )
from mininet.net import Mininet
from mininet.cli import CLI
import os, time
from random import randint

hostCounter = 1
switchCounter = 1

class Host():
	def __init__(self, mininetHost):
		self.mininetHost = mininetHost
		self.HasAssignment = False

class GatewaySwitch():
	def __init__(self, mininetSwitch):
		self.mininetSwitch = mininetSwitch
		self.IsConnectedToGateway = False

class ISP:
	#static variable for unique ID assignment
	static_id = 0

	def __init__(self, net, numberOfHosts, numberOfSwitches, numberOfGateways):
		self.net = net
		self.listOfHosts = self.AddHosts(self.net, numberOfHosts)
		self.listOfSwitches = self.AddSwitches(self.net, numberOfSwitches, True)
		self.listOfGateways = self.AddSwitches(self.net, numberOfGateways, False)
		self.HasDelegator = False
		self.id = ISP.static_id
		ISP.static_id += 1

		if self.listOfHosts and self.listOfSwitches: #if both lists are not empty
			self.ConnectISPDevices(self.net, self.listOfHosts, self.listOfSwitches)
		if self.listOfSwitches and self.listOfGateways:
			self.ConnectSwitchesAndGateways(self.net, self.listOfSwitches, self.listOfGateways)

		#write all DPIDs to a file
		WriteToFile()

	def ConnectISPDevices(self, net, listOfHosts, listOfSwitches):
		number = len(listOfHosts)/len(listOfSwitches)
		remainder = len(listOfHosts)%len(listOfSwitches) 
		j = 0
		if number != 0:
			for i in range(0, len(listOfSwitches)):
				while j < len(listOfHosts): 
					net.addLink(listOfSwitches[i], listOfHosts[j].mininetHost)
					j = j+1
					if j % number == 0: 
						break

		if remainder != 0: #if number of hosts is uneven with amount of switches
			for i in range(1, remainder+1):
				net.addLink(listOfHosts[-i].mininetHost, listOfSwitches[-i]) #link last host with last switch
		
		if len(listOfSwitches) > 1:
			for i in range (0, len(listOfSwitches)):
				if len(listOfSwitches) != i+1:
					net.addLink(listOfSwitches[i], listOfSwitches[i+1])
				else:
					break

	def ConnectSwitchesAndGateways(self, net, listOfSwitches, listOfGateways):
		if len(listOfSwitches) > len(listOfGateways):
			for i in range(0, len(listOfGateways)):
				net.addLink(listOfSwitches[i], listOfGateways[i].mininetSwitch)
		else:
			for i in range(0, len(listOfSwitches)):
				net.addLink(listOfSwitches[i], listOfGateways[i].mininetSwitch)

	def AddHosts(self, net, numberOfHosts):
		global hostCounter
		hosts = []
		for i in range(0, numberOfHosts):
			host = Host(net.addHost("h%d"% (hostCounter)))
			hostCounter += 1
			hosts.append(host)
		return hosts

	def AddSwitches(self, net, numberOfSwitches, IsSwitch):
		global switchCounter
		switches = []
		if IsSwitch:
			for i in range(0, numberOfSwitches):
				switch = net.addSwitch("s%d"% (switchCounter))
				switchCounter += 1
				switches.append(switch)
			return switches
		else: 
			for i in range(0, numberOfSwitches):
				switch = GatewaySwitch(net.addSwitch("s%d"% (switchCounter)))
				switchCounter += 1
				switches.append(switch)
			return switches

def ConnectTwoISPs(net, isp_a, isp_b):
	for i in range(0, len(isp_a.listOfGateways)):
		for j in range(0, len(isp_b.listOfGateways)):
			if isp_a.listOfGateways[i].IsConnectedToGateway == False and isp_b.listOfGateways[j].IsConnectedToGateway == False:
				net.addLink(isp_a.listOfGateways[i].mininetSwitch, isp_b.listOfGateways[j].mininetSwitch)
				isp_a.listOfGateways[i].IsConnectedToGateway = True
				isp_b.listOfGateways[j].IsConnectedToGateway = True
				return True
	return False

def AddPoxController():
	net = Mininet(switch=OVSSwitch, autoSetMacs=True)
	net.addController(name="pox", controller=RemoteController, 
				ip="127.0.0.1", protocol="tcp", port=6633)
	return net

def GetAllSwitches(allISPs):
	switches = []
	for ISP in allISPs:
		switches.extend(ISP.listOfSwitches)
		for i in range(0, len(ISP.listOfGateways)):
			switches.append(ISP.listOfGateways[i].mininetSwitch)
	return switches

def GetAllHosts(allISPs):
	hosts = []
	for ISP in allISPs:
		hosts.extend(ISP.listOfHosts)
	return hosts

def WriteToFile(switches, gateways):
	try:
		f = open("/home/user/Desktop/isp%d"%(self.id), "w")
		for switch in switches:
			f.write(switch.defaultDpid()+'\n')
		for i in range(0, len(gateways))
			gateways[i].mininetSwitch
	f.close()
	except Exception as e:
		print("Could not write DPIDs to file: %s "%(e))


def InitializeThrottleQueue(switchInterface, minBitsPerSecond=0, 
	maxBitsPerSecond=1000000, queueSize=1000, queue_id=0):

	os.system("sudo ovs-vsctl -- set Port {0} qos=@newqos -- "
		"--id=@newqos create QoS type=linux-htb other-config:maxrate={2} queues={3}=@q{3} -- "
		"--id=@q{3} create Queue other-config:min-rate={1} other-config:max-rate={2}"
		.format(switchInterface, minBitsPerSecond, maxBitsPerSecond, queue_id))


'''
net = AddPoxController()
ISPs = []
for i in range(0, 1):
	isp = ISP(net, 2, 1, 0)
	ISPs.append(isp)

for i in range(0, len(ISPs)):
	if len(ISPs) != i+1:
		ConnectTwoISPs(net, ISPs[i], ISPs[i+1])
	else:
		ConnectTwoISPs(net, ISPs[0], ISPs[-1]) #connect last with first -> probably adds cycle to network

#has to build before able to get values
print("Hostcounter %d. Switchcounter %d" % (hostCounter, switchCounter))

net.build()
#nodes = net.values()
#print(nodes)
net.start()

#this works as expected
switches = GetAllSwitches(ISPs)
print(switches[0].defaultDpid())
print(ISPs[0].listOfHosts.mininetHost[0].IP())
print(switches[0].intfNames()) #for a switch with two interfaces, returns: ["lo", "s1-eth1", "s1-eth2"]


cli = CLI(net)


net.stop()
time.sleep(3)
os.system("sudo mn -c")
'''