class Executor:
    def __init__(self):
        self.history = []

    def __repr__(self):
        string = ""
        for command in self.history:
            string += repr(command) + '\n'
        return string

    def execute(self, command):
        self.history.append(command)
        command.execute()

    def undo(self):
        command = self.history.pop()
        command.undo()