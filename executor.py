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

    def batch(self, commands):
        for command in commands:
            self.execute(command)

    def undo(self):
        command = self.history.pop()
        command.undo()

    def undo_all(self):
        while self.history:
            self.undo()