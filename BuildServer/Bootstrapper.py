from mininet.node import (Host, RemoteController, OVSSwitch)
from mininet.net import Mininet
from mininet.cli import CLI
import time, os, sys
sys.path.append("/home/user/Desktop/P5-ReactionProtocol")

from P5-ReactionProtocol.MininetTopologies.topologyFunctions import *

#sequence of things to happen:
	#1: start pox controller, with l2_multi and throttle manager
	#2: start mininet with a topology
	#3: ensure full connectivity in the mininet -> run pingall
	#4: get list of switches from each ISP and put in list
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
#os.system("pypy ./pox.py log.level. --DEBUG forwarding.l2_multi ThrottleManager")

#2
net = AddPoxController()