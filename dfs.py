from IPython.core.display import display

from command import MoveCommand, DamageUnitCommand, DamageCommand, SpawnCommand
from destructable import Destructable
from tiles import CorporateTile, CivilianTile
from unit import Vek
from main import reset_grid

class DFS:
    def __init__(self, grid, cutoff=None):
        self.grid = grid
        self.explored = {}
        self.current = ""
        self.full_path = []
        self.cutoff = cutoff
        self.search(self.rate(self.grid))

    def append_current(self, action):
        char = repr(action) + "_"
        self.current += char
        return len(char)

    def pop_current(self, digits):
        self.current = self.current[:-digits]

    def search(self, curr_score):
        frontier = self.gen_rated_frontier(self.grid)
        if not frontier:
            self.explored[self.current] = curr_score
        #             print(f"{self.current} = {curr_score}")

        frontier = list(
            filter(lambda x: (isinstance(x[0].command, MoveCommand) and x[1] >= curr_score) or x[1] > curr_score,
                   frontier))
        frontier.sort(key=lambda x: x[1], reverse=True)
        if self.cutoff:
            frontier = frontier[:self.cutoff]

        for action, score in frontier:
            digits = self.append_current(action)
            action.execute()
            self.full_path.append(action)
            new_score = self.rate(self.grid)
            if new_score != score:
                print(f"new score {new_score} != old score {score} at {self.current}")
                print(self.full_path)
                return

            self.search(score)
            action.undo()
            self.pop_current(digits)

    @classmethod
    def gen_rated_frontier(cls, grid):
        """returns action and rating"""
        frontier = []
        for mech in grid.mechs:
            for k, action in mech.gen_actions().items():
                score = cls.alter_rate_and_unalter(grid, action)
                frontier.append((action, score))

        return frontier

    @classmethod
    def rate_dict(cls, grid, verbose=False):
        power, mech_alive, mech_total, vek_alive, vek_total = cls.rate_base(grid, verbose)
        return {'Power': power, 'Veks': vek_alive, 'Vek Total Health': vek_total, 'Mechs': mech_alive,
                'Mech Total Health': mech_total}

    @staticmethod
    def rate_base(grid, verbose=False):
        commands = []

        commands.extend([
            DamageUnitCommand(grid.find('Alpha Firefly'), 1, grid),
            DamageCommand(grid, (5, 1), 1),
            DamageCommand(grid, (5, 1), 2),
            DamageCommand(grid, (6, 3), 1),
            DamageCommand(grid, (6, 4), 1),
            SpawnCommand(grid, (6, 2), Vek("Firefly")),
            SpawnCommand(grid, (5, 4), Vek("Firefly")),
        ])

        for vek in grid.veks:
            commands.append(vek.target)

        for command in commands:
            command.execute()

        if verbose:
            display(grid.show())

        power = DFS.power_count(grid)

        # power = sum(
        #     sum(tile.type_object.health for tile in tiles if '🏢' in repr(tile) or '🏘️' in repr(tile)) for tiles in
        #     grid.tiles)
        mech_alive = sum(1 for mech in grid.mechs if mech.health > 0)
        mech_total = sum(mech.health for mech in grid.mechs)
        vek_alive = sum(1 for vek in grid.veks if vek.health > 0)
        vek_total = sum(vek.health for vek in grid.veks)

        for command in commands[::-1]:
            command.undo()

        return power, mech_alive, mech_total, vek_alive, vek_total

    @staticmethod
    def power_count(grid):
        power = 0
        for tiles in grid.tiles:
            for tile in tiles:
                type_object = tile.type_object
                if isinstance(type_object, Destructable):
                    type_object = type_object.tile
                    if isinstance(type_object, CorporateTile) or isinstance(type_object, CivilianTile):
                        power += type_object.health
        return power

    @classmethod
    def rate(cls, grid):
        power, mech_alive, mech_total, vek_alive, vek_total = cls.rate_base(grid)
        return 0 + power * 5 - vek_total - vek_alive * 10 + mech_total + mech_alive * 10

    @classmethod
    def alter_rate_and_unalter(cls, grid, action):
        action.execute()
        score = cls.rate(grid)
        action.undo()
        return score

    def show(self):
        ls = self.get_best()
        for ins, score in ls:
            print(score)
            for line in ins.split("_"):
                print(line)

    def get_best(self):
        ls = list(self.explored.items())
        ls.sort(key=lambda x: x[1], reverse=True)
        return ls



