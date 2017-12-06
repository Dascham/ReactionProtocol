import socket
serveripaddress = "10.0.0.1"
serverPort = 5555
msg = "Hello"
msg = msg.encode("ascii")
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSocket.bind(('', 5556))

clientSocket.sendto(msg, (serveripaddress, serverPort))