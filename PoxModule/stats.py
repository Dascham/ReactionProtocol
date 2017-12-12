from pox.core import core
from pox.lib.recoco import Timer
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr

log = core.getLogger("Stats")

tableActiveCount = {}
#allConnections = set()
'''
def _handle_ConnectionUp (event):
    allConnections.add(event.connection)
    print(event.connection)
'''
def _handle_TableStatsReceived(event):
    print("Something even more")
    sw = 's%s'%event.dpid
    tableActiveCount[sw] = event.stats[0].active_count
    print("TableStatsReceived")
    print(tableActiveCount)

def sendTableStatsRequest():
    print("Something")
    for con in core.openflow.connections:
        print("Something more")
        sr = of.ofp_stats_request()
        sr.type = of.OFPST_TABLE
        con.send(sr)
        print("Send table stat message to Switch")

def launch():
    core.openflow.addListenerByName("TableStatsReceived", _handle_TableStatsReceived)
    #core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    Timer(5, sendTableStatsRequest, recurring=True)