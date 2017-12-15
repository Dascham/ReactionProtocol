from mininet.node import (Host, RemoteController, OVSSwitch)
from mininet.net import Mininet
from mininet.cli import CLI
import time, os, sys
from threading import Thread

sys.path.append("/home/user/Desktop/P5ReactionProtocol")
from MininetTopologies.topologyFunctions import * 

def InitializeThrottleQueue(switchName, switchInterface, minBitsPerSecond=0, maxBitsPerSecond=1000000,
                                queueSize=1000, queue_id=0):

        os.system("sudo ovs-vsctl -- set Port {0}-{1} qos=@newqos -- "
              "--id=@newqos create QoS type=linux-htb other-config:maxrate={3} queues={4}=@q{4} --"
              "--id=@q{4} create Queue other-config:min-rate={2} other-config:max-rate={3}"
            .format(switchName, switchInterface, minBitsPerSecond, maxBitsPerSecond, queue_id))
#sequence of things to happen:
	#1: start pox controller, with l2_multi and throttle manager
	#2: start mininet with a topology
	#3: ensure full connectivity in the mininet -> run pingall
	#4: get list of all switches from each ISP and put in list
	#5: install queues in all switches
	#6: select victim (runs nothing)
	#7: select victim buddy (runs client code)
	#8: select delegators (runs delegator code)
		#have them run the delegator code
	#9: Initiate IDS fastnetmon to start monitoring future victim
	#10: Start forwarder
	#11: randomly select attackers

	#12: Perform test of reaction protocol, by having attackers run Hping_3
#1
def StartController():
	pypy = "~/Desktop/poxDart/pox/pypy/bin/pypy"
	gephiData = "misc.gephi_topo"
	os.system("%s ~/Desktop/poxDart/pox/pox.py log.level --DEBUG forwarding.l2_multi openflow.discovery PoxModule.ThrottleManager" %(pypy))#PoxModule.ThrottleManager

thread1 = Thread(target=StartController)
thread1.start()

time.sleep(2)

#2
net = AddPoxController()
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

#3
print("-------------------")
result = net.pingAll()
#if result[:10] != "0% dropped"
#means there is not full connectivity
print(result)

#4
switches = GetAllSwitches(ISPs)

#
print(switches[0].defaultDpid)