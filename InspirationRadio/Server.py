from Commands.ServerReplies.AnnounceReply import Announce
from Commands.ServerReplies.InvalidCommandReply import InvalidCommand
from Commands.ServerReplies.WelcomeReply import Welcome
from Commands.Clients.TCPClient import TCPClient
import socket
from threading import Thread

numberOfStations = 2
currentSongList = [None] * 2

radioStations = ["224.0.105.128", ["224.0.105.129"]] #multicastgroups
timeout = 0.1
helpfulMessages = [""]
portNumber = 5786
MCastGroup_0 = "224.0.105.128" #send song data here


def HandleIndividualTCPConnections(connectionSocket, message):
    #expect HelloCommand
    if message[:1] == 0:
        welcome = Welcome(numberOfStations, MCastGroup_0, portNumber)
        welcomeReply = welcome.welcomeReply
        connectionSocket.send(welcomeReply)

        #expect AskSongCommand
        message = connectionSocket.recv(1024)
        message = message.decode("ascii")
        if message[:1] == 1:
            #check that requested radio station exists
            announce = Announce(message, currentSongList)
            if not announce.songname:
                msg = "Radio station "+str(announce.stationNumber)+" does not exist"
                invalidCommand = InvalidCommand(msg)
                connectionSocket.send(invalidCommand)
                connectionSocket.close()
            else:
                #get currently playing song on station defined by message and send
                announceReply = announce.announceReply
                connectionSocket.send(announceReply)
                connectionSocket.close()
        else:
            msg = "Expected: 1 AskSongCommand"
            invalidCommand = InvalidCommand(msg)
            connectionSocket.send(invalidCommand.invalidMessage)

    else:
        errormsg = "Expected a \"HelloCommand\""
        invalidcommand = InvalidCommand(errormsg)
        connectionSocket.send(invalidcommand.invalidMessage)
        connectionSocket.close()


def ListenTCPConnections():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('', portNumber))
    serverSocket.listen(1)
    print("Server is good to go on TCP")

    threads = []
    #follow custom protocol from here
    while 1:
        connectionSocket, addr = serverSocket.accept()
        message = connectionSocket.recv(1024)
        message = message.decode("ascii")

        if not message:
            thread = Thread(target=HandleIndividualTCPConnections(connectionSocket, message))
            threads.append(thread)
            thread.start()


#send song data
def TransmitSongData():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind(('', portNumber))
    print("Server is good to go on UDP")

    msg = "This message should be song data".encode("ascii")
    while 1:
        serverSocket.sendto(msg, (MCastGroup_0, portNumber))

#On server start-up, song data should start being transmitted
try:
    thread1 = Thread(target=TransmitSongData)
    thread2 = Thread(target=ListenTCPConnections)

    print("Starting thread1")
    thread1.start()
    print("Starting thread2")
    thread2.start()
except:
    print("Could not start threads")