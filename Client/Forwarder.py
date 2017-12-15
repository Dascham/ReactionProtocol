#This will run, when FNM detects an attack.
#We read attack details, and pass it onto the Linker
#This will run beside FNM, and will point towards the Linker, found within Mininet.
#Program is run with arg1 = ip, arg2 = port
import socket
import sys

if __name__=='__main__':
	linkerIP = socket.gethostbyname(socket.gethostname())
	VictimIP = sys.argv[1]
	#TTL = sys.argv[2]

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((linkerIP, 1337))
	print VictimIP 
	sock.send(VictimIP)
	sock.close()