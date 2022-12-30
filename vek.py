from ability import Move
from attack import NullAttack, UnstableGuts, AcceleratingThorax, Pincers, SpittingGlands, Stinger, HiveTargetting, \
    DiggingTusks
from command import NullCommand
from unit import Unit
from util import Compass


class Vek(Unit):
    def __init__(self, name, max_health=3, health=3, moves=3, is_flying=False):
        super().__init__(name, max_health, health, moves, is_flying)
        self.attack_order = "#1000"
        self.target = NullCommand()
        self.attack = NullAttack()
        self.direction = None
        self.offset = None

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, command):
        self._target = command

    @property
    def attack(self):
        return self._attack

    @attack.setter
    def attack(self, value):
        self._attack = value

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = value

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = value

    @property
    def attack_order(self):
        return self._attack_order

    @attack_order.setter
    def attack_order(self, value):
        assert value[0] == '#'
        self._attack_order = int(value[1])

    @staticmethod
    def init_vek(vek, grid):
        if vek is None:
            return
        vek.add(Move(vek, grid))

    @staticmethod
    def parse_direction(char):
        if char == "N":
            return Compass.NORTH
        elif char == "E":
            return Compass.EAST
        elif char == "W":
            return Compass.WEST
        elif char == "S":
            return Compass.SOUTH
        else:
            return None

    @classmethod
    def create(cls, grid, name, max_health, health, attack_order, direction=None, offset=1):
        vek = cls(name, max_health, health, 2)
        vek.attack = NullAttack()
        direction = cls.parse_direction(direction)
        if name == "Blob":
            vek.attack = UnstableGuts(vek, grid, 1)
        elif name == "Firefly":
            vek.attack = AcceleratingThorax(vek, grid, 1)
        elif name == "Alpha Firefly":
            vek.attack = AcceleratingThorax(vek, grid, 3)
        elif name == "Scarab":
            vek.attack = SpittingGlands(vek, grid, 1)
        elif name == "Alpha Scarab":
            vek.attack = SpittingGlands(vek, grid, 3)
        elif name == "Beetle":
            vek.attack = Pincers(vek, grid, 1)
        elif name == "Alpha Beetle":
            vek.attack = Pincers(vek, grid, 3)
        elif name == "Beetle Leader":
            vek.is_massive = True
            vek.attack = Pincers(vek, grid, 3)
        elif name == "Hornet":
            vek.is_flying = True
            vek.attack = Stinger(vek, grid, 1)
        elif name == "Alpha Hornet":
            vek.is_flying = True
            vek.attack = Stinger(vek, grid, 3)
        elif name == "Digger":
            vek.attack = DiggingTusks(vek, grid, 1)
        elif name == "Alpha Digger":
            vek.attack = DiggingTusks(vek, grid, 2)
        elif name == "Psion Tyrant":
            vek.is_flying = True
            vek.attack = HiveTargetting(vek, grid, 1)

        vek.direction = direction
        vek.offset = offset
        vek.attack_order = attack_order
        cls.init_vek(vek, grid)
        return vek
