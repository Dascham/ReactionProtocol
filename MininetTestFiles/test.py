from mininet.net import Mininet
from mininet.topo import LinearTopo
from threading import Thread
import os, time

linear = LinearTopo(k=4)
net = Mininet(topo=linear)
net.start()
def Server():
	h1 = net.get("h1")
	result = h1.cmd("sudo python /etc/pythonprograms/pythonServer.py")
	print(result)
def Client():
	h2 = net.get("h2")
	h2.cmd("sudo python /etc/pythonprograms/pythonClient.py")
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
time.sleep(10)
net.stop()
#always do cleanup of mininet
os.system("sudo mn -c")