from abc import ABC, abstractmethod
from command import CommandDecorator
from command import MoveCommand, HealCommand
from util import Compass


class IAbility(ABC):
    def __init__(self, unit):
        self.unit = unit

    @abstractmethod
    def gen_actions(self):
        pass

    @property
    def should_not_move(self):
        return self.unit.has_moved or self.unit.has_fired

    @property
    def should_not_fire(self):
        return not self.unit.has_moved or self.unit.has_fired


class Move(IAbility):
    def __init__(self, unit, grid):
        super().__init__(unit)
        self.grid = grid

    def gen_actions(self):
        if self.should_not_move:
            return []

        return [CommandDecorator(self.unit, MoveCommand(self.grid, self.unit.coord, coord)) for coord in
                self.grid.get_movable_tiles(self.unit.coord, self.unit.moves)]


class Repair(IAbility):
    def __init__(self, unit, amount=1):
        super().__init__(unit)
        self.amount = amount

    def gen_actions(self):
        if self.should_not_fire:
            return []
        return [CommandDecorator(self.unit, HealCommand(self.unit, self.amount))]


class Artillery(IAbility):
    def __init__(self, unit, grid, ammo_type, damage):
        super().__init__(unit)
        self.grid = grid
        self.ammo_type = ammo_type
        self.damage = damage

    def gen_viable_targets(self):
        return self.grid.get_artillery_tiles(self.unit.coord)

    def gen_actions(self):
        if self.should_not_fire:
            return []
        return [CommandDecorator(self.unit, self.ammo_type(self.unit, self.grid, self.damage, coord)) for coord in
                self.gen_viable_targets()]


class Beam(IAbility):
    def __init__(self, unit, grid, ammo_type, damage):
        super().__init__(unit)
        self.grid = grid
        self.ammo_type = ammo_type
        self.damage = damage

    def gen_actions(self):
        actions = []
        if self.should_not_fire:
            return []
        x, y = self.unit.coord
        for dx, dy in Compass.FACES:
            if x + dx in range(self.grid.square_len) and y + dy in range(self.grid.square_len):
                actions.append(CommandDecorator(self.unit, self.ammo_type(self.unit, self.grid, (dx, dy), self.damage)))
        return actions