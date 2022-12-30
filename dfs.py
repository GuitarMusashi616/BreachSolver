from IPython.core.display import display
import sys

from command import MoveCommand, DamageUnitCommand, DamageCommand, SpawnCommand, HealUnitCommand
from destructable import Destructable
from executor import Executor
from tiles import CorporateTile, CivilianTile
from vek import Vek
from main import reset_grid


class DFS:
    def __init__(self, grid, cutoff=None):
        self.grid = grid
        self.explored = {}
        self.current = ""
        self.full_path = []
        self.protected = {}
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
            old_score = self.rate(self.grid)
            digits = self.append_current(action)
            action.execute()
            self.full_path.append(("DO", action, score))
            # new_score = self.rate(self.grid)
            # assert new_score == score, f"new score {new_score} != old score {score} at {action}"

            self.search(score)
            action.undo()
            new_old_score = self.rate(self.grid)
            assert old_score == new_old_score, f"new old score {new_old_score} does not equal {old_score}"
            self.full_path.append(("UNDO", action))
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
    def count_objectives(grid):
        power = DFS.power_count(grid)
        mech_alive = sum(1 for mech in grid.mechs if mech.health > 0)
        mech_total = sum(mech.health for mech in grid.mechs)
        vek_alive = sum(1 for vek in grid.veks if vek.health > 0)
        vek_total = sum(vek.health for vek in grid.veks)
        return power, mech_alive, mech_total, vek_alive, vek_total

    @staticmethod
    def count_objectives2(grid):
        spawn_tiles_covered = sum(grid.get_tile(x.coord).visitor for x in grid.end_commands if type(x) == "SpawnDamage")
        time_pods_recovered = 0  # tiles with mech and time pod
        time_pods_alive = 0  # time pods on map
        objectives_still_alive = 0  # objectives * tile on map

    @classmethod
    def rate_base(cls, grid, verbose=False):
        ex = Executor()

        before = cls.count_objectives(grid)

        for command in grid.end_commands:
            ex.execute(command)

        if verbose:
            display(grid.show())

        power, mech_alive, mech_total, vek_alive, vek_total = cls.count_objectives(grid)

        for command in ex.history[::-1]:
            command.undo()

        after = cls.count_objectives(grid)

        assert before == after, f"{before} {after}"

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
        # return 0 + power*20 - vek_total*2 - vek_alive*10 + mech_total*4 + mech_alive*40
        score = 0 + power * 10 - vek_total*2 - vek_alive * 10 + mech_total*3 + mech_alive*15
        return score

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




