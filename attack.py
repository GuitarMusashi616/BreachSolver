from abc import ABC, abstractmethod

from beam import VekCommand, VekBeam, VekCharge
from command import CommandDecorator, CompositeCommand, DamageAdjacentCommand, DamageCommand, NullCommand, \
    DamageUnitCommand
from command import MoveCommand, HealCommand
from util import Compass


class IAttack(ABC):
    """Used in place of ability for veks, allows them to generate a command given a direction and offset"""

    @abstractmethod
    def attack(self, direction=None, offset=1):
        pass


class NullAttack(IAttack):
    def attack(self, direction=None, offset=1):
        return NullCommand()


class UnstableGuts(IAttack):
    """Blob Attack"""
    # basically do damage to the 5 tiles nearby if alive
    def __init__(self, unit, grid, damage):
        self.unit = unit
        self.grid = grid
        self.damage = damage

    def attack(self, direction=None, offset=1):
        commands = [DamageAdjacentCommand(self.grid, self.unit.coord, self.damage), DamageCommand(self.grid, self.unit.coord, self.damage)]
        return VekCommand(self.unit, CompositeCommand(commands))


class AcceleratingThorax(IAttack):
    """Firefly Attack"""
    def __init__(self, unit, grid, damage):
        self.unit = unit
        self.grid = grid
        self.damage = damage

    def attack(self, direction=None, offset=1):
        return VekBeam(self.unit, self.grid, direction, self.damage)


class Pincers(IAttack):
    """Beetle Attack"""
    def __init__(self, unit, grid, damage):
        self.unit = unit
        self.grid = grid
        self.damage = damage

    def attack(self, direction=None, offset=1):
        return VekCharge(self.unit, self.grid, direction, self.damage)


class SpittingGlands(IAttack):
    """Scarab Attack"""
    def __init__(self, unit, grid, damage):
        self.unit = unit
        self.grid = grid
        self.damage = damage

    def attack(self, direction=None, offset=1):
        x,y = self.unit.coord
        dx,dy = direction
        target = (x+dx*offset, y+dy*offset)
        return VekCommand(self.unit, DamageCommand(self.grid, target, self.damage))


class Stinger(IAttack):
    """Hornet Attack"""
    def __init__(self, unit, grid, damage):
        self.unit = unit
        self.grid = grid
        self.damage = damage

    def attack(self, direction=None, offset=1):
        x,y = self.unit.coord
        dx,dy = direction
        target = (x+dx*offset, y+dy*offset)
        return VekCommand(self.unit, DamageCommand(self.grid, target, self.damage))


class HiveTargetting(IAttack):
    """Psion Tyrant Attack"""
    def __init__(self, unit, grid, damage):
        self.unit = unit
        self.grid = grid
        self.damage = damage

    def attack(self, direction=None, offset=1):
        return VekCommand(self.unit, CompositeCommand([DamageUnitCommand(mech, self.damage, self.grid) for mech in self.grid.mechs]))


class DiggingTusks(IAttack):
    """Digger Attack (does not create rocks)"""
    def __init__(self, unit, grid, damage):
        self.unit = unit
        self.grid = grid
        self.damage = damage

    def attack(self, direction=None, offset=1):
        return VekCommand(self.unit, DamageAdjacentCommand(self.grid, self.unit.coord, self.damage))