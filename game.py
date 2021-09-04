from IPython.core.display import display
from IPython.display import clear_output
from time import sleep

from command import MoveCommand
from executor import Executor


class Game:
    def __init__(self, grid, out_of_order=False):
        self.grid = grid
        self.ex = Executor()
        if out_of_order:
            self.out_of_order_rounds(1)
        else:
            self.round(1)

    def __repr__(self):
        return repr(self.grid)

    def show(self):
        display(self.grid.show())

    def clear(self):
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
        self.show()
        for _ in self.grid.mechs:
            self.turn()

        self.ask_for_next_round(self.round, i+1)

    def ask_for_next_round(self, func, i):
        answer = input("next round (y/n)?")
        if answer == 'y':
            for _, unit in self.grid.units.items():
                unit.reset_turn()
            func(i)
        else:
            return

    @staticmethod
    def gen_mech_frontier(grid):
        frontier = []
        for mech in grid.mechs:
            for _,action in mech.gen_actions().items():
                frontier.append(action)
        return frontier

    @staticmethod
    def gen_vek_frontier(grid):
        frontier = []
        for vek in grid.veks:
            for _, action in vek.gen_actions().items():
                frontier.append(action)
        return frontier

    def out_of_order_rounds(self, i):
        print(f"Round {i}")
        frontier = self.gen_mech_frontier(self.grid)
        j = 1
        while frontier:
            self.clear()
            print(f"Turn {j}")
            self.show()
            action = self.make_choice("Which action? ", frontier)
            self.ex.execute(action)
            frontier = self.gen_mech_frontier(self.grid)
            j += 1

        self.vek_turn()
        self.ask_for_next_round(self.out_of_order_rounds, i+1)

    def vek_turn(self):
        frontier = self.gen_vek_frontier(self.grid)
        commands = []
        j = 1
        while frontier:
            self.clear()
            print(f"Turn {j}")
            self.show()
            action = self.make_choice("Which action? ", frontier)
            if not isinstance(action.command, MoveCommand):
                commands.append(action)
                action.unit.target = action
            self.ex.execute(action)
            frontier = self.gen_vek_frontier(self.grid)
            j += 1
        for command in commands[::-1]:
            command.undo()

    def turn(self):
        mech = self.make_choice("Which Mech to Move? ", [mech for mech in self.grid.mechs if mech.gen_actions()])
        print()
        print(f"{mech} moves:")
        actions = mech.gen_actions()
        while actions:
            self.show()
            action = self.make_choice("Which Move? ", actions)
            self.clear()
            self.ex.execute(action)
            actions = mech.gen_actions()