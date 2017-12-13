from pox.core import core  
import pox.openflow.libopenflow_01 as of  
from pox.lib.revent import *  
from pox.lib.recoco import Timer  
from collections import defaultdict  
from pox.openflow.discovery import Discovery  
from pox.lib.util import dpid_to_str  
import time

class tableStats(EventMixin):  
    def __init__(self,interval = 10):
        self.tableActiveCount = {}
        self.interval = interval
        core.openflow.addListeners(self)
    def _handle_ConnectionUp(self,event):
        print("Switch %s has connected" % event.dpid)
        self.sendTableStatsRequest(event)
    def _handle_TableStatsReceived(self,event):
        sw = 's%s'%event.dpid
        self.tableActiveCount[sw] = event.stats[0].active_count
        print "TableStatsReceived"
        print self.tableActiveCount
        Timer(self.interval, self.sendTableStatsRequest,args=[event])
    def sendTableStatsRequest(self, event):
        sr = of.ofp_stats_request()
        sr.type = of.OFPST_TABLE
        event.connection.send(sr)
        print "Send table stat message to Switch %s " %event.dpid

def launch(interval = '10'):  
    interval = int(interval)
    core.registerNew(tableStats,interval)