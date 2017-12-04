class InvalidCommand:
    replyType = 2
    def __init__(self, replyString):
        self.invalidMessage = (str(self.replyType)+","+str(replyString.count('')-1)+","+str(replyString)).encode("ascii")