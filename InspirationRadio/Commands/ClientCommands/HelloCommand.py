class Hello:
    commandType = 0

    def __init__(self):
        self.helloCommand = (str(self.commandType)).encode("ascii")