from IPython.core.display import display

from dfs import DFS


class DFSViewer:
    def __init__(self, grid, dfs):
        self.grid = grid
        self.ls = dfs.get_best()

    def show(self, index, verbose=False):
        ins, score = self.ls[index]
        history = self.apply_to_grid(ins, verbose)
        print(score)
        DFS.rate_base(self.grid, True)
        print(DFS.rate_dict(self.grid))
        for command in history[::-1]:
            command.undo()

    def show_all_outcomes(self, ls):
        for ins, score in ls:
            self.show_final_grid(ins, score)

    def show_all(self):
        for i in range(len(self.ls)):
            print(f"{i})")
            self.show(i)

    @staticmethod
    def gen_frontier(grid):
        frontier = {}
        for mech in grid.mechs:
            for _, action in mech.gen_actions().items():
                frontier[repr(action)] = action
        return frontier

    def apply_to_grid(self, ins, verbose=False):
        history = []
        if verbose:
            display(self.grid)
        lines = ins.split("_")[:-1]
        frontier = self.gen_frontier(self.grid)
        if verbose:
            display(self.grid.show())
        for line in lines:
            assert line in frontier, f"{line} is not in {frontier}"
            frontier[line].execute()
            if verbose:
                print(line)
                display(self.grid.show())
            history.append(frontier[line])
            frontier = self.gen_frontier(self.grid)
        return history

    def show_final_grid(self, ins, score):
        print(score)
        history = self.apply_to_grid(ins)
        display(self.grid.show())

        for line in ins.split("_")[:-1]:
            print(line)
        print()

        for command in history[::-1]:
            command.undo()

    @classmethod
    def apply(cls, grid, string):
        frontier = cls.gen_frontier(grid)
        lines = string.split("\n")
        for line in lines:
            assert line in frontier, f"{line} of {lines} is not in {frontier}"
            frontier[line].execute()
        return grid

