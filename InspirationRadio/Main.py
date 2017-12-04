#this will be internet radio
import time, struct, socket
from threading import Thread

mcastgroup = "226.55.55.25"
secondary = "224.0.105.128"
port = 5786

def ReceiveFrom(number):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    clientSocket.bind(('', port))

    mreq = struct.pack("4sl", socket.inet_aton(secondary), socket.INADDR_ANY)

    clientSocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while 1:
        data = clientSocket.recv(10240)
        data = data.decode("ascii")
        print(data+" "+str(number))

def SendToMulticastGroup():

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    serverSocket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    msg = "you getting this?"
    msg = msg.encode("ascii")
    a = 0
    b = 20
    while a < b:
        serverSocket.sendto(msg, (secondary, port))
        a = a + 1
        time.sleep(3)

try:
    thread1 = Thread(target = ReceiveFrom, args=(1, ))
    thread2 = Thread(target=ReceiveFrom, args=(2, ))
    thread3 = Thread(target=ReceiveFrom, args=(3, ))
    thread4 = Thread(target=ReceiveFrom, args=(4, ))
    thread5 = Thread(target=ReceiveFrom, args=(5, ))
    thread6 = Thread(target = SendToMulticastGroup)

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    thread6.start()
except:
    print("stuff didn't work or something")

a = 0
b = 100
while a < b:
    a = a+1
    time.sleep(4)
    pass