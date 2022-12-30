from abc import ABC, abstractmethod

from ability import Move, Repair
from command import NullCommand
from util import Util


class IUnit(ABC):
    @property
    @abstractmethod
    def health(self):
        pass

    @property
    @abstractmethod
    def at_max_health(self):
        pass

    @property
    @abstractmethod
    def coord(self):
        pass

    @abstractmethod
    def gen_actions(self):
        pass

    @abstractmethod
    def add(self, ability):
        pass

    @property
    @abstractmethod
    def has_moved(self):
        pass

    @property
    @abstractmethod
    def has_fired(self):
        pass

    @property
    @abstractmethod
    def is_webbed(self):
        pass

    @abstractmethod
    def webbed_by(self, unit):
        pass

    @abstractmethod
    def reset_turn(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass


class Unit(IUnit):
    def __init__(self, name, max_health=1, health=1, moves=0, is_flying=False):
        self.name = name
        self.max_health = max_health
        self.health = health
        self.moves = moves
        self.abilities = []
        self.on_death = []
        self.is_flying = is_flying
        self.is_massive = False
        self.is_waterlogged = False
        self.web_details = None
        self.has_moved = False
        self.has_fired = False

    @property
    def is_alive(self):
        if self._health > 0:
            return True
        return False

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = min(value, self.max_health)

    @property
    def at_max_health(self):
        if self.health == self.max_health:
            return True
        return False

    @property
    def coord(self):
        return self._coord

    @coord.setter
    def coord(self, value):
        self._coord = value

    @property
    def has_moved(self):
        return self._has_moved

    @has_moved.setter
    def has_moved(self, value):
        self._has_moved = value

    @property
    def has_fired(self):
        return self._has_fired

    @has_fired.setter
    def has_fired(self, value):
        self._has_fired = value

    def reset_turn(self):
        self.has_moved = False
        self.has_fired = False

    @property
    def is_webbed(self):
        if not self.web_details:
            return None

        unit, unit_coord, self_coord = self.web_details
        if unit.is_alive and unit.coord == unit_coord and self_coord == self.coord:
            return True

        return False

    def webbed_by(self, unit):
        self.web_details = (unit, unit.coord, self.coord)

    def add(self, ability):
        self.abilities.append(ability)

    def gen_actions(self):
        i = 1
        actions = {}
        for ability in self.abilities:
            for action in ability.gen_actions():
                actions[i] = action
                i += 1
        return actions

    #     def get_available_actions(self, grid):
    #         return [("MOVE", x) for x in grid.get_movable_tiles(self.coord, self.moves)] + \
    #         [("SHOOT", x) for x in grid.get_artillery_tiles(self.coord)]

    def __repr__(self):
        return self.name + ' ' + '♡' * self.health
