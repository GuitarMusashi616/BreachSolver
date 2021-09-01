from abc import ABC, abstractmethod

import grid
from command import CommandDecorator
from command import MoveCommand, HealCommand
from util import Compass


class IAbility(ABC):
    @abstractmethod
    def gen_actions(self):
        pass


class Move(IAbility):
    def __init__(self, unit, grid):
        self.unit = unit
        self.grid = grid

    def gen_actions(self):
        if self.unit.has_moved or self.unit.has_fired:
            return []

        return [CommandDecorator(self.unit, MoveCommand(self.grid, self.unit.coord, coord)) for coord in
                self.grid.get_movable_tiles(self.unit.coord, self.unit.moves)]


class Repair(IAbility):
    def __init__(self, unit, amount=1):
        self.unit = unit
        self.amount = amount

    def gen_actions(self):
        if self.unit.has_fired:
            return []
        return [CommandDecorator(self.unit, HealCommand(self.unit, self.amount))]


class Artillery(IAbility):
    def __init__(self, unit, grid, ammo_type, damage):
        self.unit = unit
        self.grid = grid
        self.ammo_type = ammo_type
        self.damage = damage

    def gen_viable_targets(self):
        return self.grid.get_artillery_tiles(self.unit.coord)

    def gen_actions(self):
        if self.unit.has_fired:
            return []
        return [CommandDecorator(self.unit, self.ammo_type(self.grid, self.damage, coord, self.unit.coord)) for coord in
                self.gen_viable_targets()]


class Beam(IAbility):
    def __init__(self, unit, grid: grid.IGrid, damage: int):
        self.unit = unit
        self.grid = grid
        self.ammo_type = self.ammo_type
        self.damage = damage

    def gen_actions(self):
        actions = []
        if self.unit.has_fired:
            return actions
        x, y = self.unit.coord
        for dx, dy in Compass.FACES:
            if x + dx in range(self.grid.square_len) and y + dy in range(self.grid.square_len):
                actions.append(CommandDecorator(self.unit, self.ammo_type(self.unit, self.grid, (dx, dy), self.damage)))
        return actions