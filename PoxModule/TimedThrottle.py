from pox.core import core
from pox.lib.recoco import Timer
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr

log = core.getLogger("Report: ")

s1_dpid = 0
globalEvent = None

def _handle_ConnectionUp (event):
    global s1_dpid
    print "ConnectionUp: ",
    dpidToStr(event.connection.dpid)
    
    #remember the connection dpid for switch
    for m in event.connection.features.ports:
        if m.name == "s1-eth1":
            s1_dpid = event.connection.dpid
            print "s1_dpid=", s1_dpid
def _handle_PacketIn(event):
    global s1_dpid, globalEvent

    print("PacketIn: ", dpidToStr(event.connection.dpid))    
    #openflow message to switch
    if event.connection.dpid == s1_dpid:
        #This code takes a packet from port 1 and forwards it to port 2
        msg = of.ofp_flow_mod()
        msg.priority =1
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.in_port = 1
        msg.actions.append(of.ofp_action_output(port = 2)) #in eth1 out eth2
        event.connection.send(msg)
        print("sent msg 1")

        #This code does the opposite. Port 2 -> port 1
        msg = of.ofp_flow_mod()
        msg.priority =1
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.in_port =2
        msg.actions.append(of.ofp_action_output(port = 1)) #in eth2 out eth1
        event.connection.send(msg)
        print("sent msg 2")
        
        #remember event, so that it can be used later to send another flow mod
        globalEvent = event
        log.debug("Changed Flow")

def sendFlowMod():
    global globalEvent
    log.debug("sending throttle message")
    msg = of.ofp_flow_mod()
    msg.priority = 100
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.match.dl_type = 0x0800
    msg.match.nw_src = "10.0.0.1"
    msg.match.nw_dst = "10.0.0.2"
    msg.actions.append(of.ofp_action_enqueue(port=2,queue_id=1)) #port 2 = eth2
    globalEvent.connection.send(msg)

def launch ():
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    core.callDelayed(45, sendFlowMod)