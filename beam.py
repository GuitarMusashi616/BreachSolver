from abc import abstractmethod

from command import ICommand
from util import Compass


class IBeam(ICommand):
    "Used for beam type weapons"
    @abstractmethod
    def __init__(self, unit, grid, direction, damage):
        pass


class VekBeam(IBeam):
    def __init__(self, unit, grid, direction, damage):
        assert direction in Compass.FACES, f"{direction} should be a unit vector eg. {(0, 1)}"
        self.unit = unit
        self.grid = grid
        self.direction = direction
        self.damage = damage

    def __repr__(self):
        return f"{self.__class__.__name__} at {self.unit.coord} heading {Compass.match(self.direction)}"

    def execute(self):
        x, y = self.unit.coord
        dx, dy = self.direction
        try:
            for i in range(1, self.grid.square_len):
                tile = self.grid.get_tile((x + dx * i, y + dy * i))
                if not tile.can_move_through():
                    tile.damage(self.damage)
                    return

        except IndexError:
            return