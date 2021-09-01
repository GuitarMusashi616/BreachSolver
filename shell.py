from abc import ABC, abstractmethod

from command import ICommand, DamageCommand, SummonCommand, CompositeCommand, PushAwayCommand
from unit import Unit
from util import Compass


class IShell(ICommand):
    "Used for artillery type weapons"
    @abstractmethod
    def __init__(self, grid, damage, to_coord, from_coord):
        pass


class ClusterShell(CompositeCommand, IShell):
    def __init__(self, grid, damage, coord, from_coord=None):
        self.coord = coord
        commands = []
        x, y = coord
        for dx, dy in Compass.FACES:
            commands.append(DamageCommand(grid, (x + dx, y + dy), damage))
        commands.append(PushAwayCommand(grid, coord))
        super().__init__(commands)

    def __repr__(self):
        return f"CLUSTER SHELL at {self.coord}"


class RegularShell(CompositeCommand, IShell):
    def __init__(self, grid, damage, coord, from_coord=None):
        self.coord = coord
        super().__init__([DamageCommand(grid, coord, damage), PushAwayCommand(grid, coord)])

    def __repr__(self):
        return f"REGULAR SHELL at {self.coord}"


class BoulderShell(CompositeCommand, IShell):
    def __init__(self, grid, damage, to_coord, from_coord):
        self.coord = to_coord
        faces = self.determine_which_way_to_push(to_coord, from_coord)

        commands = []
        tile = grid.get_tile(to_coord)
        if tile.can_move_through():
            commands.append(SummonCommand(Unit("Boulder", max_health=1, health=1, moves=0), grid, to_coord))
        else:
            commands.append(DamageCommand(grid, to_coord, damage))
        commands.append(PushAwayCommand(grid, to_coord, faces))

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