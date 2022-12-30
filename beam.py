from abc import abstractmethod

from command import ICommand, CompositeCommand, DamageAdjacentCommand, DamageCommand, MoveCommand, DamageUnitCommand, \
    PushAndDamageCommand
from util import Compass


class IBeam(ICommand):
    "Used for beam type weapons"
    @abstractmethod
    def __init__(self, unit, grid, direction, damage):
        pass


class VekCommand(ICommand):
    """Wraps a command, only triggers if attached unit is alive"""

    def __init__(self, unit, command):
        self.unit = unit
        self.command = command
        self.has_been_executed = False

    def __repr__(self):
        return repr(self.command)

    def execute(self):
        if not self.unit.is_alive:
            return
        self.command.execute()
        self.has_been_executed = True

    def undo(self):
        if not self.has_been_executed:
            return
        self.command.undo()
        self.has_been_executed = False


class VekBeam(ICommand):
    def __init__(self, unit, grid, direction, damage):
        self.unit = unit
        self.grid = grid
        self.direction = direction
        self.damage = damage
        self.command = None

    def __repr__(self):
        return f"{self.__class__.__name__} at {self.unit.coord} heading {Compass.match(self.direction)}"

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
                self.command.execute()
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
        self.commands = []

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
                self.commands = [MoveCommand(self.grid, self.unit.coord, tile.coord)]
                for command in self.commands:
                    command.execute()
                return

            if tile.ground_vek_dies_when_pushed_into() and not self.unit.is_flying and not self.unit.is_massive:
                self.commands = [DamageUnitCommand(self.unit, self.unit.health, self.grid)]
                for command in self.commands:
                    command.execute()
                return

            if not tile.can_move_through():
                new_tile = self.grid.get_tile((x + dx * (i - 1), y + dy * (i - 1)))
                self.commands = [MoveCommand(self.grid, self.unit.coord, new_tile.coord), PushAndDamageCommand(self.grid, tile.coord, self.direction, self.damage)]
                for command in self.commands:
                    command.execute()
                return

    def undo(self):
        for command in self.commands[::-1]:
            command.undo()
        self.commands = []


# class BlobExplode(ICommand):
#     def __init__(self, unit, grid, damage):
#         self.unit = unit
#         self.grid = grid
#         self.commands = []
#         self.damage = damage
#
#     def __repr__(self):
#         return f"EXPLODE {self.unit} at {self.unit.coord}"
#
#     def execute(self):
#         if not self.unit.is_alive:
#             return
#
#         coord = self.unit.coord
#         self.commands.extend([DamageAdjacentCommand(self.grid, coord, 1), DamageCommand(self.grid, coord, 1)])
#         for command in self.commands:
#             command.execute()
#
#     def undo(self):
#         for command in self.commands[::-1]:
#             command.undo()
#         self.commands = []


class AcidBeam(IBeam):  # todo: refactor beam class with composite beam class, also get rid of vek unit alive thing
    def __init__(self, unit, grid, direction, damage):
        super().__init__(unit, grid, direction, damage)
        self.unit = unit
        self.grid = grid
        self.direction = direction
        self.damage = damage
        self.command = None

    def __repr__(self):
        return f"{self.__class__.__name__} at {self.unit.coord} heading {Compass.match(self.direction)}"

    def execute(self):
        x, y = self.unit.coord
        dx, dy = self.direction
        for i in range(1, self.grid.square_len + 1):
            try:
                tile = self.grid.get_tile((x + dx * i, y + dy * i))
            except IndexError:
                return

            if not tile.can_move_through():
                self.command = PushAndDamageCommand(self.grid, tile.coord, self.direction, self.damage)
                self.command.execute()
                return

    def undo(self):
        if self.command is None:
            return
        self.command.undo()
        self.command = None


class UnstableBeam(AcidBeam):
    def execute(self):
        x, y = self.unit.coord
        dx, dy = self.direction
        for i in range(1, self.grid.square_len + 1):
            try:
                tile = self.grid.get_tile((x + dx * i, y + dy * i))
            except IndexError:
                return

            if not tile.can_move_through():
                self.command = CompositeCommand([
                    PushAndDamageCommand(self.grid, tile.coord, self.direction, self.damage),
                    PushAndDamageCommand(self.grid, self.unit.coord, (dx*-1, dy*-1), self.damage//2)
                ])
                self.command.execute()
                return