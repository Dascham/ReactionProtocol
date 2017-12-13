import os, time, socket
from pox.core import core
from pox.lib.util import dpid_to_str
from threading import Thread


'''
the actual component that will be used with pox
./pox.py [some pox component, for example l2_learning] [this component]
'''

class Component(object):

	def __init(self):
		self.tableActiveCount = {}
		core.openflow.addListeners(self)

	def Initiate(self):
		var = 0

		RequestFlowStats()
		PrintFlowStats()

	def RequestFlowStats():

	def PrintFlowStats():

    def launch(self):
        core.registerNew(Component)
        Timer(15, Initiate)