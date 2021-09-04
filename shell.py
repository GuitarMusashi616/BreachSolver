from abc import ABC, abstractmethod

from command import ICommand, DamageCommand, SummonCommand, CompositeCommand, PushAwayCommand, DamageAdjacentCommand
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
            DamageAdjacentCommand(grid, coord, damage),
            PushAwayCommand(grid, coord),
        ]
        super().__init__(commands)

    def __repr__(self):
        return f"CLUSTER SHELL at {self.coord}"


class RegularShell(CompositeCommand, IShell):
    def __init__(self, unit, grid, damage, coord):
        self.coord = coord
        super().__init__([DamageCommand(grid, coord, damage), PushAwayCommand(grid, coord)])

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
        commands.append(PushAwayCommand(grid, coord, faces))

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


class VekShell(IShell):
    def __init__(self, unit, grid, damage, coord):
        super().__init__(unit, grid, damage, coord)
        self.unit = unit
        self.offset = self.determine_offset(self.unit.coord, coord)
        self.grid = grid
        self.damage = damage
        self.tile_damaged = None

    def __repr__(self):
        return f"VEK SHELL at {self.coord}"

    def execute(self):
        if not self.unit.is_alive:
            return
        try:
            tile = self.grid.get_tile(self.coord)
            tile.damage(self.damage)
            self.tile_damaged = tile
        except IndexError:
            return

    @property
    def coord(self):
        x, y = self.unit.coord
        dx, dy = self.offset
        return x + dx, y + dy

    def undo(self):
        if self.tile_damaged is None:
            return
        self.tile_damaged.heal(self.damage)

    @staticmethod
    def determine_offset(from_coord, to_coord):
        xi, yi = from_coord
        xf, yf = to_coord

        return xf-xi, yf-yi



