'''
This is the client program, running 1...n hosts in Mininet.
The client is acting as the DDoS victim, and can send out
'panic' and 'stop' signals to its own delegegator (hardcoded IP).
Furthermore, it hosts an iperf server, for performing iperf tests
from other hosts.
'''

import socket
import sys
import subprocess

# Hardcoded delegator details
delegatorIP = '10.0.0.3'
delegatorPORT = 8008

# Send a panic signal to the delegator
def panic():
	try:
		myDelegator = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		myDelegator.connect((delegatorIP, delegatorPORT))
		myDelegator.send("PANIC/10.0.0.1/CLIENT")
		myDelegator.close()
	except Exception as e:
		print 'Could not send panic! ' + str(e)

# Send a stop signal to the delegator
def stop():
	try:
		myDelegator = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		myDelegator.connect((delegatorIP, delegatorPORT))
		myDelegator.send("STOP/10.0.0.1/CLIENT")
		myDelegator.close()
	except Exception as e:
		print 'Could not send stop! ' + str(e)


if __name__ == "__main__":

	# Start an iperf server in a subprocess, and open in an xterm window
	iperfServ = subprocess.Popen(["xterm", "-e", "iperf", "-s"])

	# The user can manually input 'panic' or 'stop' into the program
	# in order to send a signal of the respective type
	while True:
		inString = raw_input('>>')

		if inString == 'panic':
			panic()
		elif inString == 'stop':
			stop()
		else:
			print 'Wrong input!'