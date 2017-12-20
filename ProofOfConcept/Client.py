import socket
import sys
import subprocess

delegatorIP = '10.0.0.3'
delegatorPORT = 8008

def panic():
	#send panic
	try:
		myDelegator = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		myDelegator.connect((delegatorIP, delegatorPORT))
		myDelegator.send("PANIC/10.0.0.1/CLIENT")
		myDelegator.close()
	except Exception as e:
		print 'Could not send panic! ' + str(e)

def stop():
	#send stop
	try:
		myDelegator = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		myDelegator.connect((delegatorIP, delegatorPORT))
		myDelegator.send("STOP/10.0.0.1/CLIENT")
		myDelegator.close()
	except Exception as e:
		print 'Could not send stop! ' + str(e)


if __name__ == "__main__":

	#start an iperf server
	p = subprocess.Popen(["xterm", "-e", "iperf", "-s"])

	while True:
		inString = raw_input('>>')

		if inString == 'panic':
			panic()
		elif inString == 'stop':
			stop()
		else:
			print 'Wrong input!'