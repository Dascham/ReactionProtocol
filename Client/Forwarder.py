'''
This small program is launched by FastNetMon's
notify_about_attack.sh script, getting the victim IP
and possible details through the args.

Attack details are read in, and sent to the Linker (client)
arg1 = ip, arg2 = port
'''

import socket
import sys

if __name__=='__main__':
	linkerIP = socket.gethostbyname(socket.gethostname())
	VictimIP = sys.argv[1]

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((linkerIP, 1337))
	print VictimIP 
	sock.send(VictimIP)
	sock.close()