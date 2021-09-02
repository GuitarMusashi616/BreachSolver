class Executor:
    def __init__(self):
        self.history = []

    def execute(self, command):
        self.history.append(command)
        command.execute()

    def undo(self):
        command = self.history.pop()
        command.undo()