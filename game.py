from IPython.core.display import display
from IPython.display import clear_output
from time import sleep
from executor import Executor


class Game:
    def __init__(self, grid):
        self.grid = grid
        self.ex = Executor()
        self.round(1)

    def show(self):
        display(self.grid.show())

    def clear(self):
        return
        clear_output(wait=True)

    def make_choice(self, query, ls):
        offset = 0
        if isinstance(ls, list):
            offset = -1
            i = 1
            for v in ls:
                print(f"{i}) {v}")
                i += 1
        else:
            for i, v in ls.items():
                print(f"{i}) {v}")

        while True:
            choice = input(query)
            if choice == "":
                return
            elif choice == "undo":
                self.ex.undo()
                self.show()
                continue
            try:
                num = int(choice)
                assert 0 < num <= len(ls)
            except (ValueError, AssertionError):
                print(f"Must pick a number between {1} and {len(ls)}")
                continue
            return ls[num + offset]

    def round(self, i):
        print(f"Round {i}")
        for _ in self.grid.mechs:
            self.turn()

        answer = input("next round (y/n)?")
        if answer == 'y':
            for mech in self.grid.mechs:
                mech.reset_turn()
            self.round(i+1)
        else:
            return

    def turn(self):
        self.show()
        mech = self.make_choice("Which Mech to Move? ", [mech for mech in self.grid.mechs if mech.gen_actions()])
        print()
        print(f"{mech} moves:")
        actions = mech.gen_actions()
        while actions:
            action = self.make_choice("Which Move? ", actions)
            self.ex.execute(action)
            self.clear()
            self.show()
            actions = mech.gen_actions()