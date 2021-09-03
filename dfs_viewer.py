from IPython.core.display import display


class DFSViewer:
    def __init__(self, grid, dfs=None):
        self.grid = grid
        if dfs:
            ls = dfs.get_best()
            self.show_all_outcomes(ls)

    def show_all_outcomes(self, ls):
        for ins, score in ls:
            self.show_final_grid(ins, score)

    @staticmethod
    def gen_frontier(grid):
        frontier = {}
        for mech in grid.mechs:
            for _, action in mech.gen_actions().items():
                frontier[repr(action)] = action
        return frontier

    def show_final_grid(self, ins, score):
        history = []
        lines = ins.split("_")[:-1]
        print(score)
        frontier = self.gen_frontier(self.grid)
        for line in lines:
            assert line in frontier, f"{line} is not in {frontier}"
            frontier[line].execute()
            history.append(frontier[line])
            frontier = self.gen_frontier(self.grid)
        display(self.grid.show())
        for line in lines:
            print(line)
        print()
        for command in history[::-1]:
            command.undo()