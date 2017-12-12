from mininet.net import Mininet
from mininet.topo import LinearTopo
from threading import Thread
from mininet.node import OVSSwitch, RemoteController
from mininet.cli import CLI
import os, time
#this file can be run from the terminal by using: "sudo python test.py"

linear = LinearTopo(k=2)
net = Mininet(topo=linear, switch=OVSSwitch, autoSetMacs=True)
poxcontroller = net.addController(name="pox", 
				controller=RemoteController, 
				ip="127.0.0.1", protocol="tcp", 
				port=6633)
net.start()

def Server():
	h1 = net.get("h1")
	result = h1.cmd("sudo python /etc/pythonprograms/pythonServer.py")
	print(result)
def Client():
	h2 = net.get("h2")
	result = h2.cmd("sudo python /etc/pythonprograms/pythonClient.py")
	print(result)
try:
	thread1 = Thread(target=Server)
	thread2 = Thread(target=Client)
	print("starting thread 1")
	thread1.start()
	time.sleep(5)
	print("starting thread 2")
	thread2.start()	
except:
	print("could not start threads")
#let client and server run for a bit
time.sleep(3)
var = raw_input("Do thing")
cli = CLI(net)
net.stop()

#always do cleanup of mininet, easy
os.system("sudo mn -c")