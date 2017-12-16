from mininet.net import Mininet
from mininet.topo import LinearTopo
from mininet.node import OVSSwitch, RemoteController, Host, CPULimitedHost
from threading import Thread
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.clean import Cleanup
import os, time

#autoSetMacs=True

#linear = LinearTopo(k=4)
#topo=linear,
#autoSetMacs=False
net = Mininet(switch = OVSSwitch)

poxcontroller = net.addController(name="pox", 
                controller=RemoteController, 
                ip="127.0.0.1", protocol="tcp", 
                port=6633)

h1 = net.addHost("h1")
h2 = net.addHost("h2")
s1 = net.addSwitch("s1")

net.addLink(h1, s1)
net.addLink(h2, s1)

net.start()

print(s1.defaultDpid())

cli = CLI(net)

time.sleep(2)

net.stop()

os.system("sudo mn -c")
