import socket, struct

class UDPClient:

    def ReceiveFrom(MCASTGroup):
        port = 5786
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        clientSocket.bind(('', port))

        #no clue what this is
        mreq = struct.pack("4sl", socket.inet_aton(MCASTGroup), socket.INADDR_ANY)

        #no clue what this is
        clientSocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        while 1:
            data = clientSocket.recv(10240)
            data = data.decode("ascii")
            print(data)