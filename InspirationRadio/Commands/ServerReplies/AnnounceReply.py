class Announce:
    replyType = 1

    def __init__(self, message, currentSongList):
        self.songname = ""
        splitMessage = message.split(",")
        self.stationNumber = int(splitMessage[1])
        try:
            self.songname = currentSongList[self.stationNumber]
        except:
            self.songname = False
        if not self.songname:
            self.announceReply = (str(self.replyType)+","+str(self.songname.count('')-1)+","+
                                  str(self.songname)).encode("ascii")


