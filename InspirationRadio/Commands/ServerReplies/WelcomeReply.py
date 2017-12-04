class Welcome:
    replayType = 0

    def __init__(self, numstation, multicastgroup, portnumber):
        self.welcomeReply = (str(self.replayType)+","+str(numstation)+","+str(multicastgroup)+","+
                             str(portnumber)).encode("ascii")