#import mininet things
from mininet import *

#we are always running with Open vswitch, therefore always do the following when initializing a new mininet:
#Mininet(switch = OVSSwitch)


def SimpleTopology(self):
    net = Mininet(switch = OVSSwitch)

    #add remotecontroller, always the same
    poxcontroller = net.addController(name="pox", controller=RemoteController, ipaddress="127.0.0.1")

    #add hosts
    h1 = net.addHost("h1")
    h2 = net.addHost("h2")

    #add switch
    s1 = net.addSwitch("s1")


    return net

