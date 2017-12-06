import socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind(('', 5555))
print("server running")

msg = serverSocket.recv(1024)
msg = msg.decode("ascii")
print(msg)