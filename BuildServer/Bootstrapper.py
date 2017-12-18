from mininet.node import (Host, RemoteController, OVSSwitch)
from mininet.net import Mininet
from mininet.cli import CLI
import time, os, sys
from threading import Thread
import thread

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

#5
def AssignDelegators(allISPs, participatingISPs):
	def WriteToFile(Delegators):
		try:
			file = open("/home/user/Desktop/delegatorIPs", "w")
			for delegator in Delegators:
				file.write(delegator.mininetHost.IP()+'\n')
			file.close()
		except Exception as e:
			print("Could not write delegator IP to file exception: %s"%(e))

	Delegators = []
	if len(allISPs) < participatingISPs:
        counter = 0
		for ISP in allISPs:
			host = ISP.listOfHosts[randint(0, len(ISP.listOfHosts)-1)]
			while host.HasAssignment:
				host = ISP.listOfHosts[randint(0, len(ISP.listOfHosts)-1)]

			host.HasAssignment = True
			host.mininetHost.cmd("python $HOME/Desktop/P5ReactionProtocol/Delegator/Delegator.py %d"%(counter))
			delegators.append(host)
            counter += 1
	else:
		for i in range(0, len(allISPs)):
			host = allISPs[i].listOfHosts[randint(0, len(allISPs[i].listOfHosts)-1)]
			while host.HasAssignment:
				host = allISPs[i].listOfHosts[randint(0, len(allISPs[i].listOfHosts)-1)]

			host.HasAssignment = True
			host.mininetHost.cmd("python $HOME/Desktop/P5ReactionProtocol/Delegator/Delegator.py %d"%(i))
			Delegators.append(host)
	WriteToFile(Delegators)
#6
def Assign(listOfHosts, numberOfVictims, programPath):
	victims = []
	for i in range(0, numberOfVictims):
		host = listOfHosts[randint(0, len(listOfHosts)-1)]
		while host.HasAssignment: 							   #becomes infinite loop, if there are no hosts left without an assignment
			host = listOfHosts[randint(0, len(listOfHosts)-1)]   #randomly select another host, until a host is found that has not yet been assigned
		host.HasAssignment = True
		thread.start_new_thread(host.mininetHost.cmd, (programPath, ))
		time.sleep(1)
		victims.append(host)

	return victims 

#Takes IPs from mininet, and puts them into the file, where FNM
#looks for IPs to listen to
def FastNetMonConfigurator(victims):
	try:
		file = open("/etc/networks_list", "w")
		for item in victims:
			file.write(item.mininetHost.IP() + '/32 \n')
		file.close()
	except Exception as e:
		print('FastNetMons networks_list file not found!')

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

print("Assigning victims")
programPath = "sudo python $HOME/Desktop/P5ReactionProtocol/Client/Linker.py"
victims = Assign(GetAllHosts(ISPs), 1, programPath) #assign victims, 1 victim
print("Done")
time.sleep(3)

#fastnetmon 
print("Configuring fastnetmon")
FastNetMonConfigurator(victims)
print("Done")
time.sleep(3)

hosts = GetAllHosts(ISPs)
for host in hosts:
	print("Host IP: %s. Host Has assignment: %d"%(host.mininetHost.IP(), host.HasAssignment))

print("Assigning attackers")
programPath = "sudo python $HOME/Desktop/P5ReactionProtocol/Attacker/Attacker.py"
Assign(GetAllHosts(ISPs), 3, programPath) #assign attackers, 3 attackers
print("Done")
time.sleep(3)

var = raw_input("Speak friend, and enter..")
os.system("sudo mn -c")