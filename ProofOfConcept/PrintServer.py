'''
For ease of use, we used a Print Server (this program).
The clients/delegators and the ThrottleManager all connects,
and prints to this server, as opposed to their own terminal or log.
This is simply a means of collecting data into a single terminal,
to monitor what happens on various hosts at runtime.
'''

import socket
import sys
import thread

HOST = '192.168.2.4'
PORT = 8888

def printer(string):
	print '******\n' + string

# Host a server
if __name__ == "__main__":
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
	serversocket.bind((HOST, PORT))
	serversocket.listen(5)

	print "Ready to recieve..."

	# When a message is heard from a client, print to terminal, in a thread
	while True:
		client, addr = serversocket.accept()
		thread.start_new_thread(printer, (client.recv(4096),))