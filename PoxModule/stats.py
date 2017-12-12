from pox.core import core
from pox.lib.recoco import Timer
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr

from pox.openflow.libopenflow_01 import *
from pox.lib.packet import *



log = core.getLogger("Stats")

tableActiveCount = {}
#allConnections = set()
'''
def _handle_ConnectionUp (event):
    allConnections.add(event.connection)
    print(event.connection)
'''

'''
def _handle_TableStatsReceived(event):
    sw = 's%s'%event.dpid
    tableActiveCount[sw] = event.stats[0].active_count
    print("TableStatsReceived")
    print(tableActiveCount)

def sendTableStatsRequest():
    for con in core.openflow.connections:
        sr = of.ofp_stats_request()
        sr.type = of.OFPST_TABLE
        con.send(sr)
        print("Sent table stat message to Switch")
'''
def HandleFlowStats(event):
    ipaddress="10.0.0.1"
    #match = of.ofp_match(nw_dst=ipaddress)

    for flows in event.stats:
        if flows.match.nw_dst == "10.0.0.1":
            print("Printing stats")
            print(flows.table_id)
            for action in flows.actions:
                print("Port %s" % action.port)

def sendFlowStatsRequest():
    for con in core.openflow.connections:
        #sr = of.ofp_stats_request()
        #sr.type = of.OFPST_FLOW
        con.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))
        print("Sent flow stats request message to Switch")

def launch():
    #core.openflow.addListenerByName("TableStatsReceived", _handle_TableStatsReceived)
    core.openflow.addListenerByName("FlowStatsReceived", HandleFlowStats)
    Timer(5, sendFlowStatsRequest, recurring=True)

def receivePanic():
    open socket