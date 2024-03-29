from abc import ABC, abstractmethod

from command import ICommand, DamageCommand, SummonCommand, CompositeCommand, PushAwayAndDamageCommand, \
    DamageAdjacentCommand, DamageUnitCommand
from unit import Unit
from util import Compass


class IShell(ICommand):
    "Used for artillery type weapons"
    @abstractmethod
    def __init__(self, unit, grid, damage, coord):
        pass

    @abstractmethod
    def __repr__(self):
        pass


class ClusterShell(CompositeCommand, IShell):
    def __init__(self, unit, grid, damage, coord):
        self.coord = coord
        commands = [
            PushAwayAndDamageCommand(grid, coord, damage=damage),
        ]
        super().__init__(commands)

    def __repr__(self):
        return f"CLUSTER SHELL at {self.coord}"


class RegularShell(CompositeCommand, IShell):
    def __init__(self, unit, grid, damage, coord):
        self.coord = coord
        super().__init__([DamageCommand(grid, coord, damage), PushAwayAndDamageCommand(grid, coord)])

    def __repr__(self):
        return f"REGULAR SHELL at {self.coord}"


class BoulderShell(CompositeCommand, IShell):
    def __init__(self, unit, grid, damage, coord):
        self.coord = coord
        faces = self.determine_which_way_to_push(coord, unit.coord)

        commands = []
        tile = grid.get_tile(coord)
        if tile.can_move_through():
            commands.append(SummonCommand(Unit("Boulder", max_health=1, health=1, moves=0), grid, coord))
        else:
            commands.append(DamageCommand(grid, coord, damage))
        commands.append(PushAwayAndDamageCommand(grid, coord, faces))

        super().__init__(commands)

    @staticmethod
    def determine_which_way_to_push(to_coord, from_coord):
        unit_vec = Compass.get_direction(from_coord, to_coord)
        faces = [Compass.NORTH, Compass.SOUTH]
        if unit_vec == Compass.NORTH or unit_vec == Compass.SOUTH:
            faces = [Compass.EAST, Compass.WEST]
        return faces

    def __repr__(self):
        return f"BOULDER SHELL at {self.coord}"


class JumpShell(CompositeCommand, IShell):
    def __init__(self, unit, grid, damage, coord):
        commands = [
            PushAwayAndDamageCommand(grid, coord, damage=damage),
            DamageUnitCommand(unit, damage, grid),
        ]
        self.coord = coord
        super().__init__(commands)

    def __repr__(self):
        return f"JUMP SHELL at {self.coord}"


class VekShell(IShell):
    def __init__(self, unit, grid, damage, coord):
        super().__init__(unit, grid, damage, coord)
        self.unit = unit
        self.offset = self.determine_offset(self.unit.coord, coord)
        self.grid = grid
        self.damage = damage
        self.command = None

    def __repr__(self):
        return f"VEK SHELL at {self.coord}"

    def execute(self):
        if not self.unit.is_alive:
            return
        self.command = DamageCommand(self.grid, self.coord, self.damage)
        self.command.execute()

    @property
    def coord(self):
        x, y = self.unit.coord
        dx, dy = self.offset
        return x + dx, y + dy

    def undo(self):
        if self.command is None:
            return
        self.command.undo()

    @staticmethod
    def determine_offset(from_coord, to_coord):
        xi, yi = from_coord
        xf, yf = to_coord

        return xf-xi, yf-yi



