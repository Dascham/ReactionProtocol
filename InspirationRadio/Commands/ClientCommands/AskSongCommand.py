class AskSong:
    commandType = 1
    def __init__(self, stationnumber):
        self.askSongCommand = (str(self.commandType)+","+str(stationnumber)).encode("ascii")