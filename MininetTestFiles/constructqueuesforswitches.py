import os, time

os.system("sudo ovs-vsctl -- set Port s1-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:maxrate=1000000000 queues=0=@q0 -- --id=@q0 create Queue other-config:min-rate=10000000 other-config:max-rate=1000000000")

os.system("sudo ovs-vsctl -- set Port s1-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:maxrate=1000000 queues=1=@q1 -- --id=@q1 create Queue other-config:min-rate=100000 other-config:max-rate=1000000 ")

os.system("sudo ovs-ofctl -O Openflow13 queue-stats s1")