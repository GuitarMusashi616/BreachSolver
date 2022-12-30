from IPython.core.display import display

from dfs import DFS


class DFSViewer:
    def __init__(self, grid, dfs):
        self.grid = grid
        self.ls = dfs.get_best()

    def show(self, index, show_grid=True, verbose=False):

        ins, score = self.ls[index]
        history = self.apply_to_grid(ins, verbose)
        print(score)
        DFS.rate_base(self.grid, show_grid)
        print(DFS.rate_dict(self.grid))

        for command in history[::-1]:
            command.undo()

    def get_df(self, limit):
        for index in range(limit):

            ins, score = self.ls[index]
            history = self.apply_to_grid(ins, False)
            commands = [x for x in self.grid.end_commands]
            for command in commands:
                command.execute()
            df = self.grid.show()
            if repr(df.iloc[3][4]) == "🏘️ ϟ":
                display(df)
            for command in commands[::-1]:
                command.undo()
            for command in history[::-1]:
                command.undo()

    def show_range(self, range):
        for i in range:
            self.show(i, False, False)

    def quick_peek(self, max_i=50):
        explored = {}
        print("Power", "Veks", "Vek Total Health", "Mechs", "Mech Total Health", sep="\t")
        for i, stuff in enumerate(self.ls):
            if i >= max_i:
                return
            ins, score = stuff
            history = self.apply_to_grid(ins)
            dic = DFS.rate_dict(self.grid)
            string = ""
            scores = []
            for key, val in dic.items():
                scores.append(val)
                string += str(val)
            if string not in explored:
                explored[string] = True
                print(f"{i}) {scores}")
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
