from pox.core import core
from pox.lib.util import dpid_to_str
import socket
from pox.lib.recoco import Timer


log = core.getLogger()


class MyComponent (object):
  def __init__ (self):
    core.openflow.addListeners(self)
 
  def _handle_ConnectionUp (self, event):
    log.debug("Switch %s has come up.", dpid_to_str(event.dpid))

def launch ():
  core.registerNew(MyComponent)