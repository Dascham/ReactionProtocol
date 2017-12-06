from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController, Host
from mininet.cli import CLI
import os, time

net = Mininet(switch = OVSSwitch)
try:
	poxcontroller = net.addController(name="pox", controller=RemoteController, 
				ip="127.0.0.1", protocol="tcp", port=6633)
	h1 = net.addHost("h1")
	h2 = net.addHost("h2")
	s1 = net.addSwitch("s1")
	
	net.addLink(h1, s1) #s1_eth1
	net.addLink(s1, h2) #s1_eth2
	net.start()
	#wait until all switches have connected to the controller	
	net.waitConnected()

	#bandwidth testing, 100M == 100megabit. Connection: host1 to host2
	listOfHosts = [h1, h2]
	net.iperf(listOfHosts, l4Type="UDP", udpBw="100M", seconds=5) 
	#Testing the opposite connection: host2 to host1
	listOfHosts.reverse()
	net.iperf(listOfHosts, l4Type="UDP", udpBw="100M", seconds=5)

	#Doing another test between h1 and h2
	listOfHosts.reverse()
	net.iperf(listOfHosts, l4Type="UDP", udpBw="100M", seconds=5)

	net.stop()
	os.system("sudo mn -c") #build-in mininet command that cleans up after stopping the net
except Exception, e:
	print("Caught exception %s", e)
	os.system("sudo mn -c")