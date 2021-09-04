from abc import abstractmethod

from command import ICommand
from util import Compass


class IMelee(ICommand):
    "Used for melee type weapons"
    @abstractmethod
    def __init__(self, unit, grid, direction, damage):
        pass


class VekMelee(IMelee):
    def __init__(self, unit, grid, direction, damage, reach=1):
        super().__init__(unit, grid, direction, damage)
        assert direction in Compass.FACES, f"{direction} should be a unit vector eg. {(0, 1)}"
        self.unit = unit
        self.grid = grid
        self.direction = direction
        self.damage = damage
        self.reach = reach
        self.tile_damaged = []

    def __repr__(self):
        return f"{self.__class__.__name__} at {self.unit.coord} attacking {Compass.match(self.direction)} {self.reach} tiles"

    def execute(self):
        if not self.unit.is_alive:
            return

        x, y = self.unit.coord
        dx, dy = self.direction
        try:
            for i in range(1, self.reach+1):
                try:
                    tile = self.grid.get_tile((x+dx*i, y+dy*i))
                except IndexError:
                    continue
                if not tile.can_move_through():
                    tile.damage(self.damage)
                    self.tile_damaged.append(tile)

        except IndexError:
            return

    def undo(self):
        for tile in self.tile_damaged:
            tile.heal(self.damage)

        self.tile_damaged = []
