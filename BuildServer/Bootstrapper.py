import time, os

# This function is odd, since it uses another tool, ovs-vsctl to send queries to each virtual open vSwitch
# that adds another queue to the switch, as well as a custom value for how much throughput for that queue.

'''
Example command

"sudo ovs-vsctl -- set Port s1-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb 
other-config:maxrate=1000000000 queues=0=@q0 -- --id=@q0 create Queue other-config:min-rate=10000000 
other-config:max-rate=1000000000"
'''