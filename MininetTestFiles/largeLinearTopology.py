from mininet.net import Mininet
from mininet.topo import LinearTopo
from mininet.node import OVSSwitch, RemoteController, Host, CPULimitedHost
from threading import Thread
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.clean import Cleanup
import os, time
from mininet.util import quietRun

#autoSetMacs=True

#linear = LinearTopo(k=4)
#topo=linear,
#
net = Mininet(switch = OVSSwitch, autoSetMacs=True)

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


#Prints exactly: OVSSwitch s1: lo:127.0.0.1,s1-eth1:None
#print("Hello"+s1.defaultDpid) 



#print exactly the DPID (00000000000000001) something along those lines
print(s1.defaultDpid())



print(h1.IP()) #prints exactly "10.0.0.1"


collector = '127.0.0.1'
sampling = 10
polling = 10

#quietRun("ovs-vsctl -- --id=@sflow create sflow agent=eth0 target=127.0.0.1 sampling=10 polling=20 -- -- set bridge s1 sflow=@sflow")

cli = CLI(net)





time.sleep(2)

net.stop()

os.system("sudo mn -c")
