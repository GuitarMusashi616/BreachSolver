from abc import abstractmethod

from command import ICommand, CompositeCommand, DamageAdjacentCommand, DamageCommand, MoveCommand, DamageUnitCommand
from util import Compass


class IBeam(ICommand):
    "Used for beam type weapons"
    @abstractmethod
    def __init__(self, unit, grid, direction, damage):
        pass


class VekBeam(ICommand):
    def __init__(self, unit, grid, direction, damage):
        self.unit = unit
        self.grid = grid
        self.direction = direction
        self.damage = damage
        self.command = None

    def __repr__(self):
        return f"{self.__class__.__name__} at {self.unit.coord} charging {Compass.match(self.direction)}"

    def execute(self):
        if not self.unit.is_alive:
            return

        x, y = self.unit.coord
        dx, dy = self.direction
        for i in range(1, self.grid.square_len+1):
            try:
                tile = self.grid.get_tile((x + dx * i, y + dy * i))
            except IndexError:
                return

            if not tile.can_move_through():
                self.command = DamageCommand(self.grid, tile.coord, self.damage)
                return

    def undo(self):
        if self.command is None:
            return
        self.command.undo()
        self.command = None


class VekCharge(ICommand):
    def __init__(self, unit, grid, direction, damage):
        self.unit = unit
        self.grid = grid
        self.direction = direction
        self.damage = damage
        self.command = None

    def __repr__(self):
        return f"{self.__class__.__name__} at {self.unit.coord} charging {Compass.match(self.direction)}"

    def execute(self):
        if not self.unit.is_alive:
            return

        x, y = self.unit.coord
        dx, dy = self.direction
        for i in range(1, self.grid.square_len+1):
            try:
                tile = self.grid.get_tile((x + dx * i, y + dy * i))
            except IndexError:
                tile = self.grid.get_tile((x + dx * (i-1), y + dy * (i-1)))
                self.command = MoveCommand(self.grid, self.unit.coord, tile.coord)
                return

            if tile.ground_vek_dies_when_pushed_into() and not self.unit.is_flying and not self.unit.is_massive:
                self.command = DamageUnitCommand(self.unit, self.unit.health, self.grid)
                return

            if not tile.can_move_through():
                self.command = DamageCommand(self.grid, tile.coord, self.damage)
                return

    def undo(self):
        if self.command is None:
            return
        self.command.undo()
        self.command = None



class BlobExplode(ICommand):
    def __init__(self, unit, grid, damage):
        self.unit = unit
        self.grid = grid
        self.commands = []
        self.damage = damage

    def __repr__(self):
        return f"EXPLODE {self.unit} at {self.unit.coord}"

    def execute(self):
        if not self.unit.is_alive:
            return

        coord = self.unit.coord
        self.commands.extend([DamageAdjacentCommand(self.grid, coord, 1), DamageCommand(self.grid, coord, 1)])
        for command in self.commands:
            command.execute()

    def undo(self):
        for command in self.commands[::-1]:
            command.undo()
        self.commands = []

