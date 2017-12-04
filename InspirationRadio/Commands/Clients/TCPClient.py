from Commands.ClientCommands.AskSongCommand import AskSong
from Commands.ClientCommands.HelloCommand import Hello
import socket

class TCPClient:
    def __init__(self):
        self.serverip = "2.109.204.102"
        self.serverport = 5786

    def InitiateTCPClient(self, serverIP, serverPort):
        clienSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clienSocket.connect((serverIP, serverPort))

        #step 1 of protocol: say hello
        hello = Hello()
        clienSocket.send(hello.helloCommand)

        #expect WelcomeReply
        serverReply = clienSocket.recv(1024)
        serverReply = serverReply.decode("ascii")
        print(serverReply)
        if serverReply[:1] != "0":
            print("0 did not receive WelcomeReply")

        #send AskSongCommand
        asksong = AskSong(2)
        clienSocket.send(asksong.askSongCommand)

        #expect AnnounceReply
        serverReply1 = clienSocket.recv(1024)
        serverReply1 = serverReply1.decode("ascii")
        print(serverReply1)
        if serverReply1[:1] != "1":
            print("1 did not receive AnnounceReply")

        clienSocket.close()

q = TCPClient()
q.InitiateTCPClient(q.serverip, q.serverport)
