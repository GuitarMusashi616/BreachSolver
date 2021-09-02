from abc import ABC, abstractmethod

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

    @abstractmethod
    def reset_turn(self):
        pass

    @property
    @abstractmethod
    def __repr__(self):
        pass


class Unit(IUnit):
    def __init__(self, name, max_health=4, health=4, moves=3):
        self.name = name
        self.max_health = max_health
        self.health = health
        self.moves = moves
        self.abilities = []
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
        self._health = Util.clamp(value, 0, self.max_health)

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

    #     def heal(self, amount):
    #         self.health += amount

    #     def damage(self, amount):
    #         self.health -= amount

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


class Mech(Unit):
    pass


class Vek(Unit):
    def __init__(self, name, max_health=4, health=4, moves=3):
        super().__init__(name, max_health, health, moves)
        self.target = NullCommand()

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, command):
        self._target = command