import socket
import sys
import thread

#Server listens, and prints shit

HOST = '192.168.2.4'
PORT = 8888

def printer(string):
	print '******\n' + string

if __name__ == "__main__":
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
	serversocket.bind((HOST, PORT))
	serversocket.listen(5)

	print "Ready to recieve..."

	while True:
		client, addr = serversocket.accept()
		thread.start_new_thread(printer, (client.recv(4096),))