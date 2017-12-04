import time, os

#could also have parameter about queue size
def InitializeThrottledQueues(minBitsPerSecond, maxBitsPerSecond):
    #This function is odd, since it uses another tool, ovs-vsctl to send queries to each virtual open vSwitch
    #that adds another queue to the switch, as well as a custom value for how much throughput for that queue.
    Port = "s1-eth1"

    os.system("sudo ovs-vsctl -- set Port %s qos=@newqos -- "
              "--id=@newqos create QoS type=linux-htb other-config:maxrate=1000000000 queues=0=@q0 --"
              " --id=@q0 create Queue other-config:min-rate=%s other-config:max-rate=%s ",
              Port, minBitsPerSecond, maxBitsPerSecond)