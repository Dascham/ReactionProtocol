import os, time, socket
from pox.core import core
from pox.lib.util import dpid_to_str
from threading import Thread


'''
the actual component that will be used with pox
./pox.py [some pox component, for example l2_learning] [this component]
'''

class ThrottleManager(object):

    def SendFlowMod(clientIPAddress, port, switch, priority=100, expires=600, queue_id=0):
        global globalEvent
        log.debug("sending throttle message")
        msg = of.ofp_flow_mod()
        msg.priority = priority
        msg.idle_timeout = expires #remove flow after amount of time specified, if no packets have been matched
        msg.hard_timeout = expires #no matter what, remove flow after amount of time
        msg.match.dl_type = 0x0800
        msg.match.nw_dst = clientIPAddress
        msg.actions.append(of.ofp_action_enqueue(port=port, queue_id=queue_id)) #port 2 = eth2
        switch.connection.send(msg)

    def DeleteFlowMod(self):
        var = 0

    def ListenForDelegatorMessage(self):
        self.socket.bind(("", self.port))
        self.socket.listen(1)

        while 1:
            connectionSocket, addr = self.socket.accept()



    def GetPortThroughIpAdress(self, ipAddress, switch):
        port = 0

        return port
    def AskNeighbouringSwitches(self):



    def __init__(self):
        self.allConnectionObjects = core.connections()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 5001

        #start thread immediatly
        thread1=Thread(target=self.ListenForDelegatorMessage)
        thread1.start()

    def launch(self):
        core.registerNew(ThrottleManager)


    #function that invokes the ovs-vsctl tool
    def InitializeThrottleQueue(switch, switchInterface, minBitsPerSecond=0, maxBitsPerSecond=1000000,
                                queueSize=1000, queue_id=0):

        os.system("sudo ovs-vsctl -- set Port {0}-{1} qos=@newqos -- "
              "--id=@newqos create QoS type=linux-htb other-config:maxrate={3} queues={4}=@q{4} --"
              "--id=@q{4} create Queue other-config:min-rate={2} other-config:max-rate={3}"
            .format(switch, switchInterface, minBitsPerSecond, maxBitsPerSecond, queue_id))