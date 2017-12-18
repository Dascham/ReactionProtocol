import os, time, socket
from pox.core import core
from pox.lib.util import dpid_to_str
from threading import Thread

'''
the actual component that will be used with pox
./pox.py [some pox component, for example l2_learning] [this component]
'''

class ThrottleManager(object):
    def __init__(self):
        core.openflow.addListeners(self)
        #core.openflow.addListenerByName()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 5001
        self.clientIPAddress = None
        self.start = False
        self.stop = False
        self.TTL = None
        self.log = core.getLogger("Report: ")

        #start thread immediatly
        thread1=Thread(target=self.ListenForDelegatorMessage)
        thread1.start()

    def ListenForDelegatorMessage(self):
        self.socket.bind(("", self.port))
        self.socket.listen(1)

        while 1:
            connectionSocket, addr = self.socket.accept() #also a blocking function
            thread2=Thread(target=self.HandleDelegatorRequest, args=(connectionSocket))
            thread2.start()

    def HandleDelegatorRequest(self, connectionSocket):
        msg = connectionSocket.recv(1024)
        msg.decode("ascii")
        # incoming message looks like: <ip> / <request type>

        if msg.count('/') == 1:
            self.clientIPAddress, requestType = msg.split('/')
        elif msg.count('/') == 2:
            self.clientIPAddress, requestType, self.TTL = msg.split('/')

        #Determine if this message is a start- or stop-request
        if requestType is 'START':
            self.start = True
        elif requestType is 'STOP':
            self.stop = True

        sendFlowStatsRequest()  #sends request to all switches

    def sendFlowStatsRequest():
        for con in core.openflow.connections:
            con.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))

    def HandleFlowStats(event, clientIPAddress):
        for flows in event.stats:                            #should only be a single flow, with a destination of victimIPAddress, however there could also not be one
            if flows.match.nw_dst == victimIPAddress:        #if destination of a flow matches the IP address of the current victim
                port = flows.actions[0].port                 #out_port of packet to destination address of current victim
                SendFlowMod(self.clientIPAddress, event)

    def SendFlowMod(clientIPAddress, port, switchConnectionObject, priority=100, expires=600, queue_id=0):
        log.debug("sending throttle message")
        msg = of.ofp_flow_mod()
        msg.priority = priority
        msg.idle_timeout = expires #remove flow after amount of time specified, if no packets have been matched
        msg.hard_timeout = expires #no matter what, remove flow after amount of time
        msg.match.dl_type = 0x0800
        msg.match.nw_dst = clientIPAddress
        msg.match.tp_dst = 22
        msg.actions.append(of.ofp_action_enqueue(port=port, queue_id=queue_id)) #port 2 = eth2
        switchConnectionObject.connection.send(msg)

    def _handle_ConnectionUp(self, event):
        self.log.debug("Am here")
        print(event.dpid) #prints: 1
        print(dpid_to_str(event.dpid))#prints: 00-00-...01 
        #core.openflow.sendToDpid(dpid, msg)
        
    def DeleteFlowMod(self):
        var = 0

def launch():
    throttleManager = ThrottleManager()
    core.register(throttleManager)
    #core.openflow.addListenerByName("FlowStatsReceived", HandleFlowStats)
    #core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)

    #function that invokes the ovs-vsctl tool

def InitializeThrottleQueue(switch, switchInterface, minBitsPerSecond=0, maxBitsPerSecond=1000000,
                                queueSize=1000, queue_id=0):

    os.system("sudo ovs-vsctl -- set Port {0}-{1} qos=@newqos -- "
        "--id=@newqos create QoS type=linux-htb other-config:maxrate={3} queues={4}=@q{4} --"
        "--id=@q{4} create Queue other-config:min-rate={2} other-config:max-rate={3}"
        .format(switch, switchInterface, minBitsPerSecond, maxBitsPerSecond, queue_id))