from mininet.node import (Host, RemoteController, OVSSwitch)
from mininet.net import Mininet
from mininet.cli import CLI
import time, os, sys
from threading import Thread

#------------------------
from mininet.util import quietRun
from requests import put
from json import dumps
from subprocess import call, check_output
from os import listdir
import re
import socket
#------------------------


sys.path.append("/home/user/Desktop/P5ReactionProtocol")
from MininetTopologies.topologyFunctions import * 


#--------------------SFLOW----------------------------
collector = '127.0.0.1'
sampling = 10
polling = 10

def getIfInfo(ip):
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect((ip, 0))
  ip = s.getsockname()[0]
  ifconfig = check_output(['ifconfig'])
  ifs = re.findall(r'^(\S+).*?inet addr:(\S+).*?', ifconfig, re.S|re.M)
  for entry in ifs:
    if entry[1] == ip:
      return entry

def configSFlow(net,collector,ifname):
  print "*** Enabling sFlow:"
  sflow = 'ovs-vsctl -- --id=@sflow create sflow agent=%s target=%s sampling=%s polling=%s --' % (ifname,collector,sampling,polling)
  for s in net.switches:
    sflow += ' -- set bridge %s sflow=@sflow' % s
  print ' '.join([s.name for s in net.switches])
  quietRun(sflow)

def sendTopology(net,agent,collector):
  print "*** Sending topology"
  topo = {'nodes':{}, 'links':{}}
  for s in net.switches:
    topo['nodes'][s.name] = {'agent':agent, 'ports':{}}
  path = '/sys/devices/virtual/net/'
  for child in listdir(path):
    parts = re.match('(^s[0-9]+)-(.*)', child)
    if parts == None: continue
    ifindex = open(path+child+'/ifindex').read().split('\n',1)[0]
    topo['nodes'][parts.group(1)]['ports'][child] = {'ifindex': ifindex}
  i = 0
  for s1 in net.switches:
    j = 0
    for s2 in net.switches:
      if j > i:
        intfs = s1.connectionsTo(s2)
        for intf in intfs:
          s1ifIdx = topo['nodes'][s1.name]['ports'][intf[0].name]['ifindex']
          s2ifIdx = topo['nodes'][s2.name]['ports'][intf[1].name]['ifindex']
          linkName = '%s-%s' % (s1.name, s2.name)
          topo['links'][linkName] = {'node1': s1.name, 'port1': intf[0].name, 'node2': s2.name, 'port2': intf[1].name}
      j += 1
    i += 1

  put('http://'+collector+':8008/topology/json',data=dumps(topo))

def wrapper(fn,collector):
  def result( *args, **kwargs):
    res = fn( *args, **kwargs)
    net = args[0]
    (ifname, agent) = getIfInfo(collector)
    configSFlow(net,collector,ifname)
    sendTopology(net,agent,collector) 
    return res
  return result
#--------------------SFLOW----------------------------






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
	setattr(Mininet, 'start', wrapper(Mininet.__dict__['start'], collector))

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
	for switch in switches:
		interfaces = switch.intfNames()
		for i in range(1, len(interfaces)):
			InitializeThrottleQueue(interfaces[i])
		#print queues that have just been created
		os.system("sudo ovs-ofctl -O openflow10 queue-stats %s"%(switch.name))

#4.1
def ConfigureSwitchesForSFlow(ISPs):
	switches = GetAllSwitches(ISPs)
	for switch in switches:
		print(switch.name)
		os.system("sudo ovs-vsctl -- --id=@sflow create sflow agent=eth0 target=\"127.0.0.1:6343\" sampling=10 polling=20 -- -- set bridge %s sflow=@sflow"%(switch.name))

#5
def AssignDelegators(allISPs, participatingISPs):
	def WriteToFile(delegators):
		try:
			file_object = open("~/Desktop/delegatorIPs", "w")
			for delegator in delegators:
				file_object.write(delegator.mininetHost.IP()+"\n")
				file_object.close()
		except Exception as e:
			print("Could not write delegator IP to file")

	Delegators = []
	if len(allISPs) < participatingISPs:
		for ISP in allISPs:
			host = ISP.listOfHosts[randint(0, len(ISP.listOfHosts)-1)]
			while host.HasAssignment:
				host = ISP.listOfHosts[randint(0, len(ISP.listOfHosts)-1)]

			host.HasAssignment = True
			host.mininetHost.cmd("python $HOME/Desktop/P5ReactionProtocol/Delegator/Delegator.py")
			delegators.append(host)
	else:
		for i in range(0, len(allISPs)):
			host = allISPs[i].listOfHosts[randint(0, len(allISPs[i].listOfHosts)-1)]
			while host.HasAssignment:
				host = allISPs[i].listOfHosts[randint(0, len(allISPs[i].listOfHosts)-1)]

			host.HasAssignment = True
			host.mininetHost.cmd("python $HOME/Desktop/P5ReactionProtocol/Delegator/Delegator.py")
			Delegators.append(host)

	WriteToFile(Delegators)

	'''		
	def RunDelegatorCode(host):
		host.mininetHost.cmd("sudo python $HOME/Desktop/P5ReactionProtocol/Delegator/Delegator.py")

	if len(allISPs) < participatingISPs:
		for ISP in allISPs:
			host = IPS.listOfHosts[randint(0, len(ISP.listOfHosts))]
			thread1 = Thread(target=RunDelegatorCode, args=(host))
			thread1.start()
		host.mininetHost.cmd("sudo python ~/Desktop/P5ReactionProtocol/Delegator/Delegator.py"))
	d

	delegators = []
	if len(allISPs) < participatingISPs:
		for ISP in allISPs:
			host = IPS.listOfHosts[randint(0, len(ISP.listOfHosts))]
			delegators.append(host)
	else:
		for i in range(0, len(allISPs)):
			host = allISPs[i].listOfHosts[randint(0, len(allISPs[i].listOfHosts))]
			thread1 = Thread(target=RunDelegatorCode, args=(host))
			thread1.start()
	

	for delegator in delegators:
		thread1 = Thread(target=RunDelegatorCode, args=(host))
		thread1.start()
	'''
#6
def Assign(listOfHosts, numberOfHosts, programPath):
	def RunClientCode(host, programPath):
		host.mininetHost.cmd(programPath)
	victims = []
	for i in range(0, numberOfVictims):
		host = listOfHosts[randint(0, len(listOfHosts)-1)]
		while host.HasAssignment: #becomes infinite loop, if there are no hosts left without an assignment
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

print("Configuring switches for SFlow")
ConfigureSwitchesForSFlow(ISPs)
print("Done")
time.sleep(3)

print("Assigning delegators")
AssignDelegators(ISPs, 3)
print("Done")
time.sleep(3)

cli = CLI(net)

var = raw_input("Speak friend, and enter..")
os.system("sudo mn -c")


'''
programPath = "sudo python ~/Desktop/P5ReactionProtocol/Client/Linker.py"
Assign(GetAllHosts(ISPs), 1, programPath) #assign victims

#fastnetmon 
FastNetMonConfigurator()

programPath = "sudo python ~/Desktop/P5ReactionProtocol/hpingsomething.py"
Assign(GetAllHosts(ISPs), 5, programPath) #assign attackers


'''

'''
thread1 = Thread(target=StartController)
thread1.start()

time.sleep(2)

print(switches[0].defaultDpid())
'''
