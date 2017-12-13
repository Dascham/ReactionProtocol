from mininet.node import ( Host, CPULimitedHost, Controller, OVSController,
                           Ryu, NOX, RemoteController, findController,
                           DefaultController, NullController,
                           UserSwitch, OVSSwitch, OVSBridge,
                           IVSSwitch )
from mininet.net import Mininet
from mininet.cli import CLI

net = Mininet(switch=OVSSwitch, setAutoMacs=True)
net.addController(name="pox", controller=RemoteController, 
				ip="127.0.0.1", protocol="tcp", port=6633)
